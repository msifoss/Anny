import csv
import io
import json

_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _sanitize_cell(value: str) -> str:
    """Prefix formula-triggering characters with a tab to prevent CSV injection."""
    if isinstance(value, str) and value and value[0] in _FORMULA_PREFIXES:
        return f"\t{value}"
    return value


def to_csv(rows: list[dict]) -> bytes:
    """Convert rows to CSV bytes with UTF-8 BOM for Excel compatibility."""
    if not rows:
        return b"\xef\xbb\xbf"

    safe_rows = [{k: _sanitize_cell(str(v)) for k, v in row.items()} for row in rows]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(safe_rows[0].keys()))
    writer.writeheader()
    writer.writerows(safe_rows)
    return b"\xef\xbb\xbf" + output.getvalue().encode("utf-8")


def to_json(rows: list[dict]) -> bytes:
    """Convert rows to pretty-printed JSON bytes."""
    return json.dumps(rows, indent=2, ensure_ascii=False).encode("utf-8")
