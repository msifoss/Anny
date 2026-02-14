from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from anny.clients.ga4 import GA4Client
from anny.core.dependencies import get_ga4_client
from anny.main import app


def _mock_ga4_client():
    return MagicMock(spec=GA4Client)


def _client_with_mock_ga4(mock_client):
    app.dependency_overrides[get_ga4_client] = lambda: mock_client
    tc = TestClient(app)
    yield tc
    app.dependency_overrides.clear()


def test_report_endpoint():
    mock_client = _mock_ga4_client()
    app.dependency_overrides[get_ga4_client] = lambda: mock_client

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [
            {"date": "2024-01-01", "sessions": "100", "totalUsers": "50"}
        ]
        tc = TestClient(app)
        response = tc.post("/api/ga4/report", json={"metrics": "sessions,totalUsers"})

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 1
    assert data["rows"][0]["sessions"] == "100"


def test_top_pages_endpoint():
    mock_client = _mock_ga4_client()
    app.dependency_overrides[get_ga4_client] = lambda: mock_client

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "500"}]
        tc = TestClient(app)
        response = tc.get("/api/ga4/top-pages")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 1


def test_traffic_summary_endpoint():
    mock_client = _mock_ga4_client()
    app.dependency_overrides[get_ga4_client] = lambda: mock_client

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"sessionSource": "google", "sessions": "300"}]
        tc = TestClient(app)
        response = tc.get("/api/ga4/traffic-summary")

    app.dependency_overrides.clear()

    assert response.status_code == 200
    data = response.json()
    assert data["row_count"] == 1
