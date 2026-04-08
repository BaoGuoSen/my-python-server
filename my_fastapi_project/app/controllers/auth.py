"""Auth controller."""
from datetime import datetime, timedelta

import httpx
from fastapi import APIRouter, Depends
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.database import get_db
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.auth import WxLoginRequest, WxLoginResponse
from my_fastapi_project.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
WX_CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"


async def _get_wx_openid(code: str) -> str:
    """Exchange WeChat code for openId.

    Args:
        code: WeChat authorization code from wx.login().

    Returns:
        str: WeChat openId.

    Raises:
        HTTPException: If WeChat API returns an error.

    """
    params = {
        "appid": settings.WX_APP_ID,
        "secret": settings.WX_APP_SECRET,
        "js_code": code,
        "grant_type": "authorization_code",
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(WX_CODE2SESSION_URL, params=params, timeout=10)
        data = resp.json()

    if "errcode" in data and data["errcode"] != 0:
        raise HTTPException(
            status_code=400,
            content={"detail": f"WeChat login failed: {data.get('errmsg', 'unknown error')}"},
        )

    open_id = data.get("openid")
    if not open_id:
        raise HTTPException(status_code=400, content={"detail": "Failed to get openId from WeChat"})

    return open_id


@router.post("/wx-login", response_model=WxLoginResponse)
async def wx_login(request: WxLoginRequest, db: AsyncSession = Depends(get_db)) -> WxLoginResponse:
    """WeChat login endpoint.

    Exchanges wx.login() code for openId, creates user if not exists,
    and returns a JWT token along with user info.

    Args:
        request: WeChat login request with code.
        db: Database session.

    Returns:
        WxLoginResponse: JWT token and user info.

    """
    open_id = await _get_wx_openid(request.code)

    result = await db.execute(select(User).where(User.open_id == open_id))
    user = result.scalar_one_or_none()

    if not user:
        user = User(open_id=open_id, nickname="", avatar_url="")
        db.add(user)

    await db.commit()
    await db.refresh(user)

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": str(user.id), "exp": expire}
    access_token = jwt.encode(token_data, settings.SECRET_KEY, algorithm=ALGORITHM)

    return WxLoginResponse(
        access_token=access_token,
        user_id=user.id,
        nickname=user.nickname,
        avatar_url=user.avatar_url,
    )
