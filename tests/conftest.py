import pytest
from fastapi.testclient import TestClient

from anny.core.dependencies import verify_api_key
from anny.main import _rate_limit_store, app


@pytest.fixture(autouse=True)
def _clear_rate_limit_store():
    """Clear the rate limit store before each test to prevent cross-test pollution."""
    _rate_limit_store.clear()


@pytest.fixture
def client():
    app.dependency_overrides[verify_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.pop(verify_api_key, None)
