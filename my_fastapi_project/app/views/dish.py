"""Dish view models."""
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class DishImageResponse(BaseModel):
    """Dish image response model."""

    id: int
    url: str
    sort_order: int

    class Config:
        """Pydantic config."""

        orm_mode = True


class DishCreateRequest(BaseModel):
    """Dish creation request."""

    name: str = Field(..., max_length=100)
    description: str | None = None
    category: str = Field(..., max_length=20)
    chef_id: int
    image_urls: list[str] = Field(default_factory=list)


class DishUpdateRequest(BaseModel):
    """Dish update request."""

    name: str | None = Field(None, max_length=100)
    description: str | None = None
    category: str | None = Field(None, max_length=20)
    chef_id: int | None = None
    image_urls: list[str] | None = None


class DishResponse(BaseModel):
    """Dish response model."""

    id: int
    home_id: int
    name: str
    description: str | None
    category: str
    chef_id: int
    avg_rating: Decimal
    review_count: int
    created_at: datetime
    updated_at: datetime
    images: list[DishImageResponse] = []

    class Config:
        """Pydantic config."""

        orm_mode = True


class DishListResponse(BaseModel):
    """Dish list response with pagination."""

    items: list[DishResponse]
    total: int
    page: int
    page_size: int
