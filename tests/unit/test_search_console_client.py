from unittest.mock import MagicMock

import pytest

from anny.clients.search_console import SearchConsoleClient
from anny.core.exceptions import APIError


def _make_mock_service(response):
    service = MagicMock()
    service.searchanalytics().query().execute.return_value = response
    return service


def test_query_flattens_response():
    response = {
        "rows": [
            {
                "keys": ["python tutorial"],
                "clicks": 150,
                "impressions": 3000,
                "ctr": 0.05,
                "position": 4.2,
            },
            {
                "keys": ["fastapi guide"],
                "clicks": 80,
                "impressions": 1200,
                "ctr": 0.0667,
                "position": 6.8,
            },
        ]
    }
    service = _make_mock_service(response)
    client = SearchConsoleClient(service, "https://example.com")

    rows = client.query("2024-01-01", "2024-01-28", dimensions=["query"])

    assert len(rows) == 2
    assert rows[0]["query"] == "python tutorial"
    assert rows[0]["clicks"] == 150
    assert rows[0]["ctr"] == 5.0  # 0.05 * 100
    assert rows[0]["position"] == 4.2


def test_query_empty_response():
    service = _make_mock_service({"rows": []})
    client = SearchConsoleClient(service, "https://example.com")

    rows = client.query("2024-01-01", "2024-01-28", dimensions=["query"])
    assert not rows


def test_query_no_dimensions():
    response = {
        "rows": [{"keys": [], "clicks": 500, "impressions": 10000, "ctr": 0.05, "position": 8.5}]
    }
    service = _make_mock_service(response)
    client = SearchConsoleClient(service, "https://example.com")

    rows = client.query("2024-01-01", "2024-01-28")
    assert len(rows) == 1
    assert rows[0]["clicks"] == 500


def test_query_api_failure():
    service = MagicMock()
    service.searchanalytics().query().execute.side_effect = RuntimeError("API error")
    client = SearchConsoleClient(service, "https://example.com")

    with pytest.raises(APIError, match="Search Console query failed"):
        client.query("2024-01-01", "2024-01-28")


def test_site_url_property():
    service = MagicMock()
    client = SearchConsoleClient(service, "https://example.com")
    assert client.site_url == "https://example.com"
