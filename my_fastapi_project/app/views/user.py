"""User view models."""
from datetime import datetime

from pydantic import BaseModel, Field


class UserResponse(BaseModel):
    """User response model."""

    id: int
    open_id: str
    nickname: str
    avatar_url: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        orm_mode = True


class UserUpdateRequest(BaseModel):
    """User update request."""

    nickname: str | None = Field(None, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)
