from anny.clients.search_console import SearchConsoleClient
from anny.core.date_utils import parse_date_range


def get_search_analytics(
    client: SearchConsoleClient,
    dimensions: str = "query",
    date_range: str = "last_28_days",
    row_limit: int = 10,
) -> list[dict]:
    """Run a custom Search Console query."""
    dimension_list = [d.strip() for d in dimensions.split(",") if d.strip()]
    if not dimension_list:
        raise ValueError("At least one dimension is required")
    start_date, end_date = parse_date_range(date_range)

    return client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=dimension_list,
        row_limit=row_limit,
    )


def get_top_queries(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
    limit: int = 10,
) -> list[dict]:
    """Get top search queries by clicks."""
    start_date, end_date = parse_date_range(date_range)

    return client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=["query"],
        row_limit=limit,
    )


def get_top_pages(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
    limit: int = 10,
) -> list[dict]:
    """Get top pages by clicks."""
    start_date, end_date = parse_date_range(date_range)

    return client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=["page"],
        row_limit=limit,
    )


def get_performance_summary(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
) -> list[dict]:
    """Get overall performance summary (no dimension breakdown)."""
    start_date, end_date = parse_date_range(date_range)

    return client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=None,
        row_limit=1,
    )
