"""API v1 route aggregator."""

from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/ping", tags=["system"])
async def ping(q: int = Query(default=0, ge=0)) -> dict[str, str | int]:
    """Versioned ping used to verify /v1 mounting and validation errors."""
    return {"status": "ok", "q": q}
