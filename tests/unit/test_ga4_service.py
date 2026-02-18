from unittest.mock import MagicMock, patch

import pytest

from anny.core.services import ga4_service


def test_get_report_calls_client():
    mock_client = MagicMock()
    mock_client.run_report.return_value = [{"date": "2024-01-01", "sessions": "100"}]

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        rows = ga4_service.get_report(mock_client, metrics="sessions", dimensions="date")

    mock_client.run_report.assert_called_once_with(
        metrics=["sessions"],
        dimensions=["date"],
        start_date="2024-01-01",
        end_date="2024-01-28",
        limit=10,
    )
    assert len(rows) == 1


def test_get_report_splits_multiple_metrics():
    mock_client = MagicMock()
    mock_client.run_report.return_value = []

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        ga4_service.get_report(
            mock_client, metrics="sessions, totalUsers", dimensions="date, pagePath"
        )

    call_args = mock_client.run_report.call_args
    assert call_args.kwargs["metrics"] == ["sessions", "totalUsers"]
    assert call_args.kwargs["dimensions"] == ["date", "pagePath"]


def test_get_top_pages():
    mock_client = MagicMock()
    mock_client.run_report.return_value = [{"pagePath": "/", "screenPageViews": "500"}]

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        rows = ga4_service.get_top_pages(mock_client)

    call_args = mock_client.run_report.call_args
    assert "screenPageViews" in call_args.kwargs["metrics"]
    assert call_args.kwargs["dimensions"] == ["pagePath"]
    assert len(rows) == 1


def test_get_traffic_summary():
    mock_client = MagicMock()
    mock_client.run_report.return_value = [{"sessionSource": "google", "sessions": "300"}]

    with patch(
        "anny.core.services.ga4_service.parse_date_range", return_value=("2024-01-01", "2024-01-28")
    ):
        rows = ga4_service.get_traffic_summary(mock_client)

    call_args = mock_client.run_report.call_args
    assert "sessions" in call_args.kwargs["metrics"]
    assert call_args.kwargs["dimensions"] == ["sessionSource"]
    assert len(rows) == 1


def test_get_report_rejects_empty_metrics():
    mock_client = MagicMock()
    with pytest.raises(ValueError, match="metric"):
        ga4_service.get_report(mock_client, metrics="", dimensions="date")


def test_get_report_rejects_empty_dimensions():
    mock_client = MagicMock()
    with pytest.raises(ValueError, match="dimension"):
        ga4_service.get_report(mock_client, metrics="sessions", dimensions="")
