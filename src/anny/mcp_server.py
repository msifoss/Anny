from fastmcp import FastMCP

from anny.core.dependencies import (
    get_ga4_client,
    get_search_console_client,
    get_tag_manager_client,
)
from anny.core.formatting import format_table
from anny.core.services import ga4_service, search_console_service, tag_manager_service

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
    client = get_ga4_client()
    rows = ga4_service.get_report(client, metrics, dimensions, date_range, limit)
    return format_table(rows)


@mcp.tool()
def ga4_top_pages(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get the top pages by page views from Google Analytics 4.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    client = get_ga4_client()
    rows = ga4_service.get_top_pages(client, date_range, limit)
    return format_table(rows)


@mcp.tool()
def ga4_traffic_summary(date_range: str = "last_28_days") -> str:
    """Get a traffic summary by source from Google Analytics 4.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
    """
    client = get_ga4_client()
    rows = ga4_service.get_traffic_summary(client, date_range)
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
    client = get_search_console_client()
    rows = search_console_service.get_search_analytics(client, dimensions, date_range, row_limit)
    return format_table(rows)


@mcp.tool()
def search_console_top_queries(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get top search queries from Google Search Console.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    client = get_search_console_client()
    rows = search_console_service.get_top_queries(client, date_range, limit)
    return format_table(rows)


@mcp.tool()
def search_console_top_pages(date_range: str = "last_28_days", limit: int = 10) -> str:
    """Get top pages from Google Search Console by clicks.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
        limit: Max rows to return (1-100)
    """
    client = get_search_console_client()
    rows = search_console_service.get_top_pages(client, date_range, limit)
    return format_table(rows)


@mcp.tool()
def search_console_summary(date_range: str = "last_28_days") -> str:
    """Get overall search performance summary from Google Search Console.

    Args:
        date_range: Named range (last_7_days, last_28_days, last_90_days) or YYYY-MM-DD,YYYY-MM-DD
    """
    client = get_search_console_client()
    rows = search_console_service.get_performance_summary(client, date_range)
    return format_table(rows)


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
