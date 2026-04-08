"""Dish and DishImage models."""
from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.app.models.database import Base


class Dish(Base):
    """Dish model representing a food item."""

    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    home_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("home.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    chef_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("chef.id"), nullable=False, index=True)
    avg_rating: Mapped[Decimal] = mapped_column(Numeric(3, 2), default=Decimal("0.00"), nullable=False)
    review_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    home: Mapped["Home"] = relationship("Home", back_populates="dishes")
    chef: Mapped["Chef"] = relationship("Chef", back_populates="dishes")
    images: Mapped[list["DishImage"]] = relationship("DishImage", back_populates="dish", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="dish", cascade="all, delete-orphan")


class DishImage(Base):
    """DishImage model for dish photos."""

    __tablename__ = "dish_image"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dish_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("dish.id"), nullable=False, index=True)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    dish: Mapped["Dish"] = relationship("Dish", back_populates="images")
