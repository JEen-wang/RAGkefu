"""FastAPI exception handlers producing unified ErrorResponse."""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError
from app.core.request_context import get_request_id
from app.schemas.common import ErrorResponse

logger = logging.getLogger(__name__)


def _error_body(code: int, message: str, detail=None) -> dict:
    payload = ErrorResponse(
        code=code,
        message=message,
        detail=detail,
        request_id=get_request_id(),
    )
    return payload.model_dump()


def register_exception_handlers(app: FastAPI) -> None:
    """Attach unified exception handlers to the app."""

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.code, exc.message, exc.detail),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content=_error_body(4220, "请求参数校验失败", exc.errors()),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(
        _: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.status_code, str(exc.detail), None),
        )

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled error: %s", exc)
        return JSONResponse(
            status_code=500,
            content=_error_body(5000, "服务内部错误", None),
        )
