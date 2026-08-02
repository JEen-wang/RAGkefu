"""Chat query endpoint (contract + mock implementation)."""

import time

from fastapi import APIRouter

from app.core.request_context import get_request_id
from app.schemas.chat import ChatQueryRequest, ChatQueryResponse, Citation

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/query", response_model=ChatQueryResponse)
async def chat_query(body: ChatQueryRequest) -> ChatQueryResponse:
    """Return a deterministic mock answer to lock the API contract.

    Real exact-query / FAQ retrieval will replace this in later steps.
    """
    started = time.perf_counter()
    # Fixed mock keeps OpenAPI/clients stable before business wiring.
    answer = (
        f"[mock] 已收到问题：{body.query}。"
        "后续步骤将接入订单精确查询与 FAQ 检索。"
    )
    latency_ms = max(int((time.perf_counter() - started) * 1000), 0)
    return ChatQueryResponse(
        answer=answer,
        route="mock",
        confidence=1.0,
        latency_ms=latency_ms,
        citations=[
            Citation(
                type="mock",
                source="s09-contract-mock",
                snippet="placeholder citation for API contract",
            )
        ],
        trace_id=get_request_id(),
    )
