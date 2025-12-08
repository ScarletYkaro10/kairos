from sqlalchemy import Column, String, DateTime, Enum as SQLEnum, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from ..core.database import Base
from .schemas import TaskPriority, TaskStatus


class User(Base):
    """Modelo de usuário no banco de dados."""

    __tablename__ = "users"

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relacionamento com tasks
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    """Modelo de tarefa no banco de dados."""

    __tablename__ = "tasks"

    id = Column(
        String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True
    )
    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority = Column(
        SQLEnum(TaskPriority, name="task_priority"),
        default=TaskPriority.medium,
        nullable=False,
    )
    status = Column(
        SQLEnum(TaskStatus, name="task_status"),
        default=TaskStatus.pending,
        nullable=False,
    )
    owner_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relacionamento com usuário
    owner = relationship("User", back_populates="tasks")

