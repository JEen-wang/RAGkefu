"""Shared API schemas."""

from typing import Any

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Unified error payload returned by exception handlers."""

    code: int = Field(..., description="业务错误码")
    message: str = Field(..., description="可读错误信息")
    detail: Any = Field(default=None, description="可选细节（如校验错误列表）")
    request_id: str | None = Field(default=None, description="请求追踪 ID")
