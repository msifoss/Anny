import threading
import time

from anny.core.cache import QueryCache


def test_make_key_deterministic():
    k1 = QueryCache.make_key("ga4", {"metrics": "sessions", "date": "last_7_days"})
    k2 = QueryCache.make_key("ga4", {"metrics": "sessions", "date": "last_7_days"})
    assert k1 == k2


def test_make_key_different_params():
    k1 = QueryCache.make_key("ga4", {"metrics": "sessions"})
    k2 = QueryCache.make_key("ga4", {"metrics": "totalUsers"})
    assert k1 != k2


def test_put_and_get():
    cache = QueryCache(ttl=60)
    key = "test-key"
    cache.put(key, [{"a": 1}], api="ga4", summary="test")
    assert cache.get(key) == [{"a": 1}]


def test_get_missing_key():
    cache = QueryCache()
    assert cache.get("nonexistent") is None


def test_ttl_expiry():
    cache = QueryCache(ttl=0)
    key = "expires"
    cache.put(key, "data")
    time.sleep(0.01)
    assert cache.get(key) is None


def test_eviction_when_full():
    cache = QueryCache(ttl=60, max_entries=2)
    cache.put("k1", "v1")
    cache.put("k2", "v2")
    cache.put("k3", "v3")
    assert cache.get("k3") == "v3"
    assert cache.get("k2") == "v2"
    # k1 should have been evicted (oldest accessed)
    assert cache.get("k1") is None


def test_clear():
    cache = QueryCache()
    cache.put("k1", "v1")
    cache.put("k2", "v2")
    count = cache.clear()
    assert count == 2
    assert cache.get("k1") is None


def test_status():
    cache = QueryCache(ttl=3600, max_entries=500)
    cache.put("k1", "v1")
    s = cache.status()
    assert s["total_entries"] == 1
    assert s["active_entries"] == 1
    assert s["max_entries"] == 500
    assert s["ttl_seconds"] == 3600


def test_thread_safety():
    cache = QueryCache(ttl=60, max_entries=1000)
    errors = []

    def writer(start):
        try:
            for i in range(50):
                cache.put(f"k-{start}-{i}", f"v-{start}-{i}")
        except Exception as e:  # pylint: disable=broad-except
            errors.append(e)

    threads = [threading.Thread(target=writer, args=(t,)) for t in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not errors
    assert cache.status()["total_entries"] == 200
