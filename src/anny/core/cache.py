import hashlib
import json
import logging
import threading
import time

logger = logging.getLogger("anny")


class QueryCache:
    """In-memory query cache with TTL expiry and LRU eviction."""

    def __init__(self, ttl: int = 3600, max_entries: int = 500):
        self._ttl = ttl
        self._max_entries = max_entries
        self._lock = threading.Lock()
        # key -> {"result": ..., "api": ..., "summary": ..., "ts": ..., "last_access": ...}
        self._store: dict[str, dict] = {}

    @staticmethod
    def make_key(api: str, params: dict) -> str:
        """Create a deterministic SHA-256 cache key from API name and params."""
        raw = json.dumps({"api": api, "params": params}, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def get(self, key: str) -> dict | None:
        """Return cached result or None if missing/expired."""
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None
            if time.time() - entry["ts"] > self._ttl:
                del self._store[key]
                return None
            entry["last_access"] = time.time()
            return entry["result"]

    def put(self, key: str, result, api: str = "", summary: str = "") -> None:
        """Store a result in cache, evicting oldest-accessed entry if at capacity."""
        with self._lock:
            if len(self._store) >= self._max_entries and key not in self._store:
                oldest_key = min(self._store, key=lambda k: self._store[k]["last_access"])
                del self._store[oldest_key]
            now = time.time()
            self._store[key] = {
                "result": result,
                "api": api,
                "summary": summary,
                "ts": now,
                "last_access": now,
            }

    def clear(self) -> int:
        """Clear all entries. Returns the number of entries removed."""
        with self._lock:
            count = len(self._store)
            self._store.clear()
            logger.info("Cache cleared: %d entries removed", count)
            return count

    def status(self) -> dict:
        """Return cache status info."""
        with self._lock:
            now = time.time()
            active = sum(1 for e in self._store.values() if now - e["ts"] <= self._ttl)
            return {
                "total_entries": len(self._store),
                "active_entries": active,
                "max_entries": self._max_entries,
                "ttl_seconds": self._ttl,
            }
