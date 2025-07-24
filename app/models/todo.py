"""Todo model definition."""
import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.tag import Tag
    from app.models.user import User


class TodoStatus(str, enum.Enum):
    """Todo status enum."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Todo(Base):
    """Todo model for task management."""

    __tablename__ = "todos"
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_due_date", "due_date"),
        Index("idx_category_id", "category_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[TodoStatus] = mapped_column(
        Enum(
            TodoStatus,
            values_callable=lambda x: [e.value for e in x],
            native_enum=False
        ),
        default=TodoStatus.OPEN,
        nullable=False,
    )
    due_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="todos",
    )
    category: Mapped[Optional["Category"]] = relationship(
        "Category",
        back_populates="todos",
    )
    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="todo_tags",
        back_populates="todos",
    )

    def __repr__(self) -> str:
        """String representation of the todo."""
        return f"<Todo(id={self.id}, title={self.title}, status={self.status})>"

