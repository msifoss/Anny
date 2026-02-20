from fastapi import APIRouter, Depends, Query, Security
from fastapi.responses import StreamingResponse

from anny.clients.ga4 import GA4Client
from anny.clients.search_console import SearchConsoleClient
from anny.core.dependencies import get_ga4_client, get_search_console_client, verify_api_key
from anny.core.services import export_service, ga4_service, search_console_service

router = APIRouter(prefix="/api/export", tags=["Export"])


def _stream(data: bytes, filename: str, export_format: str) -> StreamingResponse:
    if export_format == "csv":
        media = "text/csv; charset=utf-8"
        filename = f"{filename}.csv"
    else:
        media = "application/json; charset=utf-8"
        filename = f"{filename}.json"

    return StreamingResponse(
        iter([data]),
        media_type=media,
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/ga4/report")
async def export_ga4_report(
    metrics: str = "sessions,totalUsers",
    dimensions: str = "date",
    date_range: str = "last_28_days",
    limit: int = 10,
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: GA4Client = Depends(get_ga4_client),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_report(client, metrics, dimensions, date_range, limit)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "ga4-report", export_format)


@router.get("/ga4/top-pages")
async def export_ga4_top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: GA4Client = Depends(get_ga4_client),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_top_pages(client, date_range=date_range, limit=limit)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "ga4-top-pages", export_format)


@router.get("/ga4/traffic-summary")
async def export_ga4_traffic_summary(
    date_range: str = "last_28_days",
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: GA4Client = Depends(get_ga4_client),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_traffic_summary(client, date_range=date_range)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "ga4-traffic-summary", export_format)


@router.get("/search-console/query")
async def export_sc_query(
    dimensions: str = "query",
    date_range: str = "last_28_days",
    row_limit: int = 10,
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_search_analytics(client, dimensions, date_range, row_limit)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "sc-query", export_format)


@router.get("/search-console/top-queries")
async def export_sc_top_queries(
    date_range: str = "last_28_days",
    limit: int = 10,
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_queries(client, date_range=date_range, limit=limit)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "sc-top-queries", export_format)


@router.get("/search-console/top-pages")
async def export_sc_top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    export_format: str = Query("csv", alias="format", pattern="^(csv|json)$"),
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_pages(client, date_range=date_range, limit=limit)
    data = export_service.to_csv(rows) if export_format == "csv" else export_service.to_json(rows)
    return _stream(data, "sc-top-pages", export_format)
