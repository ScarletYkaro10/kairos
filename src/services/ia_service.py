import joblib
import pandas as pd
import os
from typing import Iterable, List
from src.models.schemas import TaskPublic, TaskPriority

MODEL_PATH = "src/ia/kairos_model.pkl"
ENCODER_PATH = "src/ia/category_encoder.pkl"

_model = None
_encoder = None


def _load_ai_assets():
    """Carrega o modelo e o encoder se ainda não estiverem na memória."""
    global _model, _encoder
    if _model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            try:
                _model = joblib.load(MODEL_PATH)
                _encoder = joblib.load(ENCODER_PATH)
                print("✅ IA Kairós: Modelo carregado com sucesso.")
            except Exception as e:
                print(f"❌ Erro ao carregar modelo de IA: {e}")
        else:
            print(
                f"⚠️ AVISO: Arquivos do modelo não encontrados em {MODEL_PATH}. Usando lógica de fallback."
            )


def _predict_priority_score(task: TaskPublic) -> int:
    """
    Usa o modelo treinado para prever a prioridade.
    Retorno: 0 (Baixa), 1 (Média) ou 2 (Alta).
    """
    _load_ai_assets()

    if _model is None or _encoder is None:
        return 1

    try:
        days_until = 30
        if task.due_date:
            now = pd.Timestamp.now(tz=task.due_date.tzinfo)
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

    except Exception as e:
        print(f"⚠️ Erro na predição da tarefa '{task.title}': {e}")
        return 1


def optimize_schedule(tasks: Iterable[TaskPublic]) -> List[TaskPublic]:
    """
    Recebe a lista de tarefas, consulta a IA para cada uma e reordena.
    """
    tasks_with_scores = []

    for task in tasks:
        ai_score = _predict_priority_score(task)

        if ai_score == 2:
            task.priority = TaskPriority.high
        elif ai_score == 1:
            task.priority = TaskPriority.medium
        else:
            task.priority = TaskPriority.low

        tasks_with_scores.append((task, ai_score))

    ordered = sorted(
        tasks_with_scores,
        key=lambda x: (
            -x[1],
            x[0].due_date or pd.Timestamp.max.replace(tzinfo=x[0].created_at.tzinfo),
            x[0].estimated_minutes,
        ),
    )

    return [t[0].model_copy() for t in ordered]


__all__ = ["optimize_schedule"]
