from unittest.mock import MagicMock, patch

from anny.core.formatting import format_table
from anny.core.services import ga4_service


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


def test_ga4_report_no_data():
    mock_client = MagicMock()
    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        mock_client.run_report.return_value = []
        rows = ga4_service.get_report(mock_client, metrics="sessions", dimensions="date")
        result = format_table(rows)

    assert result == "No data available."
