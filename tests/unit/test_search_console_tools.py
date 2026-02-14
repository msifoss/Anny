from unittest.mock import MagicMock, patch

from anny.core.formatting import format_table
from anny.core.services import search_console_service


def test_search_console_query_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [
            {
                "query": "python tutorial",
                "clicks": 150,
                "impressions": 3000,
                "ctr": 5.0,
                "position": 4.2,
            }
        ]
        rows = search_console_service.get_search_analytics(mock_client)
        result = format_table(rows)

    assert "python tutorial" in result
    assert "150" in result


def test_search_console_top_queries_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"query": "fastapi", "clicks": 200}]
        rows = search_console_service.get_top_queries(mock_client)
        result = format_table(rows)

    assert "fastapi" in result


def test_search_console_top_pages_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"page": "/docs", "clicks": 300}]
        rows = search_console_service.get_top_pages(mock_client)
        result = format_table(rows)

    assert "/docs" in result


def test_search_console_summary_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.search_console_service.parse_date_range",
        return_value=("2024-01-01", "2024-01-28"),
    ):
        mock_client.query.return_value = [{"clicks": 5000, "impressions": 100000}]
        rows = search_console_service.get_performance_summary(mock_client)
        result = format_table(rows)

    assert "5000" in result
