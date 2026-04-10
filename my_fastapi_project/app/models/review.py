"""Review model."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, SmallInteger, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.app.models.database import Base
from my_fastapi_project.app.utils.wall_clock import shanghai_now


class Review(Base):
    """Review model for dish ratings and comments."""

    __tablename__ = "review"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    dish_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("dish.id"), nullable=False, index=True)
    home_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("home.id"), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id"), nullable=False, index=True)
    rating: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    like_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, onupdate=shanghai_now, nullable=False)

    dish: Mapped["Dish"] = relationship("Dish", back_populates="reviews")
    home: Mapped["Home"] = relationship("Home", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")
