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
    id: str
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


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120)
    description: Optional[str] = Field(None, max_length=1024)
    due_date: Optional[datetime] = Field(
        None, description="Deadline for completing the task"
    )
    priority: TaskPriority = Field(default=TaskPriority.medium)
    status: TaskStatus = Field(default=TaskStatus.pending)

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, value: Optional[datetime]) -> Optional[datetime]:
        """Avoid obviously invalid deadlines."""
        if value is not None:
            if value.tzinfo is None:
                value = value.replace(tzinfo=timezone.utc)
            if value < datetime.now(timezone.utc) - timedelta(days=1):
                raise ValueError("due_date cannot be in the distant past")
        return value


class TaskCreate(TaskBase):
    """Schema used when creating tasks via the API."""

    pass


class TaskPublic(TaskBase):
    """Schema returned by the API."""

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
    "TaskCreate",
    "TaskPublic",
]
