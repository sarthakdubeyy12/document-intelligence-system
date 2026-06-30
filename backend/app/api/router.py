"""Central API router aggregating all route modules."""

from fastapi import APIRouter

from app.api.routes import chat, health, upload

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(upload.router)
api_router.include_router(chat.router)
