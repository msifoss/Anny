from fastapi import APIRouter, Depends, Security

from anny.api.models import GA4ReportRequest, GA4ReportResponse
from anny.clients.ga4 import GA4Client
from anny.core.cache import QueryCache
from anny.core.dependencies import get_ga4_client, get_query_cache, verify_api_key
from anny.core.services import ga4_service

router = APIRouter(prefix="/api/ga4", tags=["GA4"])


@router.post("/report", response_model=GA4ReportResponse)
async def report(
    body: GA4ReportRequest,
    client: GA4Client = Depends(get_ga4_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_report(
        client,
        metrics=body.metrics,
        dimensions=body.dimensions,
        date_range=body.date_range,
        limit=body.limit,
        cache=cache,
    )
    return GA4ReportResponse(rows=rows, row_count=len(rows))


@router.get("/top-pages", response_model=GA4ReportResponse)
async def top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: GA4Client = Depends(get_ga4_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_top_pages(client, date_range=date_range, limit=limit, cache=cache)
    return GA4ReportResponse(rows=rows, row_count=len(rows))


@router.get("/traffic-summary", response_model=GA4ReportResponse)
async def traffic_summary(
    date_range: str = "last_28_days",
    client: GA4Client = Depends(get_ga4_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_traffic_summary(client, date_range=date_range, cache=cache)
    return GA4ReportResponse(rows=rows, row_count=len(rows))


@router.get("/realtime", response_model=GA4ReportResponse)
async def realtime(
    metrics: str = "activeUsers",
    dimensions: str = "",
    client: GA4Client = Depends(get_ga4_client),
    _: str = Security(verify_api_key),
):
    rows = ga4_service.get_realtime_report(client, metrics=metrics, dimensions=dimensions)
    return GA4ReportResponse(rows=rows, row_count=len(rows))
