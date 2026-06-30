"""Service information and health check endpoints."""

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.constants import HEALTH_STATUS_OK

router = APIRouter(tags=["health"])


@router.get("/")
def read_root(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    """Return basic information about the API."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
    }


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return a simple health response confirming the application is running."""
    return {"status": HEALTH_STATUS_OK}
