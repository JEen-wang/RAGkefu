"""Liveness and readiness health check endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.db.session import check_db_connection

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


@router.get("/readyz")
async def readyz() -> JSONResponse:
    """Readiness probe. Returns 503 when required dependencies are down."""
    settings = get_settings()
    checks: dict[str, str] = {}

    try:
        db_ok = await check_db_connection()
        checks["postgres"] = "ok" if db_ok else "fail"
    except Exception as exc:  # noqa: BLE001 - readiness must never crash the process
        checks["postgres"] = f"fail:{exc.__class__.__name__}"
        db_ok = False

    ready = all(value == "ok" for value in checks.values())
    payload = {
        "status": "ready" if ready else "not_ready",
        "env": settings.app_env,
        "version": settings.app_version,
        "checks": checks,
    }
    return JSONResponse(status_code=200 if ready else 503, content=payload)
