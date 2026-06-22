from fastapi import APIRouter

from app.api.routes import health, problems

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(problems.router, prefix="/problems", tags=["problems"])
