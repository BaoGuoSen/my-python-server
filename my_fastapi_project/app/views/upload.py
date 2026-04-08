"""Upload views."""
from pydantic import BaseModel


class UploadImageResponse(BaseModel):
    """Response model for image upload.

    Attributes:
        url (str): The public URL of the uploaded image.

    """

    url: str
