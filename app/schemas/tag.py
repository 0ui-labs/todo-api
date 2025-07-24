"""Tag schemas for API validation."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class TagBase(BaseModel):
    """Base schema for tag."""

    name: str = Field(..., min_length=1, max_length=50, description="Tag name")
    color: Optional[str] = Field(
        None,
        regex="^#[0-9A-Fa-f]{6}$",
        description="Hex color code (e.g., #FF5733)",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate and clean tag name."""
        return v.strip()


class TagCreate(TagBase):
    """Schema for creating a tag."""

    pass


class TagUpdate(BaseModel):
    """Schema for updating a tag."""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, regex="^#[0-9A-Fa-f]{6}$")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Validate and clean tag name if provided."""
        return v.strip() if v else v


class TagResponse(TagBase):
    """Schema for tag response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}