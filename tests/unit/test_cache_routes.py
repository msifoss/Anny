from fastapi.testclient import TestClient

from anny.core.cache import QueryCache
from anny.core.dependencies import get_query_cache, verify_api_key
from anny.main import app


def _setup(cache):
    app.dependency_overrides[get_query_cache] = lambda: cache
    app.dependency_overrides[verify_api_key] = lambda: None


def _teardown():
    app.dependency_overrides.pop(get_query_cache, None)
    app.dependency_overrides.pop(verify_api_key, None)


def test_cache_status_endpoint():
    cache = QueryCache(ttl=60, max_entries=100)
    cache.put("k1", "v1")
    _setup(cache)

    tc = TestClient(app)
    response = tc.get("/api/cache/status")

    _teardown()

    assert response.status_code == 200
    data = response.json()
    assert data["total_entries"] == 1
    assert data["max_entries"] == 100


def test_clear_cache_endpoint():
    cache = QueryCache()
    cache.put("k1", "v1")
    cache.put("k2", "v2")
    _setup(cache)

    tc = TestClient(app)
    response = tc.delete("/api/cache")

    _teardown()

    assert response.status_code == 200
    assert response.json()["cleared"] == 2
