
from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from flasgger import swag_from


bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")

@bp_reembolso.route("/todos-reembolsos")
@jwt_required()
@swag_from('../docs/reembolso/buscar_reembolsos.yml')
def pegar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()
    
    reembolsos = [reembolso.all_data() for reembolso in reembolsos]
    
    return jsonify({
        'sucesso': True,
        'total': len(reembolsos),
        'dados': reembolsos
    }), 200

@bp_reembolso.route("/solicitar-reembolso", methods=["POST"])
@cross_origin()
@jwt_required()
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_novo_reembolso():
    dados_requisicao = request.get_json()
    
    if not isinstance(dados_requisicao, list):
        return jsonify({'erro': 'Esperado um array de reembolsos no corpo da requisição'}), 400
    if not dados_requisicao:
        return jsonify({'erro': 'O array de reembolsos está vazio'}), 400
    
    CAMPOS_OBRIGATORIOS = [
    'colaborador', 'empresa', 'num_prestacao',
    'tipo_reembolso', 'centro_custo', 'moeda',
    'valor_faturado', 'despesa', 'id_colaborador'
    ]
    
    reembolsos_criados = []
    
    try:
        for dados in dados_requisicao:
            faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]
            if faltando:
                raise ValueError(f"Campos obrigatórios ausentes em um dos reembolsos: {', '.join(faltando)}")
            novo_reembolso = Reembolso(
                colaborador=dados["colaborador"],
                empresa=dados["empresa"],
                num_prestacao=dados["num_prestacao"],
                descricao=dados.get("descricao"),
                data=dados.get("data") or None,
                tipo_reembolso=dados["tipo_reembolso"],
                centro_custo=dados["centro_custo"],
                ordem_interna=dados.get("ordem_interna"),
                divisao=dados.get("divisao"),
                pep=dados.get("pep"),
                moeda=dados["moeda"],
                distancia_km=dados.get("distancia_km"),
                valor_km=dados.get("valor_km"),
                valor_faturado=dados["valor_faturado"],
                despesa=dados["despesa"],
                id_colaborador=dados["id_colaborador"],
                status=dados.get("status", "Em análise")
            )
    
            db.session.add(novo_reembolso)
            reembolsos_criados.append(novo_reembolso)
            
        db.session.commit()
        
        return jsonify({
                'mensagem': 'Solicitação de reembolso cadastrada com sucesso',
                'reembolso': [r.all_data() for r in reembolsos_criados]
            }), 201
        
    except ValueError as ve:
        db.session.rollback()
        return jsonify({'erro': str(ve)}), 400    
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
    
@bp_reembolso.route("/reembolsos-prestacao/<int:num_prestacao>")
@jwt_required()
@swag_from('../docs/reembolso/buscar_num_prestacao.yml')
def pegar_reembolso_por_prestacao(num_prestacao):
    reembolsos = Reembolso.query.filter_by(num_prestacao=num_prestacao).all()
    
    if not reembolsos:
        return jsonify({
            'sucesso': False,
            'mensagem': f'Nenhum reembolso encontrado para o numero de prestação de contas #{num_prestacao}'
        }), 404
    return jsonify({
        'sucesso': True,
        'total': len(reembolsos),
        'dados': [r.all_data() for r in reembolsos]
    }), 200
    
    