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
            return json.load(f)

    def _write(self, data: dict) -> None:
        """Write data to the JSON file, creating parent directories if needed."""
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # --- Insights ---

    def add_insight(self, text: str, source: str, tags: list[str]) -> dict:
        """Add an insight and return it."""
        data = self._read()
        insight = {
            "id": _generate_id("ins"),
            "text": text,
            "source": source,
            "tags": tags,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        data["insights"].append(insight)
        self._write(data)
        return insight

    def list_insights(self) -> list[dict]:
        """Return all insights."""
        return self._read()["insights"]

    def delete_insight(self, insight_id: str) -> bool:
        """Delete an insight by ID. Returns True if found and deleted."""
        data = self._read()
        original_len = len(data["insights"])
        data["insights"] = [i for i in data["insights"] if i["id"] != insight_id]
        if len(data["insights"]) < original_len:
            self._write(data)
            return True
        return False

    # --- Watchlist ---

    def add_watchlist_item(self, page_path: str, label: str, baseline: dict | None = None) -> dict:
        """Add a watchlist item and return it."""
        data = self._read()
        item = {
            "id": _generate_id("wtc"),
            "page_path": page_path,
            "label": label,
            "baseline": baseline or {},
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        data["watchlist"].append(item)
        self._write(data)
        return item

    def list_watchlist(self) -> list[dict]:
        """Return all watchlist items."""
        return self._read()["watchlist"]

    def delete_watchlist_item(self, item_id: str) -> bool:
        """Delete a watchlist item by ID. Returns True if found and deleted."""
        data = self._read()
        original_len = len(data["watchlist"])
        data["watchlist"] = [i for i in data["watchlist"] if i["id"] != item_id]
        if len(data["watchlist"]) < original_len:
            self._write(data)
            return True
        return False

    # --- Segments ---

    def add_segment(
        self, name: str, description: str, filter_type: str, patterns: list[str]
    ) -> dict:
        """Add a segment and return it."""
        data = self._read()
        segment = {
            "id": _generate_id("seg"),
            "name": name,
            "description": description,
            "filter_type": filter_type,
            "patterns": patterns,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        data["segments"].append(segment)
        self._write(data)
        return segment

    def list_segments(self) -> list[dict]:
        """Return all segments."""
        return self._read()["segments"]

    def delete_segment(self, segment_id: str) -> bool:
        """Delete a segment by ID. Returns True if found and deleted."""
        data = self._read()
        original_len = len(data["segments"])
        data["segments"] = [s for s in data["segments"] if s["id"] != segment_id]
        if len(data["segments"]) < original_len:
            self._write(data)
            return True
        return False

    # --- Bulk ---

    def get_all(self) -> dict:
        """Return the entire memory store contents."""
        return self._read()
