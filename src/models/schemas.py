from __future__ import annotations
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)


class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    done = "done"


class TaskCategory(str, Enum):
    TRABALHO = "Trabalho"
    ESTUDO = "Estudo"
    SAUDE = "Saúde"
    LAZER = "Lazer"
    CASA = "Casa"
    PROJETOS = "Projetos"
    FINANCAS = "Finanças"


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: Optional[str] = Field(None, max_length=1024)

    due_date: Optional[datetime] = Field(
        None, description="Deadline for completing the task"
    )

    category: TaskCategory = Field(
        default=TaskCategory.TRABALHO,
        description="Categoria para a IA analisar a importância",
    )
    difficulty: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Nível de dificuldade de 1 (Fácil) a 5 (Difícil)",
    )
    estimated_minutes: int = Field(
        default=60, ge=1, description="Tempo estimado em minutos"
    )

    priority: TaskPriority = Field(default=TaskPriority.medium)
    status: TaskStatus = Field(default=TaskStatus.pending)

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Evita datas muito antigas."""
        if value is not None:
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            if value < datetime.now(timezone.utc) - timedelta(days=1):
                raise ValueError("due_date cannot be in the distant past")
        return value


class TaskCreate(TaskBase):
    pass


class TaskPublic(TaskBase):
    """Schema returned by the API and persisted in the task service."""

    id: UUID = Field(default_factory=uuid4)
    owner_id: Optional[UUID] = Field(
        default=None, description="User that owns the task"
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "UserCreate",
    "UserPublic",
    "Token",
    "TokenData",
    "TaskPriority",
    "TaskStatus",
    "TaskCategory",
    "TaskCreate",
    "TaskPublic",
]
