import joblib
import pandas as pd
import os
from datetime import datetime, timezone
from typing import Iterable, List
from sqlalchemy.orm import Session
from src.models.schemas import TaskPublic, TaskPriority
from src.models.database import Task

MODEL_PATH = "src/ia/kairos_model.pkl"
ENCODER_PATH = "src/ia/category_encoder.pkl"

_model = None
_encoder = None


def _load_ai_assets():
    global _model, _encoder
    if _model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            try:
                _model = joblib.load(MODEL_PATH)
                _encoder = joblib.load(ENCODER_PATH)
            except:
                pass


def _predict_priority_score(task: TaskPublic) -> int:
    _load_ai_assets()
    if _model is None or _encoder is None:
        return 1

    try:
        days_until = 30
        if task.due_date:
            if task.due_date.tzinfo:
                now = datetime.now(timezone.utc)
            else:
                now = datetime.utcnow()
            delta = task.due_date - now
            days_until = max(0, delta.days)

        cat_encoded = _encoder.transform([task.category.value])[0]

        features = pd.DataFrame(
            [
                {
                    "days_until_due": days_until,
                    "estimated_minutes": task.estimated_minutes,
                    "difficulty": task.difficulty,
                    "category_encoded": cat_encoded,
                }
            ]
        )

        prediction = _model.predict(features)[0]
        return int(prediction)
    except:
        return 1


def optimize_schedule(tasks: Iterable[TaskPublic], db: Session) -> List[TaskPublic]:
    tasks_with_scores = []

    for task_schema in tasks:
        ai_score = _predict_priority_score(task_schema)

        new_priority = TaskPriority.medium
        if ai_score == 2:
            new_priority = TaskPriority.high
        elif ai_score == 0:
            new_priority = TaskPriority.low

        task_schema.priority = new_priority

        db_task = db.query(Task).filter(Task.id == str(task_schema.id)).first()
        if db_task:
            db_task.priority = new_priority
            db.add(db_task)

        tasks_with_scores.append((task_schema, ai_score))

    db.commit()

    ordered = sorted(
        tasks_with_scores,
        key=lambda x: (
            -x[1],
            x[0].due_date or datetime.max.replace(tzinfo=timezone.utc),
            x[0].estimated_minutes,
        ),
    )

    return [t[0].model_copy() for t in ordered]
