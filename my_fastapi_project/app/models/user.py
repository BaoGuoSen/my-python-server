"""User model."""
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from my_fastapi_project.app.models.database import Base


class User(Base):
    """User model for WeChat users."""

    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    open_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    nickname: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    homes: Mapped[list["Home"]] = relationship("Home", back_populates="owner")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
