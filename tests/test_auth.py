import pytest
from fastapi.testclient import TestClient
from src.main import app  # Importa nossa aplicação FastAPI principal
from src.services.auth_service import fake_users_db  # Importa nosso "banco"

# Cria um "Cliente de Teste" que simula requisições à nossa API
client = TestClient(app)

# Fixture do Pytest para limpar o banco de dados falso antes de cada teste
@pytest.fixture(autouse=True)
def clean_fake_db():
    fake_users_db.clear()
    yield

# ==================================
#         Testes de Registro
# ==================================

def test_register_user_success():
    """
    Testa o Teste 1: Registro bem-sucedido (Code 201)
    """
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    # Verifica se o status code é 201 (Created)
    assert response.status_code == 201
    
    # Verifica se a resposta contém os dados corretos (sem a senha)
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  # Garante que a senha não foi vazada

def test_register_user_already_exists():
    """
    Testa se a API previne o registro de um e-mail duplicado (Code 400)
    """
    # Primeiro, registra um usuário
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    # Segundo, tenta registrar o MESMO usuário
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "outrasenha"}
    )
    
    # Verifica se o status code é 400 (Bad Request)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já registrado."

def test_register_user_invalid_email():
    """
    Testa se o schema de validação (Pydantic) barra um email inválido (Code 422)
    """
    response = client.post(
        "/auth/register",
        json={"email": "email-invalido", "password": "senhaforte123"}
    )
    # 422 é o código do FastAPI para "Unprocessable Entity" (falha de validação)
    assert response.status_code == 422

def test_register_user_weak_password():
    """
    Testa se o schema de validação (Pydantic) barra uma senha fraca (Code 422)
    """
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "123"} # Senha < 8 caracteres
    )
    assert response.status_code == 422

# ==================================
#         Testes de Login
# ==================================

def test_login_success():
    """
    Testa o Teste 2: Login bem-sucedido (Code 200)
    """
    # Primeiro, registra o usuário
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    # Agora, tenta logar
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    # Verifica se o login deu certo (Code 200)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """
    Testa o Teste 3: Login com senha errada (Code 401)
    """
    # Registra o usuário
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    # Tenta logar com a senha errada
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "senhaERRADA"}
    )
    
    # Verifica se deu "Não Autorizado" (Code 401)
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos"

def test_login_user_not_found():
    """
    Testa o login com um usuário que não existe (Code 401)
    """
    response = client.post(
        "/auth/login",
        json={"email": "ninguem@example.com", "password": "senhaforte123"}
    )
    
    # Verifica se deu "Não Autorizado" (Code 401)
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos"