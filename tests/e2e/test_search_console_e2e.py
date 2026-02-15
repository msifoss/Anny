import pytest


@pytest.mark.e2e
class TestSearchConsoleTopQueries:
    def test_returns_200(self, live_client):
        resp = live_client.get(
            "/api/search-console/top-queries",
            params={"date_range": "last_28_days", "limit": 5},
        )
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        resp = live_client.get(
            "/api/search-console/top-queries",
            params={"date_range": "last_28_days", "limit": 3},
        )
        data = resp.json()
        assert "rows" in data
        assert "row_count" in data
        assert isinstance(data["rows"], list)


@pytest.mark.e2e
class TestSearchConsoleTopPages:
    def test_returns_200(self, live_client):
        resp = live_client.get(
            "/api/search-console/top-pages",
            params={"date_range": "last_28_days", "limit": 5},
        )
        assert resp.status_code == 200


@pytest.mark.e2e
class TestSearchConsoleSummary:
    def test_returns_200(self, live_client):
        resp = live_client.get(
            "/api/search-console/summary",
            params={"date_range": "last_28_days"},
        )
        assert resp.status_code == 200

    def test_response_shape(self, live_client):
        resp = live_client.get(
            "/api/search-console/summary",
            params={"date_range": "last_28_days"},
        )
        data = resp.json()
        assert isinstance(data["rows"], list)
        assert data["row_count"] == len(data["rows"])


@pytest.mark.e2e
class TestSearchConsoleCustomQuery:
    def test_returns_200(self, live_client):
        resp = live_client.post(
            "/api/search-console/query",
            json={
                "dimensions": "query",
                "date_range": "last_28_days",
                "row_limit": 3,
            },
        )
        assert resp.status_code == 200

    def test_row_shape(self, live_client):
        resp = live_client.post(
            "/api/search-console/query",
            json={
                "dimensions": "query,page",
                "date_range": "last_28_days",
                "row_limit": 1,
            },
        )
        data = resp.json()
        assert isinstance(data["rows"], list)
        if data["rows"]:
            row = data["rows"][0]
            assert isinstance(row, dict)
