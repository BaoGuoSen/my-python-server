"""Application implementation - views."""
from my_fastapi_project.app.views.error import ErrorResponse
from my_fastapi_project.app.views.ready import ReadyResponse

__all__ = ("ErrorResponse", "ReadyResponse")
