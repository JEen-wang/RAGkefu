"""Top-level API router assembly."""

from fastapi import APIRouter

from app.api.v1 import health
from app.api.v1.router import router as v1_router
from app.core.config import get_settings

api_router = APIRouter()

# Liveness stays at root (not under /v1) for probe conventions.
api_router.include_router(health.router)

settings = get_settings()
api_router.include_router(v1_router, prefix=settings.api_prefix)
