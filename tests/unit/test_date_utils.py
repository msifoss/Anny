from datetime import date, timedelta

import pytest

from anny.core.date_utils import parse_date_range


def test_explicit_range():
    start, end = parse_date_range("2024-01-01,2024-01-31")
    assert start == "2024-01-01"
    assert end == "2024-01-31"


def test_explicit_range_with_spaces():
    start, end = parse_date_range("2024-01-01 , 2024-01-31")
    assert start == "2024-01-01"
    assert end == "2024-01-31"


def test_today():
    start, end = parse_date_range("today")
    today = date.today().isoformat()
    assert start == today
    assert end == today


def test_yesterday():
    start, end = parse_date_range("yesterday")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    assert start == yesterday
    assert end == yesterday


def test_last_7_days():
    start, end = parse_date_range("last_7_days")
    expected_start = (date.today() - timedelta(days=7)).isoformat()
    assert start == expected_start
    assert end == date.today().isoformat()


def test_last_28_days():
    start, end = parse_date_range("last_28_days")
    expected_start = (date.today() - timedelta(days=28)).isoformat()
    assert start == expected_start
    assert end == date.today().isoformat()


def test_case_insensitive():
    start, _ = parse_date_range("Last_28_Days")
    expected_start = (date.today() - timedelta(days=28)).isoformat()
    assert start == expected_start


def test_unknown_range_raises():
    with pytest.raises(ValueError, match="Unknown date range"):
        parse_date_range("last_week")


def test_explicit_range_invalid_format():
    with pytest.raises(ValueError, match="Invalid date format"):
        parse_date_range("not-a-date,also-bad")


def test_explicit_range_start_after_end():
    with pytest.raises(ValueError, match="Start date .* is after end date"):
        parse_date_range("2024-12-31,2024-01-01")


def test_explicit_range_same_day():
    start, end = parse_date_range("2024-06-15,2024-06-15")
    assert start == "2024-06-15"
    assert end == "2024-06-15"
