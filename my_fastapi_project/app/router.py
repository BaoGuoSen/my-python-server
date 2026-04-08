"""Application configuration - root APIRouter.

Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications

"""
from fastapi import APIRouter

from my_fastapi_project.app.controllers import auth, chef, dish, home, ready, review, sts, upload, user

root_api_router = APIRouter(prefix="/api")

root_api_router.include_router(ready.router, tags=["ready"])
root_api_router.include_router(auth.router)
root_api_router.include_router(user.router)
root_api_router.include_router(home.router)
root_api_router.include_router(chef.router)
root_api_router.include_router(dish.router)
root_api_router.include_router(review.router)
root_api_router.include_router(upload.router)
root_api_router.include_router(sts.router)
