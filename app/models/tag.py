"""Tag model for categorizing todos."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.todo import Todo


class Tag(Base):
    """Tag model for categorizing todos with many-to-many relationship."""

    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    color: Mapped[str | None] = mapped_column(
        String(7),  # For hex color codes like #FF5733
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

    # Relationships
    todos: Mapped[List["Todo"]] = relationship(
        "Todo",
        secondary="todo_tags",
        back_populates="tags",
    )

    def __repr__(self) -> str:
        """String representation of the tag."""
        return f"<Tag(id={self.id}, name={self.name})>"