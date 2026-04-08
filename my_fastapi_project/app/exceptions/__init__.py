"""Application implementation - exceptions."""
from my_fastapi_project.app.exceptions.http import (
    HTTPException,
    http_exception_handler,
)


__all__ = ("HTTPException", "http_exception_handler")
