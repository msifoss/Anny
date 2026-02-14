def format_table(rows: list[dict], columns: list[str] | None = None) -> str:
    """Format a list of dicts as a readable text table for MCP output."""
    if not rows:
        return "No data available."

    if columns is None:
        columns = list(rows[0].keys())

    col_widths = {col: len(col) for col in columns}
    for row in rows:
        for col in columns:
            val = str(row.get(col, ""))
            col_widths[col] = max(col_widths[col], len(val))

    header = " | ".join(col.ljust(col_widths[col]) for col in columns)
    separator = "-+-".join("-" * col_widths[col] for col in columns)

    lines = [header, separator]
    for row in rows:
        line = " | ".join(str(row.get(col, "")).ljust(col_widths[col]) for col in columns)
        lines.append(line)

    return "\n".join(lines)
