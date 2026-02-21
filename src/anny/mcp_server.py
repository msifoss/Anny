from fastmcp import FastMCP

from anny.core.dependencies import (
    get_ga4_client,
    get_memory_store,
    get_query_cache,
    get_search_console_client,
    get_tag_manager_client,
)
from anny.core.constants import MAX_LIMIT, MAX_ROW_LIMIT
from anny.core.formatting import format_table
from anny.core.services import (
    cache_service,
    ga4_service,
    memory_service,
    search_console_service,
    tag_manager_service,
)

mcp = FastMCP("Anny")


@mcp.tool()
def ping() -> str:
    """Check that the Anny MCP server is running."""
    return "pong"


@mcp.tool()
def ga4_report(
    metrics: str = "sessions,totalUsers",
    dimensions: str = "date",
    date_range: str = "last_28_days",
    limit: int = 10,
) -> str:
    """Run a custom Google Analytics 4 report.

    Args:
        metrics: Comma-separated GA4 metrics (e.g. sessions,totalUsers,screenPageViews)
        dimensions: Comma-separated GA4 dimensions (e.g. date,pagePath,sessionSource)
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    limit = max(1, min(limit, MAX_LIMIT))
    client = get_ga4_client()
    cache = get_query_cache()
    rows = ga4_service.get_report(client, metrics, dimensions, date_range, limit, cache=cache)
    return format_table(rows)


@mcp.tool()
def ga4_top_pages(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get the top pages by page views from Google Analytics 4.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    limit = max(1, min(limit, MAX_LIMIT))
    client = get_ga4_client()
    cache = get_query_cache()
    rows = ga4_service.get_top_pages(client, date_range, limit, cache=cache)
    return format_table(rows)


@mcp.tool()
def ga4_traffic_summary(date_range: str = "last_28_days") -> str:
    """Get a traffic summary by source from Google Analytics 4.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
    """
    client = get_ga4_client()
    cache = get_query_cache()
    rows = ga4_service.get_traffic_summary(client, date_range, cache=cache)
    return format_table(rows)


@mcp.tool()
def ga4_realtime(
    metrics: str = "activeUsers",
    dimensions: str = "",
) -> str:
    """Get realtime data from Google Analytics 4.

    Args:
        metrics: Comma-separated GA4 realtime metrics (e.g. activeUsers,screenPageViews)
        dimensions: Comma-separated dimensions (e.g. unifiedScreenName,country) — optional
    """
    client = get_ga4_client()
    rows = ga4_service.get_realtime_report(client, metrics, dimensions)
    return format_table(rows)


# --- Search Console Tools ---


@mcp.tool()
def search_console_query(
    dimensions: str = "query",
    date_range: str = "last_28_days",
    row_limit: int = 10,
) -> str:
    """Run a custom Google Search Console search analytics query.

    Args:
        dimensions: Comma-separated dimensions (query, page, date, country, device)
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        row_limit: Max rows to return (1-1000)
    """
    row_limit = max(1, min(row_limit, MAX_ROW_LIMIT))
    client = get_search_console_client()
    cache = get_query_cache()
    rows = search_console_service.get_search_analytics(
        client, dimensions, date_range, row_limit, cache=cache
    )
    return format_table(rows)


@mcp.tool()
def search_console_top_queries(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get top search queries from Google Search Console.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    limit = max(1, min(limit, MAX_LIMIT))
    client = get_search_console_client()
    cache = get_query_cache()
    rows = search_console_service.get_top_queries(client, date_range, limit, cache=cache)
    return format_table(rows)


@mcp.tool()
def search_console_top_pages(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get top pages from Google Search Console by clicks.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    limit = max(1, min(limit, MAX_LIMIT))
    client = get_search_console_client()
    cache = get_query_cache()
    rows = search_console_service.get_top_pages(client, date_range, limit, cache=cache)
    return format_table(rows)


@mcp.tool()
def search_console_summary(date_range: str = "last_28_days") -> str:
    """Get overall search performance summary from Google Search Console.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
    """
    client = get_search_console_client()
    cache = get_query_cache()
    rows = search_console_service.get_performance_summary(client, date_range, cache=cache)
    return format_table(rows)


@mcp.tool()
def search_console_sitemaps() -> str:
    """List all sitemaps submitted to Google Search Console."""
    client = get_search_console_client()
    rows = search_console_service.get_sitemaps(client)
    return format_table(rows)


@mcp.tool()
def search_console_sitemap_details(feedpath: str) -> str:
    """Get details for a specific sitemap from Google Search Console.

    Args:
        feedpath: The sitemap URL (e.g. "https://example.com/sitemap.xml")
    """
    client = get_search_console_client()
    details = search_console_service.get_sitemap_details(client, feedpath)
    parts = [
        f"Path: {details['path']}",
        f"Type: {details['type']}",
        f"Last submitted: {details.get('lastSubmitted', 'N/A')}",
        f"Pending: {details.get('isPending', False)}",
        f"Index: {details.get('isSitemapsIndex', False)}",
        f"Warnings: {details.get('warnings', 0)}",
        f"Errors: {details.get('errors', 0)}",
    ]
    if details.get("contents"):
        parts.append(f"\nContents:\n{format_table(details['contents'])}")
    return "\n".join(parts)


# --- Cache Tools ---


@mcp.tool()
def cache_status() -> str:
    """Get the status of the query cache (entries, TTL, capacity)."""
    cache = get_query_cache()
    status = cache_service.get_cache_status(cache)
    return (
        f"Cache: {status['active_entries']}/{status['max_entries']} active entries, "
        f"TTL {status['ttl_seconds']}s"
    )


@mcp.tool()
def clear_cache() -> str:
    """Clear all cached query results."""
    cache = get_query_cache()
    result = cache_service.clear_cache(cache)
    return f"Cleared {result['cleared']} cached entries."


# --- Tag Manager Tools ---


@mcp.tool()
def gtm_list_accounts() -> str:
    """List all Google Tag Manager accounts accessible by the service account."""
    client = get_tag_manager_client()
    rows = tag_manager_service.get_accounts(client)
    return format_table(rows)


@mcp.tool()
def gtm_list_containers(account_id: str) -> str:
    """List containers for a Google Tag Manager account.

    Args:
        account_id: The GTM account ID (e.g. "123456")
    """
    client = get_tag_manager_client()
    rows = tag_manager_service.get_containers(client, account_id)
    return format_table(rows)


@mcp.tool()
def gtm_container_setup(container_path: str) -> str:
    """Get a summary of tags, triggers, and variables in a GTM container.

    Args:
        container_path: The GTM container path (e.g. "accounts/123/containers/456")
    """
    client = get_tag_manager_client()
    setup = tag_manager_service.get_container_setup(client, container_path)
    parts = [
        f"Tags ({setup['tag_count']}):",
        format_table(setup["tags"]) if setup["tags"] else "  (none)",
        "",
        f"Triggers ({setup['trigger_count']}):",
        format_table(setup["triggers"]) if setup["triggers"] else "  (none)",
        "",
        f"Variables ({setup['variable_count']}):",
        format_table(setup["variables"]) if setup["variables"] else "  (none)",
    ]
    return "\n".join(parts)


@mcp.tool()
def gtm_list_tags(container_path: str) -> str:
    """List all tags in a GTM container.

    Args:
        container_path: The GTM container path (e.g. "accounts/123/containers/456")
    """
    client = get_tag_manager_client()
    rows = client.list_tags(container_path)
    return format_table(rows)


# --- Memory Tools ---


@mcp.tool()
def save_insight(text: str, source: str = "manual", tags: str = "") -> str:
    """Save a key analytics finding for future reference.

    Args:
        text: The insight text (e.g. "Organic traffic dropped 15% after site migration")
        source: Where this insight came from (ga4, search_console, gtm, manual)
        tags: Comma-separated tags for categorization (e.g. "traffic,seo")
    """
    store = get_memory_store()
    insight = memory_service.save_insight(store, text, source, tags)
    return f"Saved insight {insight['id']}: {insight['text']}"


@mcp.tool()
def list_insights() -> str:
    """List all saved analytics insights."""
    store = get_memory_store()
    items = memory_service.list_insights(store)
    if not items:
        return "No saved insights."
    rows = [
        {"id": i["id"], "source": i["source"], "tags": ", ".join(i["tags"]), "text": i["text"]}
        for i in items
    ]
    return format_table(rows)


@mcp.tool()
def delete_insight(insight_id: str) -> str:
    """Delete a saved insight by its ID.

    Args:
        insight_id: The insight ID (e.g. "ins_20260216_143022_a1b2")
    """
    store = get_memory_store()
    if memory_service.delete_insight(store, insight_id):
        return f"Deleted insight {insight_id}."
    return f"Insight {insight_id} not found."


@mcp.tool()
def add_to_watchlist(
    page_path: str,
    label: str,
    baseline_sessions: int | None = None,
    baseline_pageviews: int | None = None,
) -> str:
    """Add a page to the watchlist to track over time.

    Args:
        page_path: The page path to watch (e.g. "/pricing")
        label: A human-readable label (e.g. "Pricing page")
        baseline_sessions: Optional baseline session count for comparison
        baseline_pageviews: Optional baseline pageview count for comparison
    """
    store = get_memory_store()
    item = memory_service.add_to_watchlist(
        store, page_path, label, baseline_sessions, baseline_pageviews
    )
    return f"Added {item['id']}: watching {item['page_path']} ({item['label']})"


@mcp.tool()
def list_watchlist() -> str:
    """List all pages on the watchlist."""
    store = get_memory_store()
    items = memory_service.list_watchlist(store)
    if not items:
        return "Watchlist is empty."
    rows = [
        {
            "id": i["id"],
            "page_path": i["page_path"],
            "label": i["label"],
            "baseline": str(i["baseline"]) if i["baseline"] else "",
        }
        for i in items
    ]
    return format_table(rows)


@mcp.tool()
def remove_from_watchlist(item_id: str) -> str:
    """Remove a page from the watchlist.

    Args:
        item_id: The watchlist item ID (e.g. "wtc_20260216_143022_a1b2")
    """
    store = get_memory_store()
    if memory_service.remove_from_watchlist(store, item_id):
        return f"Removed {item_id} from watchlist."
    return f"Watchlist item {item_id} not found."


@mcp.tool()
def save_segment(name: str, description: str, filter_type: str, patterns: str) -> str:
    """Save a reusable filter segment for analytics queries.

    Args:
        name: Short segment name (e.g. "exclude-login-pages")
        description: What this segment does
        filter_type: Type of filter (exclude_pages, include_pages, exclude_queries, include_queries)
        patterns: Comma-separated URL or query patterns (e.g. "/login,/logout")
    """
    store = get_memory_store()
    segment = memory_service.save_segment(store, name, description, filter_type, patterns)
    return f"Saved segment {segment['id']}: {segment['name']} ({segment['filter_type']})"


@mcp.tool()
def list_segments() -> str:
    """List all saved filter segments."""
    store = get_memory_store()
    items = memory_service.list_segments(store)
    if not items:
        return "No saved segments."
    rows = [
        {
            "id": s["id"],
            "name": s["name"],
            "filter_type": s["filter_type"],
            "patterns": ", ".join(s["patterns"]),
        }
        for s in items
    ]
    return format_table(rows)


@mcp.tool()
def get_context() -> str:
    """Load all saved memory (insights, watchlist, segments) for session context.

    Call this at the start of a session to restore previous context.
    """
    store = get_memory_store()
    ctx = memory_service.get_context(store)
    parts = []
    summary = ctx["summary"]
    parts.append(
        f"Memory: {summary['total_insights']} insights, "
        f"{summary['total_watchlist']} watchlist items, "
        f"{summary['total_segments']} segments"
    )

    if ctx["insights"]:
        rows = [{"source": i["source"], "text": i["text"]} for i in ctx["insights"]]
        parts.append(f"\nInsights:\n{format_table(rows)}")

    if ctx["watchlist"]:
        rows = [{"page_path": w["page_path"], "label": w["label"]} for w in ctx["watchlist"]]
        parts.append(f"\nWatchlist:\n{format_table(rows)}")

    if ctx["segments"]:
        rows = [{"name": s["name"], "filter_type": s["filter_type"]} for s in ctx["segments"]]
        parts.append(f"\nSegments:\n{format_table(rows)}")

    return "\n".join(parts)
