from src.model import db # traz a instancia do sqlalchemy 
from sqlalchemy.schema import Column # traz o recurso para o ORM entender que o atributo será uma coluna na tabela
from sqlalchemy.types import String, DECIMAL, Integer #Importando os tipos de dados que as colunas vao aceitar

class Colaborador(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    #nome = VARCHAR(100)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(255))
    cargo = Column(String(100))
    salario = Column(DECIMAL(10,2))
    telefone = Column(String(20))
    cep = Column(String(10))     
    endereco = Column(String(150))
    cidade = Column(String(100))
    
    def __init__(self, nome, email, senha, cargo, salario, telefone, cep, endereco, cidade):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario
        self.telefone = telefone
        self.cep = cep
        self.endereco = endereco
        self.cidade = cidade
        
    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'senha': self.senha,
            'nome': self.nome,
            'cargo': self.cargo,
            'id': self.id
        }
        
    def all_data(self) -> dict:
        return {
            'id': self.id,
            'nome': self.nome,
            'cargo': self.cargo,
            'salario': self.salario,
            'email': self.email,
            'telefone': self.telefone,
            'cep': self.cep,
            'endereco': self.endereco,
            'cidade': self.cidade
        }     
        