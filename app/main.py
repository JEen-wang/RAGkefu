"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.v1 import health
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="企业级智能客服混合检索 RAG 系统",
    version=settings.app_version,
    debug=settings.debug,
)

app.include_router(health.router)


@app.get("/")
async def root() -> dict[str, str]:
    """Minimal liveness-style ping for bootstrap verification."""
    return {
        "name": settings.app_name,
        "status": "ok",
        "env": settings.app_env,
        "version": settings.app_version,
        "message": "minimal FastAPI app is running",
    }
