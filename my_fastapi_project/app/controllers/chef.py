"""Chef controller."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.chef import Chef
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.home import Home
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.chef import ChefCreateRequest, ChefResponse, ChefUpdateRequest

router = APIRouter(tags=["chefs"])


@router.get("/homes/{home_id}/chefs", response_model=list[ChefResponse])
async def get_chefs(home_id: int, db: AsyncSession = Depends(get_db)) -> list[ChefResponse]:
    """Get all chefs for a home.

    Args:
        home_id: Home ID.
        db: Database session.

    Returns:
        list[ChefResponse]: List of chefs.

    """
    result = await db.execute(select(Chef).where(Chef.home_id == home_id))
    chefs = result.scalars().all()
    return [ChefResponse.from_orm(chef) for chef in chefs]


@router.post("/homes/{home_id}/chefs", response_model=ChefResponse)
async def create_chef(
    home_id: int,
    request: ChefCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChefResponse:
    """Create a new chef.

    Args:
        home_id: Home ID.
        request: Chef creation request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        ChefResponse: Created chef.

    Raises:
        HTTPException: If home not found or user is not owner.

    """
    result = await db.execute(select(Home).where(Home.id == home_id))
    home = result.scalar_one_or_none()
    if not home:
        raise HTTPException(status_code=404, content={"detail": "Home not found"})
    if home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    chef = Chef(
        home_id=home_id,
        name=request.name,
        avatar_url=request.avatar_url,
        is_friend=request.is_friend,
        bio=request.bio,
    )
    db.add(chef)
    await db.commit()
    await db.refresh(chef)
    return ChefResponse.from_orm(chef)


@router.post("/chefs/{chef_id}/update", response_model=ChefResponse)
async def update_chef(
    chef_id: int,
    request: ChefUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChefResponse:
    """Update chef information.

    Args:
        chef_id: Chef ID.
        request: Chef update request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        ChefResponse: Updated chef.

    Raises:
        HTTPException: If chef not found or user is not owner.

    """
    result = await db.execute(select(Chef).where(Chef.id == chef_id))
    chef = result.scalar_one_or_none()
    if not chef:
        raise HTTPException(status_code=404, content={"detail": "Chef not found"})

    home_result = await db.execute(select(Home).where(Home.id == chef.home_id))
    home = home_result.scalar_one_or_none()
    if not home or home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    if request.name is not None:
        chef.name = request.name
    if request.avatar_url is not None:
        chef.avatar_url = request.avatar_url
    if request.is_friend is not None:
        chef.is_friend = request.is_friend
    if request.bio is not None:
        chef.bio = request.bio

    await db.commit()
    await db.refresh(chef)
    return ChefResponse.from_orm(chef)


@router.post("/chefs/{chef_id}/delete")
async def delete_chef(
    chef_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a chef.

    Args:
        chef_id: Chef ID.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If chef not found or user is not owner.

    """
    result = await db.execute(select(Chef).where(Chef.id == chef_id))
    chef = result.scalar_one_or_none()
    if not chef:
        raise HTTPException(status_code=404, content={"detail": "Chef not found"})

    home_result = await db.execute(select(Home).where(Home.id == chef.home_id))
    home = home_result.scalar_one_or_none()
    if not home or home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    await db.delete(chef)
    await db.commit()
    return {"message": "Chef deleted successfully"}
