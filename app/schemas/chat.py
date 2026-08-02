"""Chat query API schemas."""

from typing import Any, Literal

from pydantic import BaseModel, Field


class ChatQueryRequest(BaseModel):
    """Incoming customer question."""

    query: str = Field(..., min_length=1, max_length=2000, description="用户问题")
    user_id: str | None = Field(default=None, description="用户 ID")
    session_id: str | None = Field(default=None, description="会话 ID")
    channel: str = Field(default="web", description="来源渠道，如 web/app/wechat")


class Citation(BaseModel):
    """Source attribution for an answer."""

    type: Literal["db", "faq", "mock"] = Field(..., description="溯源类型")
    table: str | None = Field(default=None, description="DB 表名（type=db）")
    keys: dict[str, Any] | None = Field(default=None, description="主键/业务键")
    fields: list[str] | None = Field(default=None, description="引用字段")
    doc_id: str | None = Field(default=None, description="FAQ 文档 ID")
    chunk_id: str | None = Field(default=None, description="FAQ chunk ID")
    source: str | None = Field(default=None, description="来源路径或标识")
    snippet: str | None = Field(default=None, description="引用片段")


class ChatQueryResponse(BaseModel):
    """Structured answer returned to the client."""

    answer: str
    route: str = Field(..., description="路由结果，如 exact_order / faq / mock")
    confidence: float = Field(..., ge=0.0, le=1.0)
    latency_ms: int = Field(..., ge=0)
    citations: list[Citation] = Field(default_factory=list)
    trace_id: str | None = Field(default=None, description="与 X-Request-ID 对齐")
