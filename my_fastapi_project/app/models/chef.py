"""Chef model."""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.app.models.database import Base
from my_fastapi_project.app.utils.wall_clock import shanghai_now


class Chef(Base):
    """Chef model representing a cook in a home."""

    __tablename__ = "chef"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    home_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("home.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_friend: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, onupdate=shanghai_now, nullable=False)

    home: Mapped["Home"] = relationship("Home", back_populates="chefs")
    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="chef")
