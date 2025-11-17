from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from src.models.schemas import TaskCreate, TaskPublic
from src.services import ia_service, task_service
from src.api.deps import get_current_user_id

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
) -> TaskPublic:
    return task_service.create_task(payload, owner_id=user_id)


@router.get(
    "/tasks",
    response_model=List[TaskPublic],
    summary="List tasks for the authenticated user",
)
def list_tasks_endpoint(user_id=Depends(get_current_user_id)) -> List[TaskPublic]:
    return task_service.list_tasks(owner_id=user_id)


@router.post(
    "/optimize-schedule",
    response_model=List[TaskPublic],
    summary="Mock IA endpoint used during the 50% milestone",
)
def optimize_schedule_endpoint(
    request: OptimizeScheduleRequest | None = None,
    user_id=Depends(get_current_user_id),
) -> List[TaskPublic]:
    tasks = (
        request.tasks
        if request and request.tasks
        else task_service.list_tasks(owner_id=user_id)
    )
    return ia_service.optimize_schedule(tasks)


__all__ = ["router"]
