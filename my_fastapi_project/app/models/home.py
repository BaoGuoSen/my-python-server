"""Home model."""
from datetime import datetime

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.app.models.database import Base
from my_fastapi_project.app.utils.wall_clock import shanghai_now


class Home(Base):
    """Home model representing a family."""

    __tablename__ = "home"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slogan: Mapped[str] = mapped_column(String(255), nullable=True)
    cover_image: Mapped[str] = mapped_column(String(500), nullable=True)
    theme: Mapped[str] = mapped_column(String(50), default="default", nullable=False)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("user.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=shanghai_now, onupdate=shanghai_now, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="homes")
    chefs: Mapped[list["Chef"]] = relationship("Chef", back_populates="home", cascade="all, delete-orphan")
    dishes: Mapped[list["Dish"]] = relationship("Dish", back_populates="home", cascade="all, delete-orphan")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="home", cascade="all, delete-orphan")
