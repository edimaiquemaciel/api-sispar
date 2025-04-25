from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flask_cors import cross_origin

bp_colaborador = Blueprint("colaborador", __name__, url_prefix="/colaborador")

dados = [
        {"id": 1, "nome": "maique", "cargo": "dev senior", "cracha": "00011"},
        {"id": 2, "nome": "lucas", "cargo": "dev jr", "cracha": "00012"},
        {"id": 3, "nome": "mauro", "cargo": "dev jr", "cracha": "00013"},
        {"id": 4, "nome": "karla", "cargo": "dev pleno", "cracha": "00014"},
        {"id": 5, "nome": "bruno", "cargo": "dev pleno", "cracha": "00015"},
    ]

@bp_colaborador.route("/pegar-dados")
def pegar_dados():
    colaboradores = Colaborador.query.all()
    resultado = []
    for c in colaboradores:
        resultado.append({
            "id": c.id,
            "nome": c.nome,
            "email": c.email,
            "senha": c.senha,
            "cargo": c.cargo,
            "salario": c.salario
        })
    return jsonify(resultado)

@bp_colaborador.route("/cadastrar", methods=["POST"])
def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()
    
    novo_colaborador = Colaborador(
        nome=dados_requisicao["nome"],
        email=dados_requisicao["email"],
        senha=hash_senha(dados_requisicao["senha"]),
        cargo=dados_requisicao["cargo"],
        salario=dados_requisicao["salario"]
    )
    db.session.add(novo_colaborador)    
    db.session.commit()
    
    return jsonify({"mensagem": "Dado cadastrado com sucesso"}), 201

@bp_colaborador.route("/atualizar/<int:id_colaborador>", methods=["PUT"])
def atualizar_dados_do_colaborador(id_colaborador):
    dados_requisicao = request.get_json()
    
    for colaborador in dados:
        if colaborador["id"] == id_colaborador:
            colaborador_encontrado = colaborador
            break
    if "nome" in dados_requisicao:
        colaborador_encontrado["nome"] = dados_requisicao["nome"]
    if "cargo" in dados_requisicao:
        colaborador_encontrado["cargo"] = dados_requisicao["cargo"]
    if "senha" in dados_requisicao:
        colaborador_encontrado["senha"] = hash_senha(dados_requisicao["senha"])
            
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
        return jsonify({"mensagem": "Login realizado com sucesso", "nome": colaborador.get('nome') , "email": colaborador.get('email'), "cargo": colaborador.get('cargo')}), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'})