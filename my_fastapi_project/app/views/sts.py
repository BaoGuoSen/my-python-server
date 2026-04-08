"""STS view models."""
from pydantic import BaseModel


class StsTokenResponse(BaseModel):
    """STS temporary credential response."""

    tmp_secret_id: str
    tmp_secret_key: str
    session_token: str
    start_time: int
    expired_time: int
    bucket: str
    region: str
