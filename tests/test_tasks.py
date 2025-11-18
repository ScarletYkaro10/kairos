import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from typing import Dict
from src.main import app
from src.services import task_service
from src.services import auth_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def _reset_all_repositories():
    """Limpa os bancos de dados falsos antes de CADA teste."""
    task_service.reset_repository()
    auth_service.fake_users_db.clear()
    yield


@pytest.fixture
def authenticated_headers() -> Dict[str, str]:
    """
    Fixture que faz o trabalho do Pilar de Segurança:
    1. Registra um usuário
    2. Faz login
    3. Retorna os headers de autorização com o token REAL.
    """
    client.post(
        "/auth/register",
        json={"email": "test.task@example.com", "password": "senhaforte123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "test.task@example.com", "password": "senhaforte123"},
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def build_payload(**overrides) -> Dict[str, str]:
    """Helper para criar payloads de tarefa."""
    base = {
        "title": "Test task",
        "description": "Ensure CRUD works",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "priority": "medium",
        "status": "pending",
    }
    base.update(overrides)
    return base


def test_create_task_requires_auth():
    """Testa se a "dependência de porteiro" está funcionando"""
    response = client.post("/tasks", json=build_payload())
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_create_and_list_tasks(authenticated_headers: Dict[str, str]):
    """
    Testa se conseguimos criar e listar tarefas USANDO um token válido
    """
    headers = authenticated_headers

    create_resp = client.post("/tasks", json=build_payload(), headers=headers)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["title"] == "Test task"

    list_resp = client.get("/tasks", headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["id"] == created["id"]


def test_optimize_schedule_orders_by_priority_then_due_date(
    authenticated_headers: Dict[str, str],
):
    """
    Testa o mock da IA, agora protegido por token.
    (Este teste é o do Wesley, mas com o header de auth)
    """
    headers = authenticated_headers
    task_payloads = [
        build_payload(title="Low priority", priority="low"),
        build_payload(
            title="High late",
            priority="high",
            # Correção: timezone.utc
            due_date=(datetime.now(timezone.utc) + timedelta(days=5)).isoformat(),
        ),
        build_payload(
            title="High soon",
            priority="high",
            # Correção: timezone.utc
            due_date=(datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
        ),
    ]

    for payload in task_payloads:
        resp = client.post("/tasks", json=payload, headers=headers)
        assert resp.status_code == 201

    optimize_resp = client.post("/optimize-schedule", headers=headers)
    assert optimize_resp.status_code == 200

    ordered_titles = [task["title"] for task in optimize_resp.json()]
    assert ordered_titles == ["High soon", "High late", "Low priority"]
