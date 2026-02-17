from anny.clients.memory import MemoryStore


def save_insight(store: MemoryStore, text: str, source: str, tags: str = "") -> dict:
    """Save an insight. Tags is a comma-separated string."""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else []
    return store.add_insight(text, source, tag_list)


def list_insights(store: MemoryStore) -> list[dict]:
    """Return all saved insights."""
    return store.list_insights()


def delete_insight(store: MemoryStore, insight_id: str) -> bool:
    """Delete an insight by ID."""
    return store.delete_insight(insight_id)


def add_to_watchlist(
    store: MemoryStore,
    page_path: str,
    label: str,
    baseline_sessions: int | None = None,
    baseline_pageviews: int | None = None,
) -> dict:
    """Add a page to the watchlist with optional baseline metrics."""
    baseline = {}
    if baseline_sessions is not None:
        baseline["sessions"] = baseline_sessions
    if baseline_pageviews is not None:
        baseline["pageviews"] = baseline_pageviews
    return store.add_watchlist_item(page_path, label, baseline if baseline else None)


def list_watchlist(store: MemoryStore) -> list[dict]:
    """Return all watchlist items."""
    return store.list_watchlist()


def remove_from_watchlist(store: MemoryStore, item_id: str) -> bool:
    """Remove a page from the watchlist."""
    return store.delete_watchlist_item(item_id)


def save_segment(
    store: MemoryStore,
    name: str,
    description: str,
    filter_type: str,
    patterns: str,
) -> dict:
    """Save a reusable filter segment. Patterns is a comma-separated string."""
    pattern_list = [p.strip() for p in patterns.split(",") if p.strip()]
    return store.add_segment(name, description, filter_type, pattern_list)


def list_segments(store: MemoryStore) -> list[dict]:
    """Return all saved segments."""
    return store.list_segments()


def get_context(store: MemoryStore) -> dict:
    """Load all memory for session context."""
    data = store.get_all()
    return {
        "insights": data["insights"],
        "watchlist": data["watchlist"],
        "segments": data["segments"],
        "summary": {
            "total_insights": len(data["insights"]),
            "total_watchlist": len(data["watchlist"]),
            "total_segments": len(data["segments"]),
        },
    }
