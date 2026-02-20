import fcntl
import json
import os
import random
from datetime import datetime, timezone


def _generate_id(prefix: str) -> str:
    """Generate a human-readable, sortable ID: {prefix}_{YYYYMMDD}_{HHMMSS}_{4hex}."""
    now = datetime.now(timezone.utc)
    hex_part = f"{random.randint(0, 0xFFFF):04x}"
    return f"{prefix}_{now.strftime('%Y%m%d')}_{now.strftime('%H%M%S')}_{hex_part}"


_EMPTY_STORE = {"insights": [], "watchlist": [], "segments": []}


class MemoryStore:
    """JSON file-backed memory store for insights, watchlist, and segments."""

    def __init__(self, path: str):
        self._path = os.path.expanduser(path)

    @property
    def path(self) -> str:
        return self._path

    def _read(self) -> dict:
        """Read the JSON file and return its contents."""
        if not os.path.exists(self._path):
            return {"insights": [], "watchlist": [], "segments": []}
        with open(self._path, "r", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_SH)
            try:
                return json.load(f)
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)

    def _modify(self, mutate_fn):
        """Atomically read, modify, and write the store under an exclusive lock."""
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        if not os.path.exists(self._path):
            with open(self._path, "w", encoding="utf-8") as f:
                json.dump({"insights": [], "watchlist": [], "segments": []}, f, indent=2)
            os.chmod(self._path, 0o600)
        with open(self._path, "r+", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                data = json.load(f)
                result = mutate_fn(data)
                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        return result

    # --- Insights ---

    def add_insight(self, text: str, source: str, tags: list[str]) -> dict:
        """Add an insight and return it."""
        insight = {
            "id": _generate_id("ins"),
            "text": text,
            "source": source,
            "tags": tags,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        def _mutate(data):
            data["insights"].append(insight)

        self._modify(_mutate)
        return insight

    def list_insights(self) -> list[dict]:
        """Return all insights."""
        return self._read()["insights"]

    def delete_insight(self, insight_id: str) -> bool:
        """Delete an insight by ID. Returns True if found and deleted."""
        deleted = []

        def _mutate(data):
            original_len = len(data["insights"])
            data["insights"] = [i for i in data["insights"] if i["id"] != insight_id]
            deleted.append(len(data["insights"]) < original_len)

        self._modify(_mutate)
        return deleted[0]

    # --- Watchlist ---

    def add_watchlist_item(self, page_path: str, label: str, baseline: dict | None = None) -> dict:
        """Add a watchlist item and return it."""
        item = {
            "id": _generate_id("wtc"),
            "page_path": page_path,
            "label": label,
            "baseline": baseline or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        def _mutate(data):
            data["watchlist"].append(item)

        self._modify(_mutate)
        return item

    def list_watchlist(self) -> list[dict]:
        """Return all watchlist items."""
        return self._read()["watchlist"]

    def delete_watchlist_item(self, item_id: str) -> bool:
        """Delete a watchlist item by ID. Returns True if found and deleted."""
        deleted = []

        def _mutate(data):
            original_len = len(data["watchlist"])
            data["watchlist"] = [i for i in data["watchlist"] if i["id"] != item_id]
            deleted.append(len(data["watchlist"]) < original_len)

        self._modify(_mutate)
        return deleted[0]

    # --- Segments ---

    def add_segment(
        self, name: str, description: str, filter_type: str, patterns: list[str]
    ) -> dict:
        """Add a segment and return it."""
        segment = {
            "id": _generate_id("seg"),
            "name": name,
            "description": description,
            "filter_type": filter_type,
            "patterns": patterns,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }

        def _mutate(data):
            data["segments"].append(segment)

        self._modify(_mutate)
        return segment

    def list_segments(self) -> list[dict]:
        """Return all segments."""
        return self._read()["segments"]

    def delete_segment(self, segment_id: str) -> bool:
        """Delete a segment by ID. Returns True if found and deleted."""
        deleted = []

        def _mutate(data):
            original_len = len(data["segments"])
            data["segments"] = [s for s in data["segments"] if s["id"] != segment_id]
            deleted.append(len(data["segments"]) < original_len)

        self._modify(_mutate)
        return deleted[0]

    # --- Bulk ---

    def get_all(self) -> dict:
        """Return the entire memory store contents."""
        return self._read()
