"""Integration tests: full stack with mocked Google responses.

These tests verify the full request flow from HTTP endpoint through
service layer to (mocked) client, without hitting real Google APIs.
"""

from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from anny.clients.ga4 import GA4Client
from anny.clients.search_console import SearchConsoleClient
from anny.clients.tag_manager import TagManagerClient
from anny.core.dependencies import (
    get_ga4_client,
    get_search_console_client,
    get_tag_manager_client,
)
from anny.main import app


class TestGA4FullStack:  # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        self.mock_client = MagicMock(spec=GA4Client)
        app.dependency_overrides[get_ga4_client] = lambda: self.mock_client
        self.tc = TestClient(app)

    def teardown_method(self):
        app.dependency_overrides.clear()

    def test_report_flow(self):
        self.mock_client.run_report.return_value = [
            {"date": "2024-01-01", "sessions": "500", "totalUsers": "200"}
        ]
        response = self.tc.post(
            "/api/ga4/report",
            json={
                "metrics": "sessions,totalUsers",
                "dimensions": "date",
                "date_range": "last_7_days",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["row_count"] == 1
        assert data["rows"][0]["sessions"] == "500"

    def test_top_pages_flow(self):
        self.mock_client.run_report.return_value = [
            {"pagePath": "/", "screenPageViews": "1000", "sessions": "800", "totalUsers": "600"}
        ]
        response = self.tc.get("/api/ga4/top-pages?date_range=last_28_days&limit=5")
        assert response.status_code == 200
        assert response.json()["row_count"] == 1

    def test_traffic_summary_flow(self):
        self.mock_client.run_report.return_value = [
            {
                "sessionSource": "google",
                "sessions": "300",
                "totalUsers": "250",
                "screenPageViews": "800",
                "bounceRate": "0.45",
            }
        ]
        response = self.tc.get("/api/ga4/traffic-summary")
        assert response.status_code == 200


class TestSearchConsoleFullStack:  # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        self.mock_client = MagicMock(spec=SearchConsoleClient)
        app.dependency_overrides[get_search_console_client] = lambda: self.mock_client
        self.tc = TestClient(app)

    def teardown_method(self):
        app.dependency_overrides.clear()

    def test_query_flow(self):
        self.mock_client.query.return_value = [
            {
                "query": "python fastapi",
                "clicks": 120,
                "impressions": 5000,
                "ctr": 2.4,
                "position": 5.3,
            }
        ]
        response = self.tc.post(
            "/api/search-console/query",
            json={"dimensions": "query", "date_range": "last_28_days"},
        )
        assert response.status_code == 200
        assert response.json()["row_count"] == 1

    def test_top_queries_flow(self):
        self.mock_client.query.return_value = [{"query": "analytics tool", "clicks": 80}]
        response = self.tc.get("/api/search-console/top-queries")
        assert response.status_code == 200

    def test_top_pages_flow(self):
        self.mock_client.query.return_value = [{"page": "/docs", "clicks": 300}]
        response = self.tc.get("/api/search-console/top-pages")
        assert response.status_code == 200

    def test_summary_flow(self):
        self.mock_client.query.return_value = [
            {"clicks": 10000, "impressions": 500000, "ctr": 2.0, "position": 12.5}
        ]
        response = self.tc.get("/api/search-console/summary")
        assert response.status_code == 200


class TestTagManagerFullStack:  # pylint: disable=attribute-defined-outside-init
    def setup_method(self):
        self.mock_client = MagicMock(spec=TagManagerClient)
        app.dependency_overrides[get_tag_manager_client] = lambda: self.mock_client
        self.tc = TestClient(app)

    def teardown_method(self):
        app.dependency_overrides.clear()

    def test_accounts_flow(self):
        self.mock_client.list_accounts.return_value = [
            {"accountId": "123", "name": "Production", "path": "accounts/123"}
        ]
        response = self.tc.get("/api/tag-manager/accounts")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_containers_flow(self):
        self.mock_client.list_containers.return_value = [
            {
                "containerId": "456",
                "name": "Web",
                "publicId": "GTM-XXXX",
                "path": "accounts/123/containers/456",
            }
        ]
        response = self.tc.get("/api/tag-manager/containers?account_id=123")
        assert response.status_code == 200
        assert response.json()["count"] == 1

    def test_container_setup_flow(self):
        self.mock_client.list_tags.return_value = [{"tagId": "1", "name": "GA4", "type": "gaawc"}]
        self.mock_client.list_triggers.return_value = [
            {"triggerId": "1", "name": "All Pages", "type": "pageview"}
        ]
        self.mock_client.list_variables.return_value = [
            {"variableId": "1", "name": "URL", "type": "u"}
        ]

        response = self.tc.get(
            "/api/tag-manager/container-setup?container_path=accounts/123/containers/456"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["tag_count"] == 1
        assert data["trigger_count"] == 1
        assert data["variable_count"] == 1


class TestHealthAndMCP:
    def test_health_endpoint(self):
        tc = TestClient(app)
        response = tc.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
