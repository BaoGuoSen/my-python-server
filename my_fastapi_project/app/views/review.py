"""Review view models."""
from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreateRequest(BaseModel):
    """Review creation request."""

    rating: int = Field(..., ge=1, le=5)
    content: str | None = None


class ReviewResponse(BaseModel):
    """Review response model."""

    id: int
    dish_id: int
    user_id: int
    rating: int
    content: str | None
    like_count: int
    created_at: datetime
    updated_at: datetime
    user_nickname: str | None = None
    user_avatar_url: str | None = None

    class Config:
        """Pydantic config."""

        orm_mode = True


class ReviewListResponse(BaseModel):
    """Review list response with pagination."""

    items: list[ReviewResponse]
    total: int
    page: int
    page_size: int
