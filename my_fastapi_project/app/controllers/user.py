"""User controller."""
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.user import UserResponse, UserUpdateRequest

router = APIRouter(prefix="/users", tags=["users"])

SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
_security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current user from JWT token.

    Args:
        credentials: HTTP Bearer credentials from Authorization header.
        db: Database session.

    Returns:
        User: Current authenticated user.

    Raises:
        HTTPException: If token is invalid or user not found.

    """
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, content={"detail": "Invalid token"})

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, content={"detail": "User not found"})

    return user


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Get current user info.

    Args:
        current_user: Current authenticated user.

    Returns:
        UserResponse: User information.

    """
    return UserResponse.from_orm(current_user)


@router.post("/me/update", response_model=UserResponse)
async def update_me(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """Update current user info.

    Args:
        request: User update request.
        current_user: Current authenticated user.
        db: Database session.

    Returns:
        UserResponse: Updated user information.

    """
    if request.nickname is not None:
        current_user.nickname = request.nickname
    if request.avatar_url is not None:
        current_user.avatar_url = request.avatar_url

    await db.commit()
    await db.refresh(current_user)
    return UserResponse.from_orm(current_user)
