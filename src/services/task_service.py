from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from src.models.schemas import TaskCreate, TaskPublic, TaskStatus


class TaskRepository:
    """Simple in-memory storage to unblock Wesley's Day 2 scope.

    The implementation is intentionally straightforward so it can later
    evolve into a real database without touching the service API.
    """

    def __init__(self) -> None:
        self._items: Dict[UUID, TaskPublic] = {}

    def create(self, data: TaskCreate, owner_id: Optional[UUID] = None) -> TaskPublic:
        task = TaskPublic(**data.dict(), owner_id=owner_id)
        self._items[task.id] = task
        return deepcopy(task)

    def list(self, owner_id: Optional[UUID] = None) -> List[TaskPublic]:
        tasks = self._items.values()
        if owner_id is not None:
            tasks = [task for task in tasks if task.owner_id == owner_id]
        return [deepcopy(task) for task in tasks]

    def get(self, task_id: UUID) -> Optional[TaskPublic]:
        task = self._items.get(task_id)
        return deepcopy(task) if task else None

    def update(
        self,
        task_id: UUID,
        data: TaskCreate,
        *,
        status: Optional[TaskStatus] = None,
    ) -> Optional[TaskPublic]:
        task = self._items.get(task_id)
        if task is None:
            return None

        updated_payload = task.copy(update=data.dict(exclude_unset=True))
        if status:
            updated_payload.status = status
        updated_payload.updated_at = datetime.utcnow()
        self._items[task_id] = TaskPublic(**updated_payload.dict())
        return deepcopy(self._items[task_id])

    def delete(self, task_id: UUID) -> bool:
        return self._items.pop(task_id, None) is not None


task_repository = TaskRepository()


def create_task(payload: TaskCreate, *, owner_id: Optional[UUID] = None) -> TaskPublic:
    return task_repository.create(payload, owner_id)


def list_tasks(*, owner_id: Optional[UUID] = None) -> List[TaskPublic]:
    return task_repository.list(owner_id)


def get_task(task_id: UUID) -> Optional[TaskPublic]:
    return task_repository.get(task_id)


def delete_task(task_id: UUID) -> bool:
    return task_repository.delete(task_id)


def reset_repository() -> None:
    """Utility hook used exclusively in tests."""

    task_repository._items.clear()


