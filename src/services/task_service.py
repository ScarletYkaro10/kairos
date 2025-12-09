from __future__ import annotations
from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from src.models.schemas import TaskCreate, TaskPublic, TaskStatus
from src.models.database import Task


def _task_db_to_schema(db_task: Task) -> TaskPublic:
    """Converte um modelo Task do banco para o schema TaskPublic."""
    return TaskPublic(
        id=UUID(db_task.id),
        title=db_task.title,
        description=db_task.description,
        due_date=db_task.due_date,
        priority=db_task.priority,
        status=db_task.status,
        category=db_task.category,
        difficulty=db_task.difficulty,
        estimated_minutes=db_task.estimated_minutes,
        owner_id=UUID(db_task.owner_id) if db_task.owner_id else None,
        created_at=db_task.created_at,
        updated_at=db_task.updated_at,
    )


def create_task(
    payload: TaskCreate, db: Session, *, owner_id: Optional[str] = None
) -> TaskPublic:
    """Cria uma nova tarefa no banco de dados."""
    db_task = Task(
        title=payload.title,
        description=payload.description,
        due_date=payload.due_date,
        priority=payload.priority,
        status=payload.status,
        category=payload.category,
        difficulty=payload.difficulty,
        estimated_minutes=payload.estimated_minutes,
        owner_id=owner_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return _task_db_to_schema(db_task)


def list_tasks(db: Session, *, owner_id: Optional[str] = None) -> List[TaskPublic]:
    """Lista tarefas, opcionalmente filtradas por owner_id."""
    query = db.query(Task)
    if owner_id is not None:
        query = query.filter(Task.owner_id == owner_id)
    db_tasks = query.all()
    return [_task_db_to_schema(task) for task in db_tasks]


def get_task(db: Session, task_id: UUID) -> Optional[TaskPublic]:
    """Busca uma tarefa pelo ID."""
    db_task = db.query(Task).filter(Task.id == str(task_id)).first()
    if db_task is None:
        return None
    return _task_db_to_schema(db_task)


def update_task(
    db: Session,
    task_id: UUID,
    data: TaskCreate,
    *,
    status: Optional[TaskStatus] = None,
) -> Optional[TaskPublic]:
    """Atualiza uma tarefa existente."""
    db_task = db.query(Task).filter(Task.id == str(task_id)).first()
    if db_task is None:
        return None

    if data.title is not None:
        db_task.title = data.title
    if data.description is not None:
        db_task.description = data.description
    if data.due_date is not None:
        db_task.due_date = data.due_date
    if data.priority is not None:
        db_task.priority = data.priority

    if data.category is not None:
        db_task.category = data.category
    if data.difficulty is not None:
        db_task.difficulty = data.difficulty
    if data.estimated_minutes is not None:
        db_task.estimated_minutes = data.estimated_minutes

    if status is not None:
        db_task.status = status

    db_task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(db_task)
    return _task_db_to_schema(db_task)


def delete_task(db: Session, task_id: UUID) -> bool:
    """Deleta uma tarefa do banco de dados."""
    db_task = db.query(Task).filter(Task.id == str(task_id)).first()
    if db_task is None:
        return False
    db.delete(db_task)
    db.commit()
    return True
