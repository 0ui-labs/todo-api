"""Admin-related schemas."""

from datetime import datetime

from pydantic import BaseModel, EmailStr


class LockedAccount(BaseModel):
    """Schema for locked account information."""

    email: EmailStr
    locked_until: datetime
    failed_attempts: int

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UnlockAccountRequest(BaseModel):
    """Request schema for unlocking an account."""

    email: EmailStr


class UnlockAccountResponse(BaseModel):
    """Response schema for unlock account operation."""

    success: bool
    message: str
