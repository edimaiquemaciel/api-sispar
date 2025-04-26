import pytest
import time
from src.model.colaborador_model import Colaborador
from src.app import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app
    
@pytest.fixture
def client(app):
    return app.test_client()
    
    
def test_desempenho_requisicao_get(client):
    comeco = time.time()
    
    for _ in range(1000):
        resposta = client.get('/colaborador/todos-colaboradores')
        
    fim = time.time() - comeco
    
    assert fim < 1.0