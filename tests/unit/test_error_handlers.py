from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from anny.clients.ga4 import GA4Client
from anny.core.dependencies import get_ga4_client, verify_api_key
from anny.core.exceptions import APIError, AuthError
from anny.main import app


def _setup_overrides(mock_client):
    app.dependency_overrides[get_ga4_client] = lambda: mock_client
    app.dependency_overrides[verify_api_key] = lambda: None


def _teardown_overrides():
    app.dependency_overrides.pop(get_ga4_client, None)
    app.dependency_overrides.pop(verify_api_key, None)


def test_auth_error_returns_401():
    mock_client = MagicMock(spec=GA4Client)
    mock_client.run_report.side_effect = AuthError("bad creds")
    _setup_overrides(mock_client)

    tc = TestClient(app, raise_server_exceptions=False)
    response = tc.get("/api/ga4/top-pages")

    _teardown_overrides()

    assert response.status_code == 401
    assert response.json()["error"] == "bad creds"


def test_api_error_returns_502():
    mock_client = MagicMock(spec=GA4Client)
    mock_client.run_report.side_effect = APIError("GA4 down", service="ga4")
    _setup_overrides(mock_client)

    tc = TestClient(app, raise_server_exceptions=False)
    response = tc.get("/api/ga4/top-pages")

    _teardown_overrides()

    assert response.status_code == 502
    assert response.json()["error"] == "GA4 down"
