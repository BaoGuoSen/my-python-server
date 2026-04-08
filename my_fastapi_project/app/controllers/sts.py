"""STS controller - provides temporary COS credentials for frontend."""
import asyncio
import json
import time
from functools import partial

from fastapi import APIRouter, Depends

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.sts import StsTokenResponse
from my_fastapi_project.config.application import settings

router = APIRouter(prefix="/sts", tags=["sts"])

_STS_DURATION = 7200  # 2 hours


def _fetch_sts_token() -> dict:
    """Call Tencent Cloud STS API to get temporary credentials.

    Returns:
        dict: Temporary credentials dict.

    Raises:
        Exception: If STS API call fails.

    """
    from tencentcloud.common import credential
    from tencentcloud.sts.v20180813 import models as sts_models
    from tencentcloud.sts.v20180813 import sts_client

    cred = credential.Credential(settings.COS_SECRET_ID, settings.COS_SECRET_KEY)
    client = sts_client.StsClient(cred, "ap-beijing")

    appid = settings.COS_BUCKET.rsplit("-", 1)[-1]
    policy = {
        "version": "2.0",
        "statement": [
            {
                "effect": "allow",
                "action": ["cos:*"],
                "resource": [
                    f"qcs::cos:{settings.COS_REGION}:uid/{appid}:{settings.COS_BUCKET}/*"
                ],
            }
        ],
    }

    req = sts_models.GetFederationTokenRequest()
    req.Name = "home-cook-frontend"
    req.DurationSeconds = _STS_DURATION
    req.Policy = json.dumps(policy)

    resp = client.GetFederationToken(req)
    return {
        "tmp_secret_id": resp.Credentials.TmpSecretId,
        "tmp_secret_key": resp.Credentials.TmpSecretKey,
        "session_token": resp.Credentials.Token,
        "start_time": int(time.time()),
        "expired_time": resp.ExpiredTime,
    }


@router.get("/token", response_model=StsTokenResponse)
async def get_sts_token(
    current_user: User = Depends(get_current_user),
) -> StsTokenResponse:
    """Get temporary COS credentials for frontend read access.

    Args:
        current_user: Current authenticated user.

    Returns:
        StsTokenResponse: Temporary credentials valid for 2 hours.

    Raises:
        HTTPException: If STS API call fails.

    """
    loop = asyncio.get_event_loop()
    try:
        token = await loop.run_in_executor(None, partial(_fetch_sts_token))
    except Exception as e:
        raise HTTPException(
            status_code=500, content={"detail": f"Failed to get STS token: {e}"}
        )

    return StsTokenResponse(
        **token,
        bucket=settings.COS_BUCKET,
        region=settings.COS_REGION,
    )
