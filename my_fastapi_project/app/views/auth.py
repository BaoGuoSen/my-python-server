"""Auth view models."""
from pydantic import BaseModel, Field


class WxLoginRequest(BaseModel):
    """WeChat login request."""

    code: str = Field(..., description="WeChat authorization code")


class WxLoginResponse(BaseModel):
    """WeChat login response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user_id: int = Field(..., description="User ID")
    nickname: str = Field(..., description="User nickname")
    avatar_url: str = Field(..., description="User avatar URL")
