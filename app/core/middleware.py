"""HTTP middleware."""

import logging
import time
import uuid
from collections.abc import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.request_context import reset_request_id, set_request_id

logger = logging.getLogger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Assign/propagate X-Request-ID and log basic access info."""

    header_name = "X-Request-ID"

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        incoming = request.headers.get(self.header_name)
        request_id = incoming.strip() if incoming else uuid.uuid4().hex
        token = set_request_id(request_id)
        started = time.perf_counter()

        try:
            response = await call_next(request)
        except Exception:
            reset_request_id(token)
            raise

        duration_ms = (time.perf_counter() - started) * 1000
        response.headers[self.header_name] = request_id
        logger.info(
            "%s %s -> %s (%.2fms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        reset_request_id(token)
        return response
