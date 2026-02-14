from anny.clients.ga4 import GA4Client
from anny.core.date_utils import parse_date_range


def get_report(
    client: GA4Client,
    metrics: str = "sessions,totalUsers",
    dimensions: str = "date",
    date_range: str = "last_28_days",
    limit: int = 10,
) -> list[dict]:
    """Run a custom GA4 report."""
    metric_list = [m.strip() for m in metrics.split(",")]
    dimension_list = [d.strip() for d in dimensions.split(",")]
    start_date, end_date = parse_date_range(date_range)

    return client.run_report(
        metrics=metric_list,
        dimensions=dimension_list,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


def get_top_pages(
    client: GA4Client,
    date_range: str = "last_28_days",
    limit: int = 10,
) -> list[dict]:
    """Get top pages by screen page views."""
    start_date, end_date = parse_date_range(date_range)

    return client.run_report(
        metrics=["screenPageViews", "sessions", "totalUsers"],
        dimensions=["pagePath"],
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


def get_traffic_summary(
    client: GA4Client,
    date_range: str = "last_28_days",
) -> list[dict]:
    """Get a traffic summary with key metrics by session source."""
    start_date, end_date = parse_date_range(date_range)

    return client.run_report(
        metrics=["sessions", "totalUsers", "screenPageViews", "bounceRate"],
        dimensions=["sessionSource"],
        start_date=start_date,
        end_date=end_date,
        limit=10,
    )
