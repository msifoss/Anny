from anny.core.cache import QueryCache


def get_cache_status(cache: QueryCache) -> dict:
    """Return cache status information."""
    return cache.status()


def clear_cache(cache: QueryCache) -> dict:
    """Clear all cache entries. Returns count of removed entries."""
    count = cache.clear()
    return {"cleared": count}
