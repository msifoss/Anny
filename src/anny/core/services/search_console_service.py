from __future__ import annotations

from anny.clients.search_console import SearchConsoleClient
from anny.core.cache import QueryCache
from anny.core.date_utils import parse_date_range
from anny.core.exceptions import ValidationError


def get_search_analytics(
    client: SearchConsoleClient,
    dimensions: str = "query",
    date_range: str = "last_28_days",
    row_limit: int = 10,
    cache: QueryCache | None = None,
) -> list[dict]:
    """Run a custom Search Console query."""
    dimension_list = [d.strip() for d in dimensions.split(",") if d.strip()]
    if not dimension_list:
        raise ValidationError("At least one dimension is required")
    try:
        start_date, end_date = parse_date_range(date_range)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    if cache:
        key = cache.make_key(
            "sc_query",
            {
                "dimensions": dimension_list,
                "start": start_date,
                "end": end_date,
                "limit": row_limit,
            },
        )
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=dimension_list,
        row_limit=row_limit,
    )

    if cache:
        cache.put(key, rows, api="search_console", summary=f"query {dimensions}")

    return rows


def get_top_queries(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
    limit: int = 10,
    cache: QueryCache | None = None,
) -> list[dict]:
    """Get top search queries by clicks."""
    try:
        start_date, end_date = parse_date_range(date_range)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    if cache:
        key = cache.make_key(
            "sc_top_queries", {"start": start_date, "end": end_date, "limit": limit}
        )
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=["query"],
        row_limit=limit,
    )

    if cache:
        cache.put(key, rows, api="search_console", summary="top_queries")

    return rows


def get_top_pages(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
    limit: int = 10,
    cache: QueryCache | None = None,
) -> list[dict]:
    """Get top pages by clicks."""
    try:
        start_date, end_date = parse_date_range(date_range)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    if cache:
        key = cache.make_key("sc_top_pages", {"start": start_date, "end": end_date, "limit": limit})
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=["page"],
        row_limit=limit,
    )

    if cache:
        cache.put(key, rows, api="search_console", summary="top_pages")

    return rows


def get_performance_summary(
    client: SearchConsoleClient,
    date_range: str = "last_28_days",
    cache: QueryCache | None = None,
) -> list[dict]:
    """Get overall performance summary (no dimension breakdown)."""
    try:
        start_date, end_date = parse_date_range(date_range)
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    if cache:
        key = cache.make_key("sc_summary", {"start": start_date, "end": end_date})
        cached = cache.get(key)
        if cached is not None:
            return cached

    rows = client.query(
        start_date=start_date,
        end_date=end_date,
        dimensions=None,
        row_limit=1,
    )

    if cache:
        cache.put(key, rows, api="search_console", summary="performance_summary")

    return rows


def get_sitemaps(client: SearchConsoleClient) -> list[dict]:
    """List all sitemaps for the site."""
    return client.list_sitemaps()


def get_sitemap_details(client: SearchConsoleClient, feedpath: str) -> dict:
    """Get details for a specific sitemap."""
    return client.get_sitemap(feedpath)
