"""Home view models."""
from datetime import datetime

from pydantic import BaseModel, Field


class HomeCreateRequest(BaseModel):
    """Home creation request."""

    name: str = Field(..., max_length=100)
    slogan: str | None = Field(None, max_length=255)
    cover_image: str | None = Field(None, max_length=500)
    theme: str = Field(default="default", max_length=50)
    is_private: bool = Field(default=False)


class HomeUpdateRequest(BaseModel):
    """Home update request."""

    name: str | None = Field(None, max_length=100)
    slogan: str | None = Field(None, max_length=255)
    cover_image: str | None = Field(None, max_length=500)
    theme: str | None = Field(None, max_length=50)
    is_private: bool | None = None


class HomeResponse(BaseModel):
    """Home response model."""

    id: int
    name: str
    slogan: str | None
    cover_image: str | None
    theme: str
    is_private: bool
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        orm_mode = True


class HomeListResponse(BaseModel):
    """Home list response model."""

    items: list[HomeResponse]
    total: int
