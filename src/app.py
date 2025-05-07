from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso
from src.model import db
from config import Config
from flasgger import Swagger
import pymysql
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os
load_dotenv()

pymysql.install_as_MySQLdb()

swagger_config = {
    
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec", # <-- Da um nome de referencia para a documentacao
            "route": "/apispec.json/", # <- Rota do arquivo JSON para a construção da documentação
            "rule_filter": lambda rule: True, # <-- Todas as rotas/endpoints serão documentados
            "model_filter": lambda tag: True, # <-- Especificar quuais modelos da entidade serão documentados
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/", 
}

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)
    app.config.from_object(Config)
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
    jwt = JWTManager(app)
    
    db.init_app(app)
    
    Swagger(app, config=swagger_config)
    
    with app.app_context():
        db.create_all()
    
    return app

# Crie a instância da aplicação no nível do módulo
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))