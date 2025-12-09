import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone
from typing import Dict
from src.main import app


def build_payload(**overrides) -> Dict[str, str]:
    """Helper auxiliar para criar dados de tarefa nos testes."""
    base = {
        "title": "Test task",
        "description": "Ensure CRUD works",
        "due_date": (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(),
        "priority": "medium",
        "status": "pending",
        "category": "Trabalho",
        "difficulty": 3,
        "estimated_minutes": 60,
    }
    base.update(overrides)
    return base


def test_create_task_requires_auth(client: TestClient):
    """
    Testa se tentar criar tarefa sem logar retorna erro 403/401.
    """
    response = client.post("/tasks", json=build_payload())
    assert response.status_code in [401, 403]
    assert response.json().get("detail") == "Not authenticated"


def test_create_and_list_tasks(client: TestClient):
    """
    Testa o fluxo completo feliz: Registrar -> Logar -> Criar -> Listar.
    """
    client.post(
        "/auth/register", json={"email": "task@test.com", "password": "senhaforte123"}
    )

    login_resp = client.post(
        "/auth/login", json={"email": "task@test.com", "password": "senhaforte123"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    create_resp = client.post(
        "/tasks", json=build_payload(title="Minha Tarefa Real"), headers=headers
    )
    assert create_resp.status_code == 201
    created_data = create_resp.json()
    assert created_data["title"] == "Minha Tarefa Real"
    created_id = created_data["id"]

    list_resp = client.get("/tasks", headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.json()

    assert len(data) == 1
    assert data[0]["id"] == created_id
    assert data[0]["title"] == "Minha Tarefa Real"


def test_optimize_schedule(client: TestClient):
    """
    Smoke Test para garantir que o endpoint da IA não está quebrando.
    """
    client.post(
        "/auth/register", json={"email": "ia@test.com", "password": "senhaforte123"}
    )
    token = client.post(
        "/auth/login", json={"email": "ia@test.com", "password": "senhaforte123"}
    ).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/tasks",
        json=build_payload(title="Urgente", priority="medium"),
        headers=headers,
    )

    client.post(
        "/tasks", json=build_payload(title="Relax", priority="medium"), headers=headers
    )

    optimize_resp = client.post("/optimize-schedule", headers=headers)

    assert optimize_resp.status_code == 200

    res_json = optimize_resp.json()
    assert isinstance(res_json, list)
    assert len(res_json) == 2
