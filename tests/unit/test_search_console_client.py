from unittest.mock import MagicMock

import pytest
from googleapiclient.errors import HttpError
from httplib2 import Response

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
    service.searchanalytics().query().execute.side_effect = HttpError(
        Response({"status": "403"}), b"forbidden"
    )
    client = SearchConsoleClient(service, "https://example.com")

    with pytest.raises(APIError, match="Search Console query failed"):
        client.query("2024-01-01", "2024-01-28")


def test_list_sitemaps():
    service = MagicMock()
    service.sitemaps().list().execute.return_value = {
        "sitemap": [
            {
                "path": "https://example.com/sitemap.xml",
                "type": "sitemap",
                "lastSubmitted": "2024-01-01",
                "isPending": False,
                "isSitemapsIndex": False,
                "warnings": 0,
                "errors": 0,
            }
        ]
    }
    client = SearchConsoleClient(service, "https://example.com")
    result = client.list_sitemaps()
    assert len(result) == 1
    assert result[0]["path"] == "https://example.com/sitemap.xml"


def test_list_sitemaps_empty():
    service = MagicMock()
    service.sitemaps().list().execute.return_value = {}
    client = SearchConsoleClient(service, "https://example.com")
    result = client.list_sitemaps()
    assert result == []


def test_list_sitemaps_failure():
    service = MagicMock()
    service.sitemaps().list().execute.side_effect = HttpError(
        Response({"status": "403"}), b"forbidden"
    )
    client = SearchConsoleClient(service, "https://example.com")
    with pytest.raises(APIError, match="Sitemap list failed"):
        client.list_sitemaps()


def test_get_sitemap():
    service = MagicMock()
    service.sitemaps().get().execute.return_value = {
        "path": "https://example.com/sitemap.xml",
        "type": "sitemap",
        "lastSubmitted": "2024-01-01",
        "contents": [{"type": "web", "submitted": 100, "indexed": 95}],
    }
    client = SearchConsoleClient(service, "https://example.com")
    result = client.get_sitemap("https://example.com/sitemap.xml")
    assert result["path"] == "https://example.com/sitemap.xml"
    assert len(result["contents"]) == 1
    assert result["contents"][0]["submitted"] == 100


def test_get_sitemap_contents():
    service = MagicMock()
    service.sitemaps().get().execute.return_value = {
        "path": "https://example.com/sitemap.xml",
        "type": "sitemap",
        "contents": [
            {"type": "web", "submitted": 50, "indexed": 45},
            {"type": "image", "submitted": 20, "indexed": 18},
        ],
    }
    client = SearchConsoleClient(service, "https://example.com")
    result = client.get_sitemap("https://example.com/sitemap.xml")
    assert len(result["contents"]) == 2


def test_get_sitemap_failure():
    service = MagicMock()
    service.sitemaps().get().execute.side_effect = HttpError(
        Response({"status": "404"}), b"not found"
    )
    client = SearchConsoleClient(service, "https://example.com")
    with pytest.raises(APIError, match="Sitemap get failed"):
        client.get_sitemap("https://example.com/sitemap.xml")


def test_site_url_property():
    service = MagicMock()
    client = SearchConsoleClient(service, "https://example.com")
    assert client.site_url == "https://example.com"
