"""Chef view models."""
from datetime import datetime

from pydantic import BaseModel, Field


class ChefCreateRequest(BaseModel):
    """Chef creation request."""

    name: str = Field(..., max_length=100)
    avatar_url: str = Field(..., max_length=500)
    is_friend: bool = Field(default=False)
    bio: str | None = Field(None, max_length=500)


class ChefUpdateRequest(BaseModel):
    """Chef update request."""

    name: str | None = Field(None, max_length=100)
    avatar_url: str | None = Field(None, max_length=500)
    is_friend: bool | None = None
    bio: str | None = Field(None, max_length=500)


class ChefResponse(BaseModel):
    """Chef response model."""

    id: int
    home_id: int
    name: str
    avatar_url: str
    is_friend: bool
    bio: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        orm_mode = True
