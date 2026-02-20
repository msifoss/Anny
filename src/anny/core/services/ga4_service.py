from __future__ import annotations

from anny.clients.ga4 import GA4Client
from anny.core.cache import QueryCache
from anny.core.date_utils import parse_date_range


def get_report(
    client: GA4Client,
    metrics: str = "sessions,totalUsers",
    dimensions: str = "date",
    date_range: str = "last_28_days",
    limit: int = 10,
    cache: QueryCache | None = None,
) -> list[dict]:
    """Run a custom GA4 report."""
    metric_list = [m.strip() for m in metrics.split(",") if m.strip()]
    dimension_list = [d.strip() for d in dimensions.split(",") if d.strip()]
    if not metric_list:
        raise ValueError("At least one metric is required")
    if not dimension_list:
        raise ValueError("At least one dimension is required")
    start_date, end_date = parse_date_range(date_range)

    if cache:
        key = cache.make_key(
            "ga4_report",
            {
                "metrics": metric_list,
                "dimensions": dimension_list,
                "start": start_date,
                "end": end_date,
                "limit": limit,
            },
        )
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.run_report(
        metrics=metric_list,
        dimensions=dimension_list,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    if cache:
        cache.put(key, rows, api="ga4", summary=f"report {metrics}")

    return rows


def get_top_pages(
    client: GA4Client,
    date_range: str = "last_28_days",
    limit: int = 10,
    cache: QueryCache | None = None,
) -> list[dict]:
    """Get top pages by screen page views."""
    start_date, end_date = parse_date_range(date_range)

    if cache:
        key = cache.make_key(
            "ga4_top_pages", {"start": start_date, "end": end_date, "limit": limit}
        )
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.run_report(
        metrics=["screenPageViews", "sessions", "totalUsers"],
        dimensions=["pagePath"],
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    if cache:
        cache.put(key, rows, api="ga4", summary="top_pages")

    return rows


def get_traffic_summary(
    client: GA4Client,
    date_range: str = "last_28_days",
    cache: QueryCache | None = None,
) -> list[dict]:
    """Get a traffic summary with key metrics by session source."""
    start_date, end_date = parse_date_range(date_range)

    if cache:
        key = cache.make_key("ga4_traffic_summary", {"start": start_date, "end": end_date})
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.run_report(
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"],
        dimensions=["sessionSource"],
        start_date=start_date,
        end_date=end_date,
        limit=10,
    )

    if cache:
        cache.put(key, rows, api="ga4", summary="traffic_summary")

    return rows


def get_realtime_report(
    client: GA4Client,
    metrics: str = "activeUsers",
    dimensions: str = "",
) -> list[dict]:
    """Run a GA4 realtime report."""
    metric_list = [m.strip() for m in metrics.split(",") if m.strip()]
    if not metric_list:
        raise ValueError("At least one metric is required")
    dimension_list = [d.strip() for d in dimensions.split(",") if d.strip()] or None

    return client.run_realtime_report(
        metrics=metric_list,
        dimensions=dimension_list,
    )
