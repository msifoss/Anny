from unittest.mock import MagicMock, patch

from anny.core.formatting import format_table
from anny.core.services import ga4_service
from anny.mcp_server import mcp


def test_ga4_report_tool_flow():
    """Test the same logic that the ga4_report MCP tool executes."""
    mock_client = MagicMock()
    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"date": "2024-01-01", "sessions": "100"}]
        rows = ga4_service.get_report(mock_client, metrics="sessions", dimensions="date")
        result = format_table(rows)

    assert "date" in result
    assert "100" in result


def test_ga4_top_pages_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"pagePath": "/home", "screenPageViews": "500"}]
        rows = ga4_service.get_top_pages(mock_client)
        result = format_table(rows)

    assert "/home" in result
    assert "500" in result


def test_ga4_traffic_summary_tool_flow():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = [{"sessionSource": "google", "sessions": "300"}]
        rows = ga4_service.get_traffic_summary(mock_client)
        result = format_table(rows)

    assert "google" in result
    assert "300" in result


def test_ga4_realtime_tool_flow():
    mock_client = MagicMock()
    mock_client.run_realtime_report.return_value = [{"activeUsers": "42"}]
    rows = ga4_service.get_realtime_report(mock_client, metrics="activeUsers")
    result = format_table(rows)

    assert "activeUsers" in result
    assert "42" in result


def test_ga4_report_no_data():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = []
        rows = ga4_service.get_report(mock_client, metrics="sessions", dimensions="date")
        result = format_table(rows)

    assert result == "No data available."


@patch("anny.mcp_server.get_query_cache")
@patch("anny.mcp_server.get_ga4_client")
def test_ga4_report_tool_bad_date_range(mock_get_client, mock_get_cache):
    """MCP tool should return a friendly error for an invalid date range."""
    mock_get_client.return_value = MagicMock()
    mock_get_cache.return_value = MagicMock()

    # Find the ga4_report tool's underlying function
    tool = None
    # pylint: disable=protected-access
    for t in mcp._tool_manager._tools.values():
        if t.name == "ga4_report":
            tool = t
            break
    assert tool is not None, "ga4_report tool not found"
    result = tool.fn(date_range="not_a_range")
    assert "Invalid input" in result
