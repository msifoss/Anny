from anny.clients.memory import MemoryStore
from anny.core.services import memory_service


def _make_store(tmp_path):
    return MemoryStore(str(tmp_path / "memory.json"))


# --- Insights ---


def test_save_insight_with_tags(tmp_path):
    store = _make_store(tmp_path)
    result = memory_service.save_insight(store, "Traffic spiked", "ga4", "traffic, seo")
    assert result["tags"] == ["traffic", "seo"]
    assert result["text"] == "Traffic spiked"


def test_save_insight_empty_tags(tmp_path):
    store = _make_store(tmp_path)
    result = memory_service.save_insight(store, "Note", "ga4", "")
    assert result["tags"] == []


def test_save_insight_no_tags_arg(tmp_path):
    store = _make_store(tmp_path)
    result = memory_service.save_insight(store, "Note", "ga4")
    assert result["tags"] == []


def test_list_insights_returns_all(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_insight(store, "Insight 1", "ga4", "tag1")
    memory_service.save_insight(store, "Insight 2", "sc", "tag2")
    items = memory_service.list_insights(store)
    assert len(items) == 2


def test_delete_insight_success(tmp_path):
    store = _make_store(tmp_path)
    insight = memory_service.save_insight(store, "To delete", "ga4")
    assert memory_service.delete_insight(store, insight["id"]) is True
    assert memory_service.list_insights(store) == []


def test_delete_insight_not_found(tmp_path):
    store = _make_store(tmp_path)
    assert memory_service.delete_insight(store, "ins_nonexistent") is False


# --- Watchlist ---


def test_add_to_watchlist_with_baseline(tmp_path):
    store = _make_store(tmp_path)
    item = memory_service.add_to_watchlist(
        store, "/pricing", "Pricing page", baseline_sessions=1200, baseline_pageviews=3000
    )
    assert item["page_path"] == "/pricing"
    assert item["baseline"] == {"sessions": 1200, "pageviews": 3000}


def test_add_to_watchlist_no_baseline(tmp_path):
    store = _make_store(tmp_path)
    item = memory_service.add_to_watchlist(store, "/about", "About page")
    assert item["baseline"] == {}


def test_list_watchlist(tmp_path):
    store = _make_store(tmp_path)
    memory_service.add_to_watchlist(store, "/page1", "Page 1")
    memory_service.add_to_watchlist(store, "/page2", "Page 2")
    items = memory_service.list_watchlist(store)
    assert len(items) == 2


def test_remove_from_watchlist_success(tmp_path):
    store = _make_store(tmp_path)
    item = memory_service.add_to_watchlist(store, "/page", "Page")
    assert memory_service.remove_from_watchlist(store, item["id"]) is True
    assert memory_service.list_watchlist(store) == []


def test_remove_from_watchlist_not_found(tmp_path):
    store = _make_store(tmp_path)
    assert memory_service.remove_from_watchlist(store, "wtc_nonexistent") is False


# --- Segments ---


def test_save_segment_splits_patterns(tmp_path):
    store = _make_store(tmp_path)
    segment = memory_service.save_segment(
        store, "no-login", "Exclude login", "exclude_pages", "/login, /logout"
    )
    assert segment["patterns"] == ["/login", "/logout"]
    assert segment["filter_type"] == "exclude_pages"


def test_list_segments(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_segment(store, "seg1", "Desc 1", "exclude_pages", "/a")
    memory_service.save_segment(store, "seg2", "Desc 2", "include_pages", "/b")
    items = memory_service.list_segments(store)
    assert len(items) == 2


# --- Context ---


def test_get_context_empty(tmp_path):
    store = _make_store(tmp_path)
    ctx = memory_service.get_context(store)
    assert ctx["insights"] == []
    assert ctx["watchlist"] == []
    assert ctx["segments"] == []
    assert ctx["summary"] == {"total_insights": 0, "total_watchlist": 0, "total_segments": 0}


def test_get_context_with_data(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_insight(store, "Insight", "ga4")
    memory_service.add_to_watchlist(store, "/page", "Page")
    memory_service.save_segment(store, "seg", "Desc", "exclude_pages", "/x")

    ctx = memory_service.get_context(store)
    assert ctx["summary"]["total_insights"] == 1
    assert ctx["summary"]["total_watchlist"] == 1
    assert ctx["summary"]["total_segments"] == 1
    assert len(ctx["insights"]) == 1
    assert len(ctx["watchlist"]) == 1
    assert len(ctx["segments"]) == 1
