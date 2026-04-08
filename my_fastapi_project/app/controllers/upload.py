"""Upload controller."""
import asyncio
import os
import uuid
from functools import partial

from fastapi import APIRouter, Depends, UploadFile
from qcloud_cos import CosConfig, CosS3Client

from my_fastapi_project.app.controllers.user import get_current_user
from my_fastapi_project.app.exceptions.http import HTTPException
from my_fastapi_project.app.models.user import User
from my_fastapi_project.app.views.upload import UploadImageResponse
from my_fastapi_project.config.application import settings

router = APIRouter(tags=["upload"])

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


def _get_cos_client() -> CosS3Client:
    """Create and return a COS client.

    Returns:
        CosS3Client: Configured Tencent Cloud COS client.

    """
    config = CosConfig(
        Region=settings.COS_REGION,
        SecretId=settings.COS_SECRET_ID,
        SecretKey=settings.COS_SECRET_KEY,
    )
    return CosS3Client(config)


def _upload_to_cos(key: str, content: bytes, content_type: str) -> None:
    """Upload bytes to COS synchronously.

    Args:
        key: Object key in the bucket.
        content: File content bytes.
        content_type: MIME type of the file.

    """
    client = _get_cos_client()
    client.put_object(
        Bucket=settings.COS_BUCKET,
        Body=content,
        Key=key,
        ContentType=content_type,
    )


@router.post("/upload/image", response_model=UploadImageResponse)
async def upload_image(
    file: UploadFile,
    current_user: User = Depends(get_current_user),
) -> UploadImageResponse:
    """Upload an image file to Tencent Cloud COS.

    Args:
        file: The image file to upload (JPEG, PNG, GIF or WebP, max 10 MB).
        current_user: Current authenticated user.

    Returns:
        UploadImageResponse: Public URL of the uploaded image.

    Raises:
        HTTPException: If the file type is not allowed or the file is too large.

    """
    if not file.content_type or file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            content={"detail": "Invalid file type. Only JPEG, PNG, GIF and WebP are allowed."},
        )

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            content={"detail": "File too large. Maximum size is 10 MB."},
        )

    filename = file.filename or "image"
    ext = os.path.splitext(filename)[1] or ".jpg"
    key = f"images/{uuid.uuid4().hex}{ext}"

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(
        None,
        partial(_upload_to_cos, key, content, file.content_type),
    )

    url = f"https://{settings.COS_BUCKET}.cos.{settings.COS_REGION}.myqcloud.com/{key}"
    return UploadImageResponse(url=url)
