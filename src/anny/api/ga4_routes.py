from fastapi import APIRouter, Depends

from anny.api.models import GA4ReportRequest, GA4ReportResponse
from anny.clients.ga4 import GA4Client
from anny.core.dependencies import get_ga4_client
from anny.core.services import ga4_service

router = APIRouter(prefix="/api/ga4", tags=["GA4"])


@router.post("/report", response_model=GA4ReportResponse)
async def report(body: GA4ReportRequest, client: GA4Client = Depends(get_ga4_client)):
    rows = ga4_service.get_report(
        client,
        metrics=body.metrics,
        dimensions=body.dimensions,
        date_range=body.date_range,
        limit=body.limit,
    )
    return GA4ReportResponse(rows=rows, row_count=len(rows))


@router.get("/top-pages", response_model=GA4ReportResponse)
async def top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: GA4Client = Depends(get_ga4_client),
):
    rows = ga4_service.get_top_pages(client, date_range=date_range, limit=limit)
    return GA4ReportResponse(rows=rows, row_count=len(rows))


@router.get("/traffic-summary", response_model=GA4ReportResponse)
async def traffic_summary(
    date_range: str = "last_28_days",
    client: GA4Client = Depends(get_ga4_client),
):
    rows = ga4_service.get_traffic_summary(client, date_range=date_range)
    return GA4ReportResponse(rows=rows, row_count=len(rows))
