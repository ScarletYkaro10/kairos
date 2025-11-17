from __future__ import annotations

from fastapi import FastAPI

from src.api.task_router import router as task_router
from src.api import auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Kairos API",
        version="0.1.0",
        description="Core endpoints for tasks and schedule optimization.",
    )
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
