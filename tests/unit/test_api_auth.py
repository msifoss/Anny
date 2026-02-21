"""Tests for REST API key authentication."""

from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from anny.clients.ga4 import GA4Client
from anny.core.cache import QueryCache
from anny.core.dependencies import get_ga4_client, get_query_cache, verify_api_key
from anny.main import app

TEST_API_KEY = "test-secret-key-12345"


class TestAPIKeyAuth:  # pylint: disable=attribute-defined-outside-init
    """Test API key authentication on REST endpoints."""

    def setup_method(self):
        self.mock_client = MagicMock(spec=GA4Client)
        self.mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "100"}]
        app.dependency_overrides[get_ga4_client] = lambda: self.mock_client
        app.dependency_overrides[get_query_cache] = lambda: QueryCache(ttl=60, max_entries=10)
        self.tc = TestClient(app)

    def teardown_method(self):
        app.dependency_overrides.clear()

    @patch("anny.core.dependencies.settings")
    def test_valid_key_returns_200(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        response = self.tc.get("/api/ga4/top-pages", headers={"X-API-Key": TEST_API_KEY})
        assert response.status_code == 200

    @patch("anny.core.dependencies.settings")
    def test_invalid_key_returns_401(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        response = self.tc.get("/api/ga4/top-pages", headers={"X-API-Key": "wrong-key"})
        assert response.status_code == 401
        assert "Invalid or missing API key" in response.json()["error"]

    @patch("anny.core.dependencies.settings")
    def test_missing_key_returns_401(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        response = self.tc.get("/api/ga4/top-pages")
        assert response.status_code == 401
        assert "Invalid or missing API key" in response.json()["error"]

    @patch("anny.core.dependencies.settings")
    def test_empty_key_returns_401(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        response = self.tc.get("/api/ga4/top-pages", headers={"X-API-Key": ""})
        assert response.status_code == 401

    @patch("anny.core.dependencies.settings")
    def test_auth_disabled_when_no_key_configured(self, mock_settings):
        mock_settings.anny_api_key = ""
        response = self.tc.get("/api/ga4/top-pages")
        assert response.status_code == 200

    def test_health_endpoint_no_auth_required(self):
        response = self.tc.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] in ("healthy", "degraded")

    @patch("anny.core.dependencies.settings")
    def test_auth_applies_to_post_endpoints(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        response = self.tc.post(
            "/api/ga4/report",
            json={"metrics": "sessions", "dimensions": "date", "date_range": "last_7_days"},
        )
        assert response.status_code == 401

    @patch("anny.core.dependencies.settings")
    def test_auth_override_bypasses_check(self, mock_settings):
        mock_settings.anny_api_key = TEST_API_KEY
        app.dependency_overrides[verify_api_key] = lambda: None
        response = self.tc.get("/api/ga4/top-pages")
        assert response.status_code == 200


def test_mcp_path_is_rate_limited():
    """Requests to /mcp should be subject to rate limiting."""
    from anny.main import _rate_limit_store  # pylint: disable=import-outside-toplevel

    # Simulate a burst that exceeds the limit
    _rate_limit_store["testclient"] = [__import__("time").time()] * 60

    tc = TestClient(app)
    response = tc.get("/mcp/")
    assert response.status_code == 429
