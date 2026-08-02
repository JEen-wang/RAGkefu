"""Chat API contract tests (mock implementation)."""

from fastapi.testclient import TestClient


def test_chat_query_mock_success(client: TestClient) -> None:
    response = client.post(
        "/v1/chat/query",
        json={
            "query": "我的订单到哪了？",
            "user_id": "u_1",
            "session_id": "s_1",
            "channel": "web",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["route"] == "mock"
    assert body["answer"].startswith("[mock]")
    assert body["confidence"] == 1.0
    assert isinstance(body["latency_ms"], int)
    assert body["citations"][0]["type"] == "mock"
    assert body["trace_id"] == response.headers["X-Request-ID"]


def test_chat_query_empty_query_validation_error(client: TestClient) -> None:
    response = client.post("/v1/chat/query", json={"query": ""})
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == 4220
    assert body["message"] == "请求参数校验失败"
    assert body["request_id"] == response.headers["X-Request-ID"]


def test_v1_ping_ok(client: TestClient) -> None:
    response = client.get("/v1/ping")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
