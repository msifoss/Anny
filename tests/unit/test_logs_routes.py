"""Tests for the /api/logs endpoint."""

import logging
from unittest.mock import patch

from fastapi.testclient import TestClient

from anny.core.logging import _ring_handler
from anny.main import app


def test_logs_endpoint_returns_list(client):
    """GET /api/logs returns a JSON array."""
    _ring_handler.buffer.clear()
    logger = logging.getLogger("test.logs.route")
    logger.info("route test entry")

    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_logs_endpoint_with_limit(client):
    """Limit parameter caps returned entries."""
    _ring_handler.buffer.clear()
    logger = logging.getLogger("test.logs.limit")
    for i in range(10):
        logger.info("log %d", i)

    response = client.get("/api/logs?limit=3")
    assert response.status_code == 200
    assert len(response.json()) <= 3


def test_logs_endpoint_with_level_filter(client):
    """Level filter excludes lower-severity entries."""
    _ring_handler.buffer.clear()
    logger = logging.getLogger("test.logs.filter")
    logger.info("info msg")
    logger.error("error msg")

    response = client.get("/api/logs?level=ERROR")
    assert response.status_code == 200
    data = response.json()
    for entry in data:
        assert entry["level"] in ("ERROR", "CRITICAL")


def test_logs_endpoint_invalid_level(client):
    """Invalid level value returns 422."""
    response = client.get("/api/logs?level=BOGUS")
    assert response.status_code == 422


def test_logs_endpoint_requires_auth():
    """Without auth override, endpoint requires API key when configured."""
    with patch("anny.core.dependencies.settings") as mock_settings:
        mock_settings.anny_api_key = "test-secret-key"
        unauthenticated = TestClient(app)
        response = unauthenticated.get("/api/logs")
        assert response.status_code == 401
