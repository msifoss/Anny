"""Tests for request-ID and request-logging middleware."""

import logging


def test_request_id_header_present(client):
    """Every response gets an X-Request-ID header."""
    response = client.get("/api/logs")
    assert "X-Request-ID" in response.headers
    rid = response.headers["X-Request-ID"]
    assert len(rid) == 12
    assert rid.isalnum()


def test_request_id_unique_per_request(client):
    """Each request gets a different ID."""
    r1 = client.get("/api/logs")
    r2 = client.get("/api/logs")
    assert r1.headers["X-Request-ID"] != r2.headers["X-Request-ID"]


def test_health_skips_request_logging(client, caplog):
    """The /health endpoint should not produce request-logging output."""
    with caplog.at_level(logging.INFO, logger="anny"):
        client.get("/health")

    http_logs = [r for r in caplog.records if r.getMessage() == "HTTP request" and r.name == "anny"]
    # /health is skipped by the request logging middleware
    assert len(http_logs) == 0


def test_request_logging_fires_for_api(client, caplog):
    """API requests produce an HTTP-request log entry."""
    with caplog.at_level(logging.INFO):
        client.get("/api/logs")

    http_logs = [r for r in caplog.records if r.getMessage() == "HTTP request"]
    assert len(http_logs) >= 1
    record = http_logs[0]
    assert record.method == "GET"
    assert record.path == "/api/logs"
    assert hasattr(record, "duration_ms")
