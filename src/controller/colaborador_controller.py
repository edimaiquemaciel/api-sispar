from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flask_cors import cross_origin
from flasgger import swag_from
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp_colaborador = Blueprint("colaborador", __name__, url_prefix="/colaborador")


@bp_colaborador.route("/todos-colaboradores")
@jwt_required()
def pegar_dados_todos_colaboradores():
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()
    
    colaboradores = [colaborador.all_data() for colaborador in colaboradores]
    
    return jsonify(colaboradores), 200

@bp_colaborador.route("/cadastrar", methods=['POST', 'OPTIONS'])
@cross_origin()
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()
    email = dados_requisicao["email"]
    
    colaborador =db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()
    
    if colaborador:
        return  jsonify({"mensagem": "Já existe um colaborador com esse e-mail."}), 400
    
    novo_colaborador = Colaborador(
        nome=dados_requisicao["nome"],
        email=email,
        senha=hash_senha(dados_requisicao["senha"]),
        cargo=dados_requisicao["cargo"],
        salario=dados_requisicao["salario"],
        telefone=dados_requisicao["telefone"],
        cep=dados_requisicao["cep"],
        endereco=dados_requisicao["endereco"],
        cidade=dados_requisicao["cidade"]
    )
    db.session.add(novo_colaborador)    
    db.session.commit()
    
    return jsonify({"mensagem": "Dado cadastrado com sucesso"}), 201

@bp_colaborador.route("/atualizar/<int:id_colaborador>", methods=["PUT"])
@jwt_required()
def atualizar_dados_do_colaborador(id_colaborador):
    dados_requisicao = request.get_json()
    
    colaborador = Colaborador.query.get(id_colaborador)
    if not colaborador:
        return jsonify({"mensagem": "Colaborador não encontrado"}), 404
    usuario_autenticado = get_jwt_identity()
    if colaborador.email != usuario_autenticado:
        return jsonify({"mensagem": "Você não tem permissão para atualizar esses dados"}), 403
    
    if "nome" in dados_requisicao:
        colaborador.nome = dados_requisicao["nome"]
    if "cargo" in dados_requisicao:
        colaborador.cargo = dados_requisicao["cargo"]
    if "senha" in dados_requisicao:
        colaborador.senha = hash_senha(dados_requisicao["senha"])
        
    db.session.commit()
            
    return jsonify({"mensagem": "Dados do colaborador atualizados com sucesso!"}), 200

@bp_colaborador.route('/login', methods=['POST'])
@cross_origin()
def login():
    dados_requisicao = request.get_json()
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400
    
    colaborador =db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()
    
    if not colaborador:
        return jsonify({"mensagem": "Usuário não encontrado."}), 404
    
    colaborador = colaborador.to_dict()
    
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        access_token = create_access_token(identity=email)
        return jsonify({"mensagem": "Login realizado com sucesso", "nome": colaborador.get('nome') , "email": colaborador.get('email'), "cargo": colaborador.get('cargo'), "token": access_token}), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'}), 401