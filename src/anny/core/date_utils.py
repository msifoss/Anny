from datetime import date, timedelta

NAMED_RANGES = {
    "today": 0,
    "yesterday": 1,
    "last_7_days": 7,
    "last_14_days": 14,
    "last_28_days": 28,
    "last_30_days": 30,
    "last_90_days": 90,
    "last_365_days": 365,
}


def parse_date_range(date_range: str) -> tuple[str, str]:
    """Convert a named date range to (start_date, end_date) strings for Google APIs.

    Supports named ranges like 'last_28_days', 'today', 'yesterday',
    or explicit 'YYYY-MM-DD,YYYY-MM-DD' format.

    Returns GA4-style date strings: 'YYYY-MM-DD'.
    """
    if "," in date_range:
        parts = date_range.split(",", 1)
        return parts[0].strip(), parts[1].strip()

    key = date_range.lower().strip()
    if key not in NAMED_RANGES:
        raise ValueError(
            f"Unknown date range: '{date_range}'. "
            f"Use one of: {', '.join(NAMED_RANGES.keys())} or 'YYYY-MM-DD,YYYY-MM-DD'"
        )

    days = NAMED_RANGES[key]
    today = date.today()

    if key == "today":
        return today.isoformat(), today.isoformat()
    if key == "yesterday":
        yesterday = today - timedelta(days=1)
        return yesterday.isoformat(), yesterday.isoformat()

    start = today - timedelta(days=days)
    return start.isoformat(), today.isoformat()
