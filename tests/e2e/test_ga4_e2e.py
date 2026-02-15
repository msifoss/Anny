import pytest


@pytest.mark.e2e
class TestGA4TopPages:
    def test_returns_200(self, live_client):
        resp = live_client.get(
            "/api/ga4/top-pages", params={"date_range": "last_28_days", "limit": 5}
        )
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        resp = live_client.get(
            "/api/ga4/top-pages", params={"date_range": "last_28_days", "limit": 3}
        )
        data = resp.json()
        assert "rows" in data
        assert "row_count" in data
        assert isinstance(data["rows"], list)
        assert data["row_count"] == len(data["rows"])


@pytest.mark.e2e
class TestGA4TrafficSummary:
    def test_returns_200(self, live_client):
        resp = live_client.get("/api/ga4/traffic-summary", params={"date_range": "last_28_days"})
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        resp = live_client.get("/api/ga4/traffic-summary", params={"date_range": "last_28_days"})
        data = resp.json()
        assert isinstance(data["rows"], list)
        if data["rows"]:
            row = data["rows"][0]
            assert isinstance(row, dict)


@pytest.mark.e2e
class TestGA4CustomReport:
    def test_returns_200(self, live_client):
        resp = live_client.post(
            "/api/ga4/report",
            json={
                "metrics": "sessions",
                "dimensions": "date",
                "date_range": "last_28_days",
                "limit": 3,
            },
        )
        assert resp.status_code == 200

    def test_row_shape(self, live_client):
        resp = live_client.post(
            "/api/ga4/report",
            json={
                "metrics": "sessions,totalUsers",
                "dimensions": "date",
                "date_range": "last_28_days",
                "limit": 1,
            },
        )
        data = resp.json()
        assert isinstance(data["rows"], list)
        if data["rows"]:
            row = data["rows"][0]
            assert "date" in row
            assert "sessions" in row
            assert "totalUsers" in row
