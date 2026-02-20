"""Tests for structured logging infrastructure."""

import logging

from anny.core.logging import (
    RequestIdFilter,
    RingBufferHandler,
    get_recent_logs,
    get_request_id,
    new_request_id,
    set_request_id,
    _ring_handler,
)


class TestRequestId:
    def test_default_is_empty(self):
        set_request_id("")
        assert get_request_id() == ""

    def test_set_and_get(self):
        set_request_id("abc123")
        assert get_request_id() == "abc123"
        set_request_id("")

    def test_new_request_id_format(self):
        rid = new_request_id()
        assert len(rid) == 12
        assert rid.isalnum()

    def test_new_request_id_unique(self):
        ids = {new_request_id() for _ in range(100)}
        assert len(ids) == 100


class TestRequestIdFilter:
    def test_adds_request_id_to_record(self):
        set_request_id("test-rid")
        filt = RequestIdFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        result = filt.filter(record)
        assert result is True
        assert record.request_id == "test-rid"  # pylint: disable=no-member
        set_request_id("")

    def test_empty_when_no_request_id(self):
        set_request_id("")
        filt = RequestIdFilter()
        record = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        filt.filter(record)
        assert record.request_id == ""  # pylint: disable=no-member


class TestRingBufferHandler:
    def test_stores_log_entries(self):
        handler = RingBufferHandler(maxlen=10)
        filt = RequestIdFilter()
        handler.addFilter(filt)
        logger = logging.getLogger("test.ring")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        set_request_id("ring-test")
        logger.info("hello world")

        assert len(handler.buffer) >= 1
        entry = handler.buffer[-1]
        assert entry["level"] == "INFO"
        assert entry["message"] == "hello world"
        assert entry["request_id"] == "ring-test"

        logger.removeHandler(handler)
        set_request_id("")

    def test_respects_maxlen(self):
        handler = RingBufferHandler(maxlen=3)
        logger = logging.getLogger("test.ring.maxlen")
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

        for i in range(5):
            logger.info("msg %d", i)

        assert len(handler.buffer) == 3
        assert handler.buffer[0]["message"] == "msg 2"

        logger.removeHandler(handler)


class TestGetRecentLogs:
    def setup_method(self):
        """Clear ring buffer before each test."""
        _ring_handler.buffer.clear()

    def test_returns_empty_when_no_logs(self):
        assert get_recent_logs() == []

    def test_returns_recent_entries(self):
        logger = logging.getLogger("test.recent")
        logger.info("entry one")
        logger.warning("entry two")
        logs = get_recent_logs(limit=10)
        messages = [e["message"] for e in logs]
        assert "entry one" in messages
        assert "entry two" in messages

    def test_limit_parameter(self):
        logger = logging.getLogger("test.limit")
        for i in range(10):
            logger.info("log %d", i)
        logs = get_recent_logs(limit=3)
        assert len(logs) <= 3

    def test_level_filter_warning(self):
        logger = logging.getLogger("test.level")
        logger.info("info msg")
        logger.warning("warn msg")
        logger.error("error msg")
        logs = get_recent_logs(limit=100, level="WARNING")
        levels = {e["level"] for e in logs}
        assert "INFO" not in levels
        assert "WARNING" in levels or "ERROR" in levels

    def test_level_filter_error(self):
        logger = logging.getLogger("test.level.error")
        logger.info("info")
        logger.warning("warn")
        logger.error("err")
        logs = get_recent_logs(limit=100, level="ERROR")
        levels = {e["level"] for e in logs}
        assert "INFO" not in levels
        assert "WARNING" not in levels
