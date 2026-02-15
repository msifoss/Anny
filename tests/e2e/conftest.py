import os

import pytest
from fastapi.testclient import TestClient

from anny.main import app


def pytest_collection_modifyitems(config, items):  # pylint: disable=unused-argument
    """Skip e2e tests unless ANNY_E2E=1 is set."""
    if os.environ.get("ANNY_E2E") == "1":
        return
    skip_e2e = pytest.mark.skip(reason="Set ANNY_E2E=1 to run e2e tests")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


@pytest.fixture(scope="session")
def live_client():
    """TestClient that uses real dependencies (no mocks)."""
    return TestClient(app)
