import json

from anny.core.services import export_service


def test_to_csv_basic():
    rows = [{"name": "Alice", "score": 10}, {"name": "Bob", "score": 20}]
    result = export_service.to_csv(rows)
    assert result.startswith(b"\xef\xbb\xbf")
    text = result.decode("utf-8-sig")
    lines = text.strip().splitlines()
    assert lines[0] == "name,score"
    assert lines[1] == "Alice,10"
    assert lines[2] == "Bob,20"


def test_to_csv_empty():
    result = export_service.to_csv([])
    assert result == b"\xef\xbb\xbf"


def test_to_csv_special_chars():
    rows = [{"name": 'He said "hi"', "note": "a,b,c"}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    assert '"He said ""hi"""' in text
    assert '"a,b,c"' in text


def test_to_json_basic():
    rows = [{"name": "Alice", "score": 10}]
    result = export_service.to_json(rows)
    parsed = json.loads(result)
    assert parsed == rows


def test_to_json_empty():
    result = export_service.to_json([])
    parsed = json.loads(result)
    assert parsed == []


def test_to_csv_formula_injection_equals():
    rows = [{"name": "=CMD()", "score": 10}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    lines = text.strip().splitlines()
    # Value should be tab-prefixed, not raw =CMD()
    assert lines[1].startswith("\t=CMD()")
    assert not lines[1].startswith("=CMD()")


def test_to_csv_formula_injection_plus():
    rows = [{"name": "+1+2", "score": 5}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    assert "\t+1+2" in text


def test_to_csv_formula_injection_minus():
    rows = [{"name": "-1-2", "score": 5}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    assert "\t-1-2" in text


def test_to_csv_formula_injection_at():
    rows = [{"name": "@SUM(A1)", "score": 5}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    assert "\t@SUM(A1)" in text


def test_to_csv_safe_values_unchanged():
    rows = [{"name": "hello", "score": 42}]
    result = export_service.to_csv(rows)
    text = result.decode("utf-8-sig")
    lines = text.strip().splitlines()
    assert lines[1] == "hello,42"
