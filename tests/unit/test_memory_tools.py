from anny.clients.memory import MemoryStore
from anny.core.formatting import format_table
from anny.core.services import memory_service


def _make_store(tmp_path):
    return MemoryStore(str(tmp_path / "memory.json"))


def test_save_insight_tool_flow(tmp_path):
    """Test the same logic that the save_insight MCP tool executes."""
    store = _make_store(tmp_path)
    insight = memory_service.save_insight(store, "Traffic dropped", "ga4", "traffic, seo")
    result = f"Saved insight {insight['id']}: {insight['text']}"
    assert "Traffic dropped" in result
    assert "ins_" in result


def test_list_insights_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_insight(store, "Insight 1", "ga4", "tag1")
    items = memory_service.list_insights(store)
    rows = [
        {"id": i["id"], "source": i["source"], "tags": ", ".join(i["tags"]), "text": i["text"]}
        for i in items
    ]
    result = format_table(rows)
    assert "Insight 1" in result
    assert "ga4" in result


def test_list_insights_empty(tmp_path):
    store = _make_store(tmp_path)
    items = memory_service.list_insights(store)
    assert items == []


def test_delete_insight_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    insight = memory_service.save_insight(store, "Delete me", "ga4")
    deleted = memory_service.delete_insight(store, insight["id"])
    assert deleted is True


def test_add_to_watchlist_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    item = memory_service.add_to_watchlist(store, "/pricing", "Pricing", 1200, 3000)
    result = f"Added {item['id']}: watching {item['page_path']} ({item['label']})"
    assert "/pricing" in result
    assert "Pricing" in result


def test_list_watchlist_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    memory_service.add_to_watchlist(store, "/page", "Page")
    items = memory_service.list_watchlist(store)
    rows = [
        {
            "id": i["id"],
            "page_path": i["page_path"],
            "label": i["label"],
            "baseline": str(i["baseline"]) if i["baseline"] else "",
        }
        for i in items
    ]
    result = format_table(rows)
    assert "/page" in result
    assert "Page" in result


def test_save_segment_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    segment = memory_service.save_segment(
        store, "no-login", "Exclude login", "exclude_pages", "/login, /logout"
    )
    result = f"Saved segment {segment['id']}: {segment['name']} ({segment['filter_type']})"
    assert "no-login" in result
    assert "exclude_pages" in result


def test_list_segments_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_segment(store, "seg1", "Desc", "exclude_pages", "/a, /b")
    items = memory_service.list_segments(store)
    rows = [
        {
            "id": s["id"],
            "name": s["name"],
            "filter_type": s["filter_type"],
            "patterns": ", ".join(s["patterns"]),
        }
        for s in items
    ]
    result = format_table(rows)
    assert "seg1" in result
    assert "exclude_pages" in result


def test_get_context_empty_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    ctx = memory_service.get_context(store)
    summary = ctx["summary"]
    result = (
        f"Memory: {summary['total_insights']} insights, "
        f"{summary['total_watchlist']} watchlist items, "
        f"{summary['total_segments']} segments"
    )
    assert "0 insights" in result
    assert "0 watchlist items" in result
    assert "0 segments" in result


def test_get_context_with_data_tool_flow(tmp_path):
    store = _make_store(tmp_path)
    memory_service.save_insight(store, "Test insight", "ga4")
    memory_service.add_to_watchlist(store, "/home", "Home page")
    memory_service.save_segment(store, "seg", "Desc", "exclude_pages", "/x")

    ctx = memory_service.get_context(store)
    assert ctx["summary"]["total_insights"] == 1
    assert ctx["summary"]["total_watchlist"] == 1
    assert ctx["summary"]["total_segments"] == 1

    # Verify the context can be formatted as expected by the MCP tool
    parts = []
    if ctx["insights"]:
        rows = [{"source": i["source"], "text": i["text"]} for i in ctx["insights"]]
        parts.append(format_table(rows))
    result = "\n".join(parts)
    assert "Test insight" in result
