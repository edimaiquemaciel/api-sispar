# Desafio Final SISPAR - Back-End Vai Na Web

![Versão](https://img.shields.io/badge/versão-1.0.0-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Flask](https://img.shields.io/badge/Flask-3.1.0-red)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.40-yellow)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-orange)

Sistema de gerenciamento de reembolsos desenvolvido com Flask para cadastro e controle de colaboradores e suas respectivas solicitações de reembolso.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação e Configuração](#instalação-e-configuração)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Uso da API](#uso-da-api)
- [Documentação da API](#documentação-da-api)
- [Endpoints](#endpoints)
- [Autenticação](#autenticação)
- [Testes](#testes)
- [Deploy](#deploy)
- [Contato](#contato)

## 🔍 Visão Geral

O Sistema de Gerenciamento de Reembolsos é uma aplicação backend desenvolvida para gerenciar os dados de colaboradores e suas solicitações de reembolso. O sistema permite o cadastro de colaboradores, autenticação via JWT, e o gerenciamento completo das solicitações de reembolso com status de aprovação.

## ⚙️ Funcionalidades

### Colaboradores
- Cadastro de novos colaboradores
- Autenticação via JWT
- Listagem de todos os colaboradores
- Atualização de dados pessoais

### Reembolsos
- Solicitação de reembolsos (individual ou em lote)
- Listagem de todos os reembolsos
- Busca de reembolsos por número de prestação de contas
- Rastreamento de status de reembolsos

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**: Linguagem de programação
- **Flask 3.1.0**: Framework web
- **SQLAlchemy 2.0.40**: ORM para banco de dados
- **Flask-JWT-Extended 4.7.1**: Autenticação JWT
- **Flask-Bcrypt 1.0.1**: Criptografia de senhas
- **Flask-CORS 5.0.1**: Suporte a CORS
- **Flasgger 0.9.7.1**: Documentação da API com Swagger
- **PyMySQL 1.1.1**: Conexão com banco de dados MySQL
- **Pytest 8.3.5**: Framework para testes

## 📁 Estrutura do Projeto

```
sistema-de-reembolsos/
├── .env                      # Variáveis de ambiente (não versionado)
├── .gitignore                # Arquivos ignorados pelo Git
├── config.py                 # Configurações do aplicativo
├── Procfile                  # Configuração para deploy no Heroku
├── requirements.txt          # Dependências do projeto
├── run.py                    # Ponto de entrada da aplicação
└── src/
    ├── __init__.py
    ├── app.py                # Configuração da aplicação Flask
    ├── controller/
    │   ├── colaborador_controller.py  # Controlador de colaboradores
    │   └── reembolso_controller.py    # Controlador de reembolsos
    ├── docs/                 # Documentação da API (Swagger)
    │   ├── colaborador/
    │   └── reembolso/
    ├── model/
    │   ├── __init__.py       # Instância do SQLAlchemy
    │   ├── colaborador_model.py       # Modelo de colaboradores
    │   └── reembolso_model.py         # Modelo de reembolsos
    ├── security/
    │   └── security.py       # Funções de criptografia
    └── tests/
        ├── __init__.py
        └── test_app.py       # Testes da aplicação
```

## 🚀 Instalação e Configuração

### Pré-requisitos
- Python 3.9+
- MySQL ou outro banco de dados compatível

### Instalação
1. Clone o repositório:
```bash
git clone https://github.com/edimaiquemaciel/api-sispar.git
cd api-sispar
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (veja a seção [Variáveis de Ambiente](#variáveis-de-ambiente))

5. Execute a aplicação:
```bash
python run.py
```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```
URL_DATABASE_DEV=mysql+pymysql://usuario:senha@localhost/nome_do_banco
JWT_SECRET_KEY=sua_chave_secreta_para_jwt
PORT=5000
```

## 📲 Uso da API

### Exemplo de uso (com curl)

#### Cadastro de Colaborador
```bash
curl -X POST http://localhost:5000/colaborador/cadastrar \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João da Silva",
    "email": "joao@empresa.com",
    "senha": "senha123",
    "cargo": "Analista",
    "salario": 5000.00,
    "telefone": "99 9999-9999",
    "cep": "12345-678",
    "endereco": "Rua Exemplo, 123",
    "cidade": "São Paulo"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/colaborador/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "joao@empresa.com",
    "senha": "senha123"
  }'
```

#### Solicitar Reembolso (autenticado)
```bash
curl -X POST http://localhost:5000/reembolso/solicitar-reembolso \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {seu_token_jwt}" \
  -d '[{
    "colaborador": "João da Silva",
    "empresa": "Empresa X",
    "num_prestacao": 101,
    "descricao": "Viagem a trabalho",
    "data": "2025-05-01",
    "tipo_reembolso": "Transporte",
    "centro_custo": "CC-123",
    "ordem_interna": "OI-456",
    "divisao": "Comercial",
    "pep": "PEP001",
    "moeda": "BRL",
    "distancia_km": "30",
    "valor_km": "1.5",
    "valor_faturado": 200.00,
    "despesa": 75.50,
    "id_colaborador": 1
  }]'
```

## 📚 Documentação da API

A documentação completa da API está disponível através do Swagger UI no endpoint `/apidocs/`. Após iniciar a aplicação, acesse:

```
http://localhost:5000/apidocs/
```

## 🔄 Endpoints

### Colaboradores
- `GET /colaborador/todos-colaboradores` - Lista todos os colaboradores
- `POST /colaborador/cadastrar` - Cadastra um novo colaborador
- `PUT /colaborador/atualizar/<id_colaborador>` - Atualiza dados de um colaborador
- `POST /colaborador/login` - Realiza login e retorna um token JWT

### Reembolsos
- `GET /reembolso/todos-reembolsos` - Lista todos os reembolsos
- `POST /reembolso/solicitar-reembolso` - Solicita um ou mais reembolsos
- `GET /reembolso/reembolsos-prestacao/<num_prestacao>` - Busca reembolsos por número de prestação

## 🔒 Autenticação

O sistema utiliza autenticação JWT (JSON Web Token). Para acessar endpoints protegidos:

1. Obtenha um token através do endpoint de login
2. Utilize o token em todas as requisições subsequentes no header `Authorization: Bearer {seu_token}`

Exemplo:
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." http://localhost:5000/reembolso/todos-reembolsos
```

## 🧪 Testes

Para executar os testes:

```bash
pytest
```

## 🌐 Deploy

A aplicação está configurada para deploy na plataforma Railway através do arquivo `Procfile`.

### Deploy no Railway
```bash
# Configure o projeto no dashboard do Railway
railway login
railway init
railway link

# Configure as variáveis de ambiente no dashboard do Railway ou via CLI
railway variables set URL_DATABASE_DEV=sua_url_de_banco_de_dados
railway variables set JWT_SECRET_KEY=sua_chave_secreta_jwt

# Deploy da aplicação
railway up
```
