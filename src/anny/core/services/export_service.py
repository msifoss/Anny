import csv
import io
import json


def to_csv(rows: list[dict]) -> bytes:
    """Convert rows to CSV bytes with UTF-8 BOM for Excel compatibility."""
    if not rows:
        return b"\xef\xbb\xbf"

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return b"\xef\xbb\xbf" + output.getvalue().encode("utf-8")


def to_json(rows: list[dict]) -> bytes:
    """Convert rows to pretty-printed JSON bytes."""
    return json.dumps(rows, indent=2, ensure_ascii=False).encode("utf-8")
