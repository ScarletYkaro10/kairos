from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict
from uuid import UUID, uuid4

import pytest
from fastapi.testclient import TestClient

from src.main import create_app
from src.services import task_service


@pytest.fixture(autouse=True)
def _reset_task_repo():
    task_service.reset_repository()
    yield
    task_service.reset_repository()


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app())


def auth_headers(user_id: UUID | None = None) -> Dict[str, str]:
    token = user_id or uuid4()
    return {"Authorization": f"Bearer {token}"}


def build_payload(**overrides) -> Dict[str, str]:
    base = {
        "title": "Test task",
        "description": "Ensure CRUD works",
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "priority": "medium",
        "status": "pending",
    }
    base.update(overrides)
    return base


def test_create_task_requires_auth(client: TestClient):
    response = client.post("/tasks", json=build_payload())
    assert response.status_code == 401


def test_create_and_list_tasks(client: TestClient):
    headers = auth_headers()

    create_resp = client.post("/tasks", json=build_payload(), headers=headers)
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["title"] == "Test task"

    list_resp = client.get("/tasks", headers=headers)
    assert list_resp.status_code == 200
    data = list_resp.json()
    assert len(data) == 1
    assert data[0]["id"] == created["id"]


def test_optimize_schedule_orders_by_priority_then_due_date(client: TestClient):
    headers = auth_headers()
    task_payloads = [
        build_payload(title="Low priority", priority="low"),
        build_payload(
            title="High late",
            priority="high",
            due_date=(datetime.utcnow() + timedelta(days=5)).isoformat(),
        ),
        build_payload(
            title="High soon",
            priority="high",
            due_date=(datetime.utcnow() + timedelta(days=2)).isoformat(),
        ),
    ]

    for payload in task_payloads:
        resp = client.post("/tasks", json=payload, headers=headers)
        assert resp.status_code == 201

    optimize_resp = client.post("/optimize-schedule", headers=headers)
    assert optimize_resp.status_code == 200

    ordered_titles = [task["title"] for task in optimize_resp.json()]
    assert ordered_titles == ["High soon", "High late", "Low priority"]
