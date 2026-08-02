"""FastAPI application entrypoint."""

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import RequestIdMiddleware

settings = get_settings()
setup_logging(debug=settings.debug)

app = FastAPI(
    title=settings.app_name,
    description="企业级智能客服混合检索 RAG 系统",
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(RequestIdMiddleware)
register_exception_handlers(app)
app.include_router(api_router)


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
