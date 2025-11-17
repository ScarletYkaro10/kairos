import pytest
from fastapi.testclient import TestClient
from src.main import app 
from src.services.auth_service import fake_users_db  

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_fake_db():
    fake_users_db.clear()
    yield


def test_register_user_success():
    """
    Testa o Teste 1: Registro bem-sucedido (Code 201)
    """
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )

    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "password" not in data  

def test_register_user_already_exists():
    """
    Testa se a API previne o registro de um e-mail duplicado (Code 400)
    """

    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "outrasenha"}
    )
    
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
    assert response.status_code == 422

def test_register_user_weak_password():
    """
    Testa se o schema de validação (Pydantic) barra uma senha fraca (Code 422)
    """
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "123"} 
    )
    assert response.status_code == 422


def test_login_success():
    """
    Testa o Teste 2: Login bem-sucedido (Code 200)
    """
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password():
    """
    Testa o Teste 3: Login com senha errada (Code 401)
    """
    client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "senhaforte123"}
    )
    
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "senhaERRADA"}
    )
    
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
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Email ou senha incorretos"