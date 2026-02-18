from fastapi import APIRouter, Depends, Security

from anny.api.models import SCQueryRequest, SCQueryResponse
from anny.clients.search_console import SearchConsoleClient
from anny.core.dependencies import get_search_console_client, verify_api_key
from anny.core.services import search_console_service

router = APIRouter(prefix="/api/search-console", tags=["Search Console"])


@router.post("/query", response_model=SCQueryResponse)
async def query(
    body: SCQueryRequest,
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_search_analytics(
        client,
        dimensions=body.dimensions,
        date_range=body.date_range,
        row_limit=body.row_limit,
    )
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/top-queries", response_model=SCQueryResponse)
async def top_queries(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_queries(client, date_range=date_range, limit=limit)
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/top-pages", response_model=SCQueryResponse)
async def top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_pages(client, date_range=date_range, limit=limit)
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/summary", response_model=SCQueryResponse)
async def summary(
    date_range: str = "last_28_days",
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_performance_summary(client, date_range=date_range)
    return SCQueryResponse(rows=rows, row_count=len(rows))
