from fastapi import APIRouter, Depends, Security

from anny.core.cache import QueryCache
from anny.core.dependencies import get_query_cache, verify_api_key
from anny.core.services import cache_service

router = APIRouter(prefix="/api/cache", tags=["Cache"])


@router.get("/status")
async def cache_status(
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    return cache_service.get_cache_status(cache)


@router.delete("")
async def clear_cache(
    cache: QueryCache = Depends(get_query_cache),
    _: str = Security(verify_api_key),
):
    return cache_service.clear_cache(cache)
