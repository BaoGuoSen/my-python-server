"""Dish controller."""
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.dish import Dish, DishImage
from my_fastapi_project.app.models.home import Home
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.dish import DishCreateRequest, DishListResponse, DishResponse, DishUpdateRequest

router = APIRouter(tags=["dishes"])


@router.get("/homes/{home_id}/dishes", response_model=DishListResponse)
async def get_dishes(
    home_id: int,
    category: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> DishListResponse:
    """Get dishes for a home with pagination.

    Args:
        home_id: Home ID.
        category: Optional category filter.
        page: Page number.
        page_size: Items per page.
        db: Database session.

    Returns:
        DishListResponse: Paginated dish list; most recently updated first.

    """
    query = select(Dish).where(Dish.home_id == home_id).options(selectinload(Dish.images))
    if category:
        query = query.where(Dish.category == category)

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    query = (
        query.order_by(Dish.updated_at.desc(), Dish.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    dishes = result.scalars().all()

    return DishListResponse(
        items=[DishResponse.from_orm(dish) for dish in dishes],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/homes/{home_id}/dishes", response_model=DishResponse)
async def create_dish(
    home_id: int,
    request: DishCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DishResponse:
    """Create a new dish.

    Args:
        home_id: Home ID.
        request: Dish creation request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        DishResponse: Created dish.

    Raises:
        HTTPException: If home not found or user is not owner.

    """
    result = await db.execute(select(Home).where(Home.id == home_id))
    home = result.scalar_one_or_none()
    if not home:
        raise HTTPException(status_code=404, content={"detail": "Home not found"})
    if home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    dish = Dish(
        home_id=home_id,
        name=request.name,
        description=request.description,
        category=request.category,
        chef_id=request.chef_id,
    )
    db.add(dish)
    await db.flush()

    for idx, url in enumerate(request.image_urls):
        image = DishImage(dish_id=dish.id, url=url, sort_order=idx)
        db.add(image)

    await db.commit()
    await db.refresh(dish, ["images"])
    return DishResponse.from_orm(dish)


@router.get("/dishes/{dish_id}", response_model=DishResponse)
async def get_dish(dish_id: int, db: AsyncSession = Depends(get_db)) -> DishResponse:
    """Get dish by ID.

    Args:
        dish_id: Dish ID.
        db: Database session.

    Returns:
        DishResponse: Dish information.

    Raises:
        HTTPException: If dish not found.

    """
    result = await db.execute(select(Dish).where(Dish.id == dish_id).options(selectinload(Dish.images)))
    dish = result.scalar_one_or_none()
    if not dish:
        raise HTTPException(status_code=404, content={"detail": "Dish not found"})
    return DishResponse.from_orm(dish)


@router.post("/dishes/{dish_id}/update", response_model=DishResponse)
async def update_dish(
    dish_id: int,
    request: DishUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> DishResponse:
    """Update dish information.

    Args:
        dish_id: Dish ID.
        request: Dish update request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        DishResponse: Updated dish.

    Raises:
        HTTPException: If dish not found or user is not owner.

    """
    result = await db.execute(select(Dish).where(Dish.id == dish_id).options(selectinload(Dish.images)))
    dish = result.scalar_one_or_none()
    if not dish:
        raise HTTPException(status_code=404, content={"detail": "Dish not found"})

    home_result = await db.execute(select(Home).where(Home.id == dish.home_id))
    home = home_result.scalar_one_or_none()
    if not home or home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    if request.name is not None:
        dish.name = request.name
    if request.description is not None:
        dish.description = request.description
    if request.category is not None:
        dish.category = request.category
    if request.chef_id is not None:
        dish.chef_id = request.chef_id

    if request.image_urls is not None:
        await db.execute(select(DishImage).where(DishImage.dish_id == dish_id))
        for img in dish.images:
            await db.delete(img)
        for idx, url in enumerate(request.image_urls):
            image = DishImage(dish_id=dish.id, url=url, sort_order=idx)
            db.add(image)

    await db.commit()
    await db.refresh(dish, ["images"])
    return DishResponse.from_orm(dish)


@router.post("/dishes/{dish_id}/delete")
async def delete_dish(
    dish_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    """Delete a dish.

    Args:
        dish_id: Dish ID.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        dict: Success message.

    Raises:
        HTTPException: If dish not found or user is not owner.

    """
    result = await db.execute(select(Dish).where(Dish.id == dish_id))
    dish = result.scalar_one_or_none()
    if not dish:
        raise HTTPException(status_code=404, content={"detail": "Dish not found"})

    home_result = await db.execute(select(Home).where(Home.id == dish.home_id))
    home = home_result.scalar_one_or_none()
    if not home or home.owner_id != current_user.id:
        raise HTTPException(status_code=403, content={"detail": "Not authorized"})

    await db.delete(dish)
    await db.commit()
    return {"message": "Dish deleted successfully"}
