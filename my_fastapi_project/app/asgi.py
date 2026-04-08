"""Application implementation - ASGI."""
import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from my_fastapi_project.config import settings
from my_fastapi_project.app.router import root_api_router
from my_fastapi_project.app.exceptions import (
    HTTPException,
    http_exception_handler,
)
from my_fastapi_project.app.models.database import Base, engine
import my_fastapi_project.app.models  # noqa: F401 - registers all models with Base


log = logging.getLogger(__name__)


async def on_startup() -> None:
    """Define FastAPI startup event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#startup-event

    """
    log.debug("Execute FastAPI startup event handler.")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def on_shutdown() -> None:
    """Define FastAPI shutdown event handler.

    Resources:
        1. https://fastapi.tiangolo.com/advanced/events/#shutdown-event

    """
    log.debug("Execute FastAPI shutdown event handler.")
    await engine.dispose()


def get_application() -> FastAPI:
    """Initialize FastAPI application.

    Returns:
       FastAPI: Application object instance.

    """
    log.debug("Initialize FastAPI application node.")
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
        version=settings.VERSION,
        docs_url=None,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        swagger_ui_init_oauth={},
    )
    log.debug("Add application routes.")
    app.include_router(root_api_router)
    log.debug("Register global exception handler for custom HTTPException.")
    app.add_exception_handler(HTTPException, http_exception_handler)

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui() -> HTMLResponse:
        """Serve Swagger UI using domestic CDN for China accessibility."""
        return get_swagger_ui_html(
            openapi_url=app.openapi_url or "/openapi.json",
            title=app.title + " - Swagger UI",
            swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.1.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.1.0/swagger-ui.css",
        )

    return app
