from fastapi import APIRouter, Depends, HTTPException, Security

from anny.api.models import (
    SCQueryRequest,
    SCQueryResponse,
    SitemapDetailResponse,
    SitemapListResponse,
)
from anny.clients.search_console import SearchConsoleClient
from anny.core.cache import QueryCache
from anny.core.dependencies import get_query_cache, get_search_console_client, verify_api_key
from anny.core.services import search_console_service

router = APIRouter(prefix="/api/search-console", tags=["Search Console"])


@router.post("/query", response_model=SCQueryResponse)
async def query(
    body: SCQueryRequest,
    client: SearchConsoleClient = Depends(get_search_console_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_search_analytics(
        client,
        dimensions=body.dimensions,
        date_range=body.date_range,
        row_limit=body.row_limit,
        cache=cache,
    )
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/top-queries", response_model=SCQueryResponse)
async def top_queries(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: SearchConsoleClient = Depends(get_search_console_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_queries(
        client, date_range=date_range, limit=limit, cache=cache
    )
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/top-pages", response_model=SCQueryResponse)
async def top_pages(
    date_range: str = "last_28_days",
    limit: int = 10,
    client: SearchConsoleClient = Depends(get_search_console_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_top_pages(
        client, date_range=date_range, limit=limit, cache=cache
    )
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/summary", response_model=SCQueryResponse)
async def summary(
    date_range: str = "last_28_days",
    client: SearchConsoleClient = Depends(get_search_console_client),
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    rows = search_console_service.get_performance_summary(
        client, date_range=date_range, cache=cache
    )
    return SCQueryResponse(rows=rows, row_count=len(rows))


@router.get("/sitemaps", response_model=SitemapListResponse)
async def sitemaps(
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    items = search_console_service.get_sitemaps(client)
    return SitemapListResponse(sitemaps=items, count=len(items))


@router.get("/sitemaps/{feedpath:path}", response_model=SitemapDetailResponse)
async def sitemap_details(
    feedpath: str,
    client: SearchConsoleClient = Depends(get_search_console_client),
    _: str = Security(verify_api_key),
):
    if not feedpath.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="feedpath must be a valid URL (http/https)")
    return search_console_service.get_sitemap_details(client, feedpath)
