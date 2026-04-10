"""Review controller."""
from decimal import Decimal

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.dish import Dish
from my_fastapi_project.app.models.review import Review
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.review import ReviewCreateRequest, ReviewListResponse, ReviewResponse

router = APIRouter(tags=["reviews"])


@router.get("/dishes/{dish_id}/reviews", response_model=ReviewListResponse)
async def get_reviews(
    dish_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> ReviewListResponse:
    """Get reviews for a dish with pagination.

    Args:
        dish_id: Dish ID.
        page: Page number.
        page_size: Items per page.
        db: Database session.

    Returns:
        ReviewListResponse: Paginated review list; most recently updated first.

    """
    query = select(Review).where(Review.dish_id == dish_id)
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    query = (
        query.order_by(Review.updated_at.desc(), Review.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(query)
    reviews = result.scalars().all()

    review_responses = []
    for review in reviews:
        user_result = await db.execute(select(User).where(User.id == review.user_id))
        user = user_result.scalar_one_or_none()
        review_dict = ReviewResponse.from_orm(review).dict()
        if user:
            review_dict["user_nickname"] = user.nickname
            review_dict["user_avatar_url"] = user.avatar_url
        review_responses.append(ReviewResponse(**review_dict))

    return ReviewListResponse(items=review_responses, total=total, page=page, page_size=page_size)


@router.post("/dishes/{dish_id}/reviews", response_model=ReviewResponse)
async def create_review(
    dish_id: int,
    request: ReviewCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ReviewResponse:
    """Create a new review for a dish.

    Args:
        dish_id: Dish ID.
        request: Review creation request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        ReviewResponse: Created review.

    Raises:
        HTTPException: If dish not found.

    """
    result = await db.execute(select(Dish).where(Dish.id == dish_id))
    dish = result.scalar_one_or_none()
    if not dish:
        raise HTTPException(status_code=404, content={"detail": "Dish not found"})

    review = Review(
        dish_id=dish_id,
        home_id=dish.home_id,
        user_id=current_user.id,
        rating=request.rating,
        content=request.content,
    )
    db.add(review)

    reviews_result = await db.execute(select(Review).where(Review.dish_id == dish_id))
    all_reviews = reviews_result.scalars().all()
    total_rating = sum(r.rating for r in all_reviews) + request.rating
    new_count = len(all_reviews) + 1
    dish.avg_rating = Decimal(str(total_rating / new_count))
    dish.review_count = new_count

    await db.commit()
    await db.refresh(review)

    review_dict = ReviewResponse.from_orm(review).dict()
    review_dict["user_nickname"] = current_user.nickname
    review_dict["user_avatar_url"] = current_user.avatar_url
    return ReviewResponse(**review_dict)


@router.post("/reviews/{review_id}/like")
async def like_review(review_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    """Like a review.

    Args:
        review_id: Review ID.
        db: Database session.

    Returns:
        dict: Success message with new like count.

    Raises:
        HTTPException: If review not found.

    """
    result = await db.execute(select(Review).where(Review.id == review_id))
    review = result.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, content={"detail": "Review not found"})

    review.like_count += 1
    await db.commit()
    return {"message": "Review liked", "like_count": review.like_count}
