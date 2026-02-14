from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from anny.clients.search_console import SearchConsoleClient
from anny.core.dependencies import get_search_console_client
from anny.main import app


def _mock_sc_client():
    return MagicMock(spec=SearchConsoleClient)


def test_query_endpoint():
    mock_client = _mock_sc_client()
    app.dependency_overrides[get_search_console_client] = lambda: mock_client

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"query": "python", "clicks": 100}]
        tc = TestClient(app)
        response = tc.post("/api/search-console/query", json={"dimensions": "query"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 1
    assert data["rows"][0]["query"] == "python"


def test_top_queries_endpoint():
    mock_client = _mock_sc_client()
    app.dependency_overrides[get_search_console_client] = lambda: mock_client

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"query": "fastapi", "clicks": 200}]
        tc = TestClient(app)
        response = tc.get("/api/search-console/top-queries")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["row_count"] == 1


def test_top_pages_endpoint():
    mock_client = _mock_sc_client()
    app.dependency_overrides[get_search_console_client] = lambda: mock_client

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"page": "/", "clicks": 500}]
        tc = TestClient(app)
        response = tc.get("/api/search-console/top-pages")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["row_count"] == 1


def test_summary_endpoint():
    mock_client = _mock_sc_client()
    app.dependency_overrides[get_search_console_client] = lambda: mock_client

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"clicks": 5000}]
        tc = TestClient(app)
        response = tc.get("/api/search-console/summary")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["row_count"] == 1
