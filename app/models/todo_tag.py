"""Association table for many-to-many relationship between todos and tags."""


from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base

# Association table for many-to-many relationship
todo_tags = Table(
    "todo_tags",
    Base.metadata,
    Column(
        "todo_id",
        UUID(as_uuid=True),
        ForeignKey("todos.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
    Column(
        "tag_id",
        UUID(as_uuid=True),
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    ),
)
