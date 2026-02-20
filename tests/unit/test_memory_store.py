import json
import os
import stat

from anny.clients.memory import MemoryStore, _generate_id


def test_generate_id_format():
    """ID should be prefix_YYYYMMDD_HHMMSS_4hex."""
    id_val = _generate_id("ins")
    parts = id_val.split("_")
    assert len(parts) == 4
    assert parts[0] == "ins"
    assert len(parts[1]) == 8  # YYYYMMDD
    assert len(parts[2]) == 6  # HHMMSS
    assert len(parts[3]) == 4  # 4 hex chars


def test_generate_id_unique():
    """Two generated IDs should differ (at least the hex part)."""
    id1 = _generate_id("seg")
    id2 = _generate_id("seg")
    assert id1 != id2


def test_empty_store_returns_defaults(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    assert store.list_insights() == []
    assert store.list_watchlist() == []
    assert store.list_segments() == []


def test_add_and_list_insight(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    insight = store.add_insight("Traffic spiked", "ga4", ["traffic"])

    assert insight["text"] == "Traffic spiked"
    assert insight["source"] == "ga4"
    assert insight["tags"] == ["traffic"]
    assert insight["id"].startswith("ins_")

    items = store.list_insights()
    assert len(items) == 1
    assert items[0]["id"] == insight["id"]


def test_delete_insight(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    insight = store.add_insight("To delete", "ga4", [])

    assert store.delete_insight(insight["id"]) is True
    assert store.list_insights() == []


def test_delete_insight_not_found(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    assert store.delete_insight("ins_nonexistent") is False


def test_add_and_list_watchlist_item(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    item = store.add_watchlist_item("/pricing", "Pricing page", {"sessions": 1200})

    assert item["page_path"] == "/pricing"
    assert item["label"] == "Pricing page"
    assert item["baseline"] == {"sessions": 1200}
    assert item["id"].startswith("wtc_")

    items = store.list_watchlist()
    assert len(items) == 1


def test_watchlist_default_baseline(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    item = store.add_watchlist_item("/about", "About page")
    assert item["baseline"] == {}


def test_delete_watchlist_item(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    item = store.add_watchlist_item("/page", "Test")
    assert store.delete_watchlist_item(item["id"]) is True
    assert store.list_watchlist() == []


def test_add_and_list_segment(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    segment = store.add_segment("no-login", "Exclude login pages", "exclude_pages", ["/login"])

    assert segment["name"] == "no-login"
    assert segment["filter_type"] == "exclude_pages"
    assert segment["patterns"] == ["/login"]
    assert segment["id"].startswith("seg_")

    items = store.list_segments()
    assert len(items) == 1


def test_delete_segment(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    segment = store.add_segment("temp", "Temp", "exclude_pages", ["/tmp"])
    assert store.delete_segment(segment["id"]) is True
    assert store.list_segments() == []


def test_get_all(tmp_path):
    store = MemoryStore(str(tmp_path / "memory.json"))
    store.add_insight("Insight 1", "ga4", [])
    store.add_watchlist_item("/page", "Page")
    store.add_segment("seg1", "Desc", "exclude_pages", ["/x"])

    data = store.get_all()
    assert len(data["insights"]) == 1
    assert len(data["watchlist"]) == 1
    assert len(data["segments"]) == 1


def test_file_persists_across_instances(tmp_path):
    path = str(tmp_path / "memory.json")
    store1 = MemoryStore(path)
    store1.add_insight("Persisted", "ga4", ["test"])

    store2 = MemoryStore(path)
    items = store2.list_insights()
    assert len(items) == 1
    assert items[0]["text"] == "Persisted"


def test_creates_parent_directories(tmp_path):
    path = str(tmp_path / "nested" / "dir" / "memory.json")
    store = MemoryStore(path)
    store.add_insight("Deep", "ga4", [])

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert len(data["insights"]) == 1


def test_file_created_with_restricted_permissions(tmp_path):
    """Memory file should be created with 0600 (owner-only read/write)."""
    path = str(tmp_path / "secure_memory.json")
    store = MemoryStore(path)
    store.add_insight("Secret insight", "ga4", [])

    file_mode = stat.S_IMODE(os.stat(path).st_mode)
    assert file_mode == 0o600
