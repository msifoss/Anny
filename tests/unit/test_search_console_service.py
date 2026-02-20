from unittest.mock import MagicMock, patch

import pytest

from anny.core.services import search_console_service


def test_get_search_analytics():
    mock_client = MagicMock()
    mock_client.query.return_value = [{"query": "test", "clicks": 100}]

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        rows = search_console_service.get_search_analytics(mock_client)

    mock_client.query.assert_called_once_with(
        start_date="2024-01-01",
        end_date="2024-01-28",
        dimensions=["query"],
        row_limit=10,
    )
    assert len(rows) == 1


def test_get_search_analytics_multiple_dimensions():
    mock_client = MagicMock()
    mock_client.query.return_value = []

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        search_console_service.get_search_analytics(mock_client, dimensions="query, page")

    call_args = mock_client.query.call_args
    assert call_args.kwargs["dimensions"] == ["query", "page"]


def test_get_top_queries():
    mock_client = MagicMock()
    mock_client.query.return_value = [{"query": "python", "clicks": 200}]

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        rows = search_console_service.get_top_queries(mock_client)

    call_args = mock_client.query.call_args
    assert call_args.kwargs["dimensions"] == ["query"]
    assert len(rows) == 1


def test_get_top_pages():
    mock_client = MagicMock()
    mock_client.query.return_value = [{"page": "/", "clicks": 300}]

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        rows = search_console_service.get_top_pages(mock_client)

    call_args = mock_client.query.call_args
    assert call_args.kwargs["dimensions"] == ["page"]
    assert len(rows) == 1


def test_get_performance_summary():
    mock_client = MagicMock()
    mock_client.query.return_value = [{"clicks": 5000, "impressions": 100000}]

    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        rows = search_console_service.get_performance_summary(mock_client)

    call_args = mock_client.query.call_args
    assert call_args.kwargs["dimensions"] is None
    assert len(rows) == 1


def test_get_sitemaps():
    mock_client = MagicMock()
    mock_client.list_sitemaps.return_value = [
        {"path": "https://example.com/sitemap.xml", "type": "sitemap"}
    ]
    rows = search_console_service.get_sitemaps(mock_client)
    mock_client.list_sitemaps.assert_called_once()
    assert len(rows) == 1


def test_get_sitemap_details():
    mock_client = MagicMock()
    mock_client.get_sitemap.return_value = {
        "path": "https://example.com/sitemap.xml",
        "type": "sitemap",
        "contents": [{"type": "web", "submitted": 50}],
    }
    result = search_console_service.get_sitemap_details(
        mock_client, "https://example.com/sitemap.xml"
    )
    mock_client.get_sitemap.assert_called_once_with("https://example.com/sitemap.xml")
    assert result["path"] == "https://example.com/sitemap.xml"


def test_get_search_analytics_rejects_empty_dimensions():
    mock_client = MagicMock()
    with pytest.raises(ValueError, match="dimension"):
        search_console_service.get_search_analytics(mock_client, dimensions="")
