"""Pydantic schemas for request/response validation."""
from app.schemas.base import (
    BaseSchema,
    ErrorResponse,
    PaginatedResponse,
    PaginationParams,
    TimestampMixin,
)
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.tag import TagCreate, TagResponse, TagUpdate
from app.schemas.todo import (
    TodoCreate,
    TodoFilter,
    TodoListResponse,
    TodoResponse,
    TodoSort,
    TodoUpdate,
)
from app.schemas.user import (
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
    UserUpdate,
)

__all__ = [
    # Base
    "BaseSchema",
    "ErrorResponse",
    "PaginatedResponse",
    "PaginationParams",
    "TimestampMixin",
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "TokenResponse",
    # Category
    "CategoryCreate",
    "CategoryUpdate",
    "CategoryResponse",
    # Todo
    "TodoCreate",
    "TodoUpdate",
    "TodoResponse",
    "TodoListResponse",
    "TodoFilter",
    "TodoSort",
    # Tag
    "TagCreate",
    "TagUpdate",
    "TagResponse",
]
