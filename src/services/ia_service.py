from __future__ import annotations

from datetime import datetime
from typing import Iterable, List

from src.models.schemas import TaskPriority, TaskPublic

PRIORITY_SCORES = {
    TaskPriority.high: 0,
    TaskPriority.medium: 1,
    TaskPriority.low: 2,
}


def optimize_schedule(tasks: Iterable[TaskPublic]) -> List[TaskPublic]:
    """Agendador mock usado na qualificacao (50%).

    A logica e deterministica e pronta para ser substituida pelo modelo de IA.
    Priorizamos primeiro e, em caso de empate, ordenamos pela data limite mais proxima.
    """

    def sort_key(task: TaskPublic) -> tuple[int, datetime]:
        due_date = task.due_date or datetime.max
        return PRIORITY_SCORES.get(task.priority, 3), due_date

    ordered_tasks = sorted(tasks, key=sort_key)
    return [task.copy() for task in ordered_tasks]


__all__ = ["optimize_schedule"]
