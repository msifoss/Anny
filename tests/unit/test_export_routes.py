from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from anny.clients.ga4 import GA4Client
from anny.clients.search_console import SearchConsoleClient
from anny.core.dependencies import get_ga4_client, get_search_console_client, verify_api_key
from anny.main import app


def _setup_ga4(mock_client):
    app.dependency_overrides[get_ga4_client] = lambda: mock_client
    app.dependency_overrides[verify_api_key] = lambda: None


def _setup_sc(mock_client):
    app.dependency_overrides[get_search_console_client] = lambda: mock_client
    app.dependency_overrides[verify_api_key] = lambda: None


def _teardown():
    app.dependency_overrides.pop(get_ga4_client, None)
    app.dependency_overrides.pop(get_search_console_client, None)
    app.dependency_overrides.pop(verify_api_key, None)


def test_export_ga4_top_pages_csv():
    mock_client = MagicMock(spec=GA4Client)
    _setup_ga4(mock_client)

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "500"}]
        tc = TestClient(app)
        response = tc.get("/api/export/ga4/top-pages?format=csv")

    _teardown()

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "attachment" in response.headers["content-disposition"]
    assert "pagePath" in response.text


def test_export_ga4_top_pages_json():
    mock_client = MagicMock(spec=GA4Client)
    _setup_ga4(mock_client)

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "500"}]
        tc = TestClient(app)
        response = tc.get("/api/export/ga4/top-pages?format=json")

    _teardown()

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    data = response.json()
    assert data[0]["pagePath"] == "/"


def test_export_sc_top_queries_csv():
    mock_client = MagicMock(spec=SearchConsoleClient)
    _setup_sc(mock_client)

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"query": "python", "clicks": 200}]
        tc = TestClient(app)
        response = tc.get("/api/export/search-console/top-queries?format=csv")

    _teardown()

    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]
    assert "python" in response.text


def test_export_invalid_format_422():
    mock_client = MagicMock(spec=GA4Client)
    _setup_ga4(mock_client)

    tc = TestClient(app)
    response = tc.get("/api/export/ga4/top-pages?format=xml")

    _teardown()

    assert response.status_code == 422


def test_export_content_disposition_quoted_filename():
    mock_client = MagicMock(spec=GA4Client)
    _setup_ga4(mock_client)

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "500"}]
        tc = TestClient(app)
        response = tc.get("/api/export/ga4/top-pages?format=csv")

    _teardown()

    assert response.status_code == 200
    cd = response.headers["content-disposition"]
    assert 'filename="ga4-top-pages.csv"' in cd


def test_export_limit_clamped():
    mock_client = MagicMock(spec=GA4Client)
    _setup_ga4(mock_client)

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/"}]
        tc = TestClient(app)
        response = tc.get("/api/export/ga4/top-pages?format=csv&limit=999999")

    _teardown()

    assert response.status_code == 200
    # Verify the service was called with clamped limit (100), not 999999
    mock_client.run_report.assert_called_once()
    call_kwargs = mock_client.run_report.call_args[1]
    assert call_kwargs["limit"] <= 100
