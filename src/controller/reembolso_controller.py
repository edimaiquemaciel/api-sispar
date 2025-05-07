
from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso
from flask_jwt_extended import jwt_required


bp_reembolso = Blueprint("reembolso", __name__, url_prefix="/reembolso")

@bp_reembolso.route("/todos-reembolsos")
@jwt_required()
def pegar_todos_reembolsos():
    reembolsos = db.session.execute(
        db.select(Reembolso)
    ).scalars().all()
    
    reembolsos = [reembolso.all_data() for reembolso in reembolsos]
    
    return jsonify(reembolsos), 200

@bp_reembolso.route("/solicitar-reembolso", methods=["POST"])
@jwt_required()
def solicitar_novo_reembolso():
    dados_requisicao = request.get_json()
    
    CAMPOS_OBRIGATORIOS = [
    'colaborador', 'empresa', 'num_prestacao',
    'tipo_reembolso', 'centro_custo', 'moeda',
    'valor_faturado', 'despesa', 'id_colaborador'
    ]
    
    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados_requisicao]
    if faltando:
        return jsonify({'erro': f'Campos obrigatórios ausentes: {", ".join(faltando)}'}), 400

    try:
        novo_reembolso = Reembolso(
            colaborador=dados_requisicao["colaborador"],
            empresa=dados_requisicao["empresa"],
            num_prestacao=dados_requisicao["num_prestacao"],
            descricao=dados_requisicao.get("descricao"),
            data=dados_requisicao.get("data"),
            tipo_reembolso=dados_requisicao["tipo_reembolso"],
            centro_custo=dados_requisicao["centro_custo"],
            ordem_interna=dados_requisicao.get("ordem_interna"),
            divisao=dados_requisicao.get("divisao"),
            pep=dados_requisicao.get("pep"),
            moeda=dados_requisicao["moeda"],
            distancia_km=dados_requisicao.get("distancia_km"),
            valor_km=dados_requisicao.get("valor_km"),
            valor_faturado=dados_requisicao["valor_faturado"],
            despesa=dados_requisicao["despesa"],
            id_colaborador=dados_requisicao["id_colaborador"],
            status=dados_requisicao.get("status", "Em análise")
        )
    
        db.session.add(novo_reembolso)
        db.session.commit()
        
        return jsonify({
                'mensagem': 'Solicitação de reembolso cadastrada com sucesso',
                'reembolso': novo_reembolso.all_data()
            }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
    
@bp_reembolso.route("/reembolsos-prestacao/<int:num_prestacao>")
@jwt_required()
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
    
    