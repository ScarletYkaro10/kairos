from __future__ import annotations

from fastapi import FastAPI

from src.api.task_router import router as task_router
from src.api import auth_router
from src.core.database import init_db
# Importa os modelos para que sejam registrados no Base.metadata
from src.models import database  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kairos API",
        version="0.1.0",
        description="Core endpoints for tasks and schedule optimization.",
    )
    
    # Inicializa o banco de dados (cria as tabelas)
    # Os modelos devem ser importados antes de chamar init_db()
    init_db()
    
    app.include_router(task_router)
    app.include_router(auth_router.router)

    @app.get("/", tags=["health"])
    def root() -> dict[str, str]:
        """Simple health check for root path."""
        return {
            "status": "ok",
            "message": "Kairos API is running. See /docs for available endpoints.",
        }

    return app


app = create_app()
