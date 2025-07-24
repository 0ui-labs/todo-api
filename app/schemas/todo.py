"""Todo schemas for request/response validation."""
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import Field, field_validator

from app.models.todo import TodoStatus
from app.schemas.base import BaseSchema, PaginatedResponse, TimestampMixin
from app.schemas.category import CategoryResponse
from app.schemas.tag import TagResponse


class TodoBase(BaseSchema):
    """Base todo schema."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Todo title"
    )
    description: str | None = Field(
        None,
        max_length=1000,
        description="Todo description"
    )
    due_date: datetime | None = Field(
        None,
        description="Due date for the todo"
    )
    category_id: UUID | None = Field(
        None,
        description="Category ID"
    )


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""

    tag_ids: List[UUID] = Field(default_factory=list, description="List of tag IDs")

    @field_validator("due_date")
    @classmethod
    def validate_due_date(cls, v: datetime | None) -> datetime | None:
        """Validate that due date is in the future."""
        if v and v < datetime.now(v.tzinfo):
            raise ValueError("Due date must be in the future")
        return v


class TodoUpdate(BaseSchema):
    """Schema for updating a todo."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    status: TodoStatus | None = Field(None)
    due_date: datetime | None = Field(None)
    category_id: UUID | None = Field(None)
    completed_at: datetime | None = Field(None)
    tag_ids: List[UUID] | None = Field(None, description="List of tag IDs")

    @field_validator("status")
    @classmethod
    def validate_completed_at(cls, v: TodoStatus | None, info) -> TodoStatus | None:
        """Set completed_at when status is set to completed."""
        if v == TodoStatus.COMPLETED and "completed_at" not in info.data:
            info.data["completed_at"] = datetime.now()
        return v


class TodoResponse(TodoBase, TimestampMixin):
    """Schema for todo response."""

    id: UUID = Field(..., description="Todo ID")
    user_id: UUID = Field(..., description="Owner user ID")
    status: TodoStatus = Field(..., description="Todo status")
    completed_at: datetime | None = Field(None, description="Completion timestamp")
    category: CategoryResponse | None = Field(None, description="Category details")
    tags: List[TagResponse] = Field(default_factory=list, description="Associated tags")

    model_config = BaseSchema.model_config.copy()
    model_config["json_schema_extra"] = {
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174002",
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "title": "Complete project documentation",
            "description": "Write comprehensive API documentation",
            "status": "open",
            "due_date": "2024-01-20T15:00:00Z",
            "completed_at": None,
            "category_id": "123e4567-e89b-12d3-a456-426614174001",
            "category": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "name": "Work",
                "color": "#FF5733"
            },
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z"
        }
    }


class TodoListResponse(PaginatedResponse):
    """Schema for paginated todo list response."""

    items: list[TodoResponse] = Field(..., description="List of todos")

    model_config = BaseSchema.model_config.copy()
    model_config["json_schema_extra"] = {
        "example": {
            "items": [TodoResponse.model_config["json_schema_extra"]["example"]],
            "total": 42,
            "limit": 20,
            "offset": 0
        }
    }


class TodoFilter(BaseSchema):
    """Schema for todo filtering."""

    status: TodoStatus | None = Field(None, description="Filter by status")
    category_id: UUID | None = Field(None, description="Filter by category")
    search: str | None = Field(None, description="Search in title and description")

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, v: str | TodoStatus | None) -> TodoStatus | None:
        """Normalize status string to TodoStatus enum (case-insensitive)."""
        if v is None or isinstance(v, TodoStatus):
            return v
        if isinstance(v, str):
            # Normalize string to match enum values
            normalized = v.lower().replace("_", " ").replace(" ", "_")
            try:
                return TodoStatus(normalized)
            except ValueError:
                # Let Pydantic handle the validation error
                return v
        return v


class TodoSort(BaseSchema):
    """Schema for todo sorting."""

    sort_by: str = Field(
        default="created_at",
        pattern="^(created_at|due_date|title|updated_at)$",
        description="Field to sort by"
    )
    order: str = Field(
        default="desc",
        pattern="^(asc|desc)$",
        description="Sort order"
    )

