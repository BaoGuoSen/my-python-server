"""Application implementation - database engine and session."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from my_fastapi_project.config import settings


engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


async def get_db() -> AsyncSession:
    """Provide a database session for each request.

    Yields:
        AsyncSession: SQLAlchemy async session.

    """
    async with AsyncSessionLocal() as session:
        yield session
