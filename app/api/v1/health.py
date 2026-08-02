"""Liveness health check endpoints."""

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/healthz")
async def healthz() -> dict[str, str]:
    """Process liveness probe. Does not check external dependencies."""
    settings = get_settings()
    return {
        "status": "ok",
        "env": settings.app_env,
        "version": settings.app_version,
    }
