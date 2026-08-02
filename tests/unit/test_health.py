"""Health endpoint contract tests."""

from fastapi.testclient import TestClient


def test_healthz_ok(client: TestClient) -> None:
    response = client.get("/healthz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "env" in body
    assert "version" in body
    assert "X-Request-ID" in response.headers


def test_readyz_ok_when_postgres_up(client: TestClient) -> None:
    response = client.get("/readyz")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["checks"]["postgres"] == "ok"


def test_readyz_not_ready_when_postgres_down(
    client: TestClient, monkeypatch
) -> None:
    async def _fail() -> bool:
        return False

    monkeypatch.setattr("app.api.v1.health.check_db_connection", _fail)
    response = client.get("/readyz")
    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "not_ready"
    assert body["checks"]["postgres"] == "fail"
