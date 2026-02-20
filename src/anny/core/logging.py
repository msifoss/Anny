"""Structured JSON logging with request-ID tracking and in-memory ring buffer."""

import collections
import contextvars
import logging
import uuid

from pythonjsonlogger.json import JsonFormatter

# ---- Request-ID context ----
_request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


def get_request_id() -> str:
    return _request_id_var.get()


def set_request_id(rid: str) -> contextvars.Token:
    return _request_id_var.set(rid)


def new_request_id() -> str:
    return uuid.uuid4().hex[:12]


# ---- Request-ID filter (injects request_id into every log record) ----
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_request_id()
        return True


# ---- Ring-buffer handler (stores recent log dicts in memory) ----
class RingBufferHandler(logging.Handler):
    """Stores the most recent *maxlen* log records as dicts for the /api/logs endpoint."""

    def __init__(self, maxlen: int = 1000):
        super().__init__()
        self.buffer: collections.deque[dict] = collections.deque(maxlen=maxlen)

    def emit(self, record):
        self.buffer.append(
            {
                "timestamp": (
                    self.formatter.formatTime(record) if self.formatter else record.created
                ),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "request_id": getattr(record, "request_id", ""),
            }
        )


# Module-level singleton so the logs endpoint can read it.
_ring_handler = RingBufferHandler(maxlen=1000)

_LEVEL_VALUES = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def get_recent_logs(limit: int = 100, level: str = "DEBUG") -> list[dict]:
    """Return the most recent log entries, optionally filtered by minimum level."""
    min_level = _LEVEL_VALUES.get(level.upper(), logging.DEBUG)
    entries = [e for e in _ring_handler.buffer if _LEVEL_VALUES.get(e["level"], 0) >= min_level]
    return list(entries)[-limit:]


# ---- Setup (called once from main.py) ----
def setup_logging() -> None:
    """Replace the default logging config with structured JSON output."""
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    # Remove any existing handlers from prior basicConfig calls
    for h in root.handlers[:]:
        root.removeHandler(h)

    # JSON formatter
    fmt = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
    )

    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    root.addHandler(console)

    # Ring-buffer handler (no formatter needed, we build dicts manually)
    root.addHandler(_ring_handler)

    # Inject request_id into every record
    root.addFilter(RequestIdFilter())
