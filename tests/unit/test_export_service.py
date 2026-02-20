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
