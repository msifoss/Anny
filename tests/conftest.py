import pytest
from fastapi.testclient import TestClient

from anny.core.dependencies import get_query_cache, verify_api_key
from anny.core.logging import set_request_id
from anny.main import _rate_limit_store, app


@pytest.fixture(autouse=True)
def _clear_rate_limit_store():
    """Clear the rate limit store before each test to prevent cross-test pollution."""
    _rate_limit_store.clear()


@pytest.fixture(autouse=True)
def _clear_query_cache():
    """Clear cached QueryCache singleton between tests to prevent MagicMock leaks."""
    get_query_cache.cache_clear()
    yield
    get_query_cache.cache_clear()


@pytest.fixture(autouse=True)
def _clear_request_id():
    """Reset request-ID context between tests."""
    set_request_id("")
    yield
    set_request_id("")


@pytest.fixture
def client():
    app.dependency_overrides[verify_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.pop(verify_api_key, None)
