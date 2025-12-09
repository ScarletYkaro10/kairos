from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.models.schemas import TaskCreate, TaskPublic
from src.services import ia_service, task_service
from src.api.deps import get_current_user_id
from src.core.database import get_db

router = APIRouter(tags=["tasks"])


class OptimizeScheduleRequest(BaseModel):
    tasks: Optional[List[TaskPublic]] = None


@router.post(
    "/tasks",
    response_model=TaskPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
def create_task_endpoint(
    payload: TaskCreate,
    user_id=Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> TaskPublic:
    return task_service.create_task(payload, db, owner_id=user_id)


@router.get(
    "/tasks",
    response_model=List[TaskPublic],
    summary="List tasks for the authenticated user",
)
def list_tasks_endpoint(
    user_id=Depends(get_current_user_id), db: Session = Depends(get_db)
) -> List[TaskPublic]:
    return task_service.list_tasks(db, owner_id=user_id)


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
def delete_task_endpoint(
    task_id: UUID,
    user_id=Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    success = task_service.delete_task(db, task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return None


@router.post("/optimize-schedule", response_model=List[TaskPublic])
def optimize_schedule_endpoint(
    request: OptimizeScheduleRequest | None = None,
    user_id=Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> List[TaskPublic]:
    tasks = (
        request.tasks
        if request and request.tasks
        else task_service.list_tasks(db, owner_id=user_id)
    )

    return ia_service.optimize_schedule(tasks, db)


__all__ = ["router"]
