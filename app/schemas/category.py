"""Category schemas for request/response validation."""
from datetime import datetime
from uuid import UUID

from pydantic import Field

from app.schemas.base import BaseSchema, PaginatedResponse


class CategoryBase(BaseSchema):
    """Base category schema."""

    name: str = Field(..., min_length=1, max_length=50, description="Category name")
    color: str = Field(
        default="#000000",
        pattern=r"^#[0-9A-Fa-f]{6}$",
        description="Category color in hex format"
    )


class CategoryCreate(CategoryBase):
    """Schema for creating a new category."""

    pass


class CategoryUpdate(BaseSchema):
    """Schema for updating a category."""

    name: str | None = Field(None, min_length=1, max_length=50)
    color: str | None = Field(None, pattern=r"^#[0-9A-Fa-f]{6}$")


class CategoryResponse(CategoryBase):
    """Schema for category response."""

    id: UUID = Field(..., description="Category ID")
    user_id: UUID = Field(..., description="Owner user ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = BaseSchema.model_config.copy()
    model_config["json_schema_extra"] = {
        "example": {
            "id": "123e4567-e89b-12d3-a456-426614174001",
            "user_id": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Work",
            "color": "#FF5733",
            "created_at": "2024-01-01T00:00:00Z"
        }
    }


class CategoryListResponse(PaginatedResponse):
    """Schema for paginated category list response."""

    items: list[CategoryResponse] = Field(..., description="List of categories")

    model_config = BaseSchema.model_config.copy()
    model_config["json_schema_extra"] = {
        "example": {
            "items": [CategoryResponse.model_config["json_schema_extra"]["example"]],
            "total": 10,
            "limit": 20,
            "offset": 0
        }
    }
