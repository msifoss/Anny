import pytest
from fastapi.testclient import TestClient

from anny.core.dependencies import verify_api_key
from anny.main import app


@pytest.fixture
def client():
    app.dependency_overrides[verify_api_key] = lambda: None
    yield TestClient(app)
    app.dependency_overrides.pop(verify_api_key, None)
