from __future__ import annotations
from copy import deepcopy
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import UUID
from src.models.schemas import TaskCreate, TaskPublic, TaskStatus


class TaskRepository:
    """Simple in-memory storage."""

    def __init__(self) -> None:
        self._items: Dict[UUID, TaskPublic] = {}

    def create(self, data: TaskCreate, owner_id: Optional[UUID] = None) -> TaskPublic:
        owner_id_str = str(owner_id) if owner_id else None
        task = TaskPublic(**data.model_dump(), owner_id=owner_id_str)
        self._items[task.id] = task
        return deepcopy(task)

    def list(self, owner_id: Optional[UUID] = None) -> List[TaskPublic]:
        tasks = self._items.values()
        if owner_id is not None:
            owner_id_str = str(owner_id)
            tasks = [task for task in tasks if str(task.owner_id) == owner_id_str]
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

        updated_payload = task.copy(update=data.model_dump(exclude_unset=True))
        if status:
            updated_payload.status = status
        updated_payload.updated_at = datetime.now(timezone.utc)
        self._items[task_id] = TaskPublic(**updated_payload.model_dump())
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
    task_repository._items.clear()
