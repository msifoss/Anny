import pytest


@pytest.mark.e2e
def test_health(live_client):
    resp = live_client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
