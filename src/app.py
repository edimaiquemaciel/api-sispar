from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.model import db
from config import Config
import pymysql
import os

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(bp_colaborador)
    
    app.config.from_object(Config)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

# Crie a instância da aplicação no nível do módulo
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))