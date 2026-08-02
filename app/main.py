"""FastAPI application entrypoint."""

from fastapi import FastAPI

app = FastAPI(
    title="RAGkefu",
    description="企业级智能客服混合检索 RAG 系统",
    version="0.1.0",
)


@app.get("/")
async def root() -> dict[str, str]:
    """Minimal liveness-style ping for bootstrap verification."""
    return {
        "name": "RAGkefu",
        "status": "ok",
        "message": "minimal FastAPI app is running",
    }
