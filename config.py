#Armazenar as configurações do ambiente de desenvolvimento
from os import environ # acessa as variáveis de ambiente

from dotenv import load_dotenv #carregamento das variáveis de ambiente nesse arquivo

load_dotenv()

class Config():
    SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV") # puxa a variável e utiliza para a conexão
    SQLALCHEMY_TRACK_MODIFICATIONS=False #Otimiza as queries no banco de dados
    