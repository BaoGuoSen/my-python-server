"""Home controller."""
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.home import Home
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.home import (
    HomeCreateRequest,
    HomeListResponse,
    HomeResponse,
    HomeUpdateRequest,
)

router = APIRouter(prefix="/homes", tags=["homes"])


@router.get(
    "",
    response_model=HomeListResponse,
    dependencies=[Depends(get_current_user)],
)
async def get_homes(db: AsyncSession = Depends(get_db)) -> HomeListResponse:
    """List all homes (no server-side privacy filter; UI may hide by is_private).

    Args:
        db: Database session.

    Returns:
        HomeListResponse: All homes, newest first.

    """
    count_result = await db.execute(select(func.count()).select_from(Home))
    total = count_result.scalar_one()

    result = await db.execute(select(Home).order_by(Home.created_at.desc()))
    homes = result.scalars().all()

    return HomeListResponse(
        items=[HomeResponse.from_orm(home) for home in homes],
        total=total,
    )


@router.post("", response_model=HomeResponse)
async def create_home(
    request: HomeCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> HomeResponse:
    """Create a new home.

    Args:
        request: Home creation request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        HomeResponse: Created home.

    """
    home = Home(
        name=request.name,
        slogan=request.slogan,
        cover_image=request.cover_image,
        theme=request.theme,
        is_private=request.is_private,
        owner_id=current_user.id,
    )
    db.add(home)
    await db.commit()
    await db.refresh(home)
    return HomeResponse.from_orm(home)


@router.get("/{home_id}", response_model=HomeResponse)
async def get_home(home_id: int, db: AsyncSession = Depends(get_db)) -> HomeResponse:
    """Get home by ID (no server-side privacy filter).

    Args:
        home_id: Home ID.
        db: Database session.

    Returns:
        HomeResponse: Home information.

    Raises:
        HTTPException: If home not found.

    """
    result = await db.execute(select(Home).where(Home.id == home_id))
    home = result.scalar_one_or_none()
    if not home:
        raise HTTPException(status_code=404, content={"detail": "Home not found"})
    return HomeResponse.from_orm(home)


@router.post("/{home_id}/update", response_model=HomeResponse)
async def update_home(
    home_id: int,
    request: HomeUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> HomeResponse:
    """Update home information.

    Args:
        home_id: Home ID.
        request: Home update request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        HomeResponse: Updated home.

    Raises:
        HTTPException: If home not found or user is not owner.

    """
    result = await db.execute(select(Home).where(Home.id == home_id))
    home = result.scalar_one_or_none()
    if not home:
        raise HTTPException(status_code=404, content={"detail": "Home not found"})
    if home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    if request.name is not None:
        home.name = request.name
    if request.slogan is not None:
        home.slogan = request.slogan
    if request.cover_image is not None:
        home.cover_image = request.cover_image
    if request.theme is not None:
        home.theme = request.theme
    if request.is_private is not None:
        home.is_private = request.is_private

    await db.commit()
    await db.refresh(home)
    return HomeResponse.from_orm(home)
