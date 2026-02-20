from unittest.mock import MagicMock

import pytest
from google.api_core.exceptions import GoogleAPICallError

from anny.clients.ga4 import GA4Client
from anny.core.exceptions import APIError


def _make_mock_response(rows_data):
    """Build a mock RunReportResponse with the given rows.

    rows_data: list of (dimension_values, metric_values) tuples
    """
    response = MagicMock()
    mock_rows = []
    for dims, mets in rows_data:
        row = MagicMock()
        row.dimension_values = [MagicMock(value=v) for v in dims]
        row.metric_values = [MagicMock(value=v) for v in mets]
        mock_rows.append(row)
    response.rows = mock_rows
    return response


def test_run_report_flattens_response():
    mock_api = MagicMock()
    mock_response = _make_mock_response(
        [
            (["2024-01-01"], ["100", "50"]),
            (["2024-01-02"], ["200", "75"]),
        ]
    )
    mock_api.run_report.return_value = mock_response

    client = GA4Client(mock_api, "123456")
    rows = client.run_report(
        metrics=["sessions", "totalUsers"],
        dimensions=["date"],
        start_date="2024-01-01",
        end_date="2024-01-02",
    )

    assert len(rows) == 2
    assert rows[0] == {"date": "2024-01-01", "sessions": "100", "totalUsers": "50"}
    assert rows[1] == {"date": "2024-01-02", "sessions": "200", "totalUsers": "75"}


def test_run_report_empty_response():
    mock_api = MagicMock()
    mock_api.run_report.return_value = MagicMock(rows=[])

    client = GA4Client(mock_api, "123456")
    rows = client.run_report(
        metrics=["sessions"],
        dimensions=["date"],
        start_date="2024-01-01",
        end_date="2024-01-01",
    )
    assert not rows


def test_run_report_api_failure():
    mock_api = MagicMock()
    mock_api.run_report.side_effect = GoogleAPICallError("connection failed")

    client = GA4Client(mock_api, "123456")
    with pytest.raises(APIError, match="GA4 report failed"):
        client.run_report(
            metrics=["sessions"],
            dimensions=["date"],
            start_date="2024-01-01",
            end_date="2024-01-01",
        )


def test_run_realtime_report():
    mock_api = MagicMock()
    mock_response = _make_mock_response(
        [
            (["US"], ["42"]),
            (["UK"], ["15"]),
        ]
    )
    mock_api.run_realtime_report.return_value = mock_response

    client = GA4Client(mock_api, "123456")
    rows = client.run_realtime_report(
        metrics=["activeUsers"],
        dimensions=["country"],
    )

    assert len(rows) == 2
    assert rows[0] == {"country": "US", "activeUsers": "42"}


def test_run_realtime_report_no_dimensions():
    mock_api = MagicMock()
    mock_response = _make_mock_response(
        [
            ([], ["42"]),
        ]
    )
    mock_api.run_realtime_report.return_value = mock_response

    client = GA4Client(mock_api, "123456")
    rows = client.run_realtime_report(metrics=["activeUsers"])

    assert len(rows) == 1
    assert rows[0] == {"activeUsers": "42"}


def test_run_realtime_report_api_failure():
    mock_api = MagicMock()
    mock_api.run_realtime_report.side_effect = GoogleAPICallError("connection failed")

    client = GA4Client(mock_api, "123456")
    with pytest.raises(APIError, match="GA4 realtime report failed"):
        client.run_realtime_report(metrics=["activeUsers"])


def test_run_realtime_report_minute_ranges():
    mock_api = MagicMock()
    mock_api.run_realtime_report.return_value = MagicMock(rows=[])

    client = GA4Client(mock_api, "123456")
    client.run_realtime_report(
        metrics=["activeUsers"],
        minute_ranges_start=0,
        minute_ranges_end=10,
    )

    call_args = mock_api.run_realtime_report.call_args[0][0]
    assert call_args.minute_ranges[0].start_minutes_ago == 10
    assert call_args.minute_ranges[0].end_minutes_ago == 0


def test_property_id_strips_prefix():
    mock_api = MagicMock()
    mock_api.run_report.return_value = MagicMock(rows=[])

    client = GA4Client(mock_api, "properties/123456")
    client.run_report(
        metrics=["sessions"],
        dimensions=["date"],
        start_date="2024-01-01",
        end_date="2024-01-01",
    )

    call_args = mock_api.run_report.call_args[0][0]
    assert call_args.property == "properties/123456"
