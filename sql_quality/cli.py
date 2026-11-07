import argparse
import json
import sqlite3
from pathlib import Path

def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'

def inspect_table(connection, table):
    exists = connection.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)).fetchone()
    if not exists:
        raise ValueError(f"Table not found: {table}")
    columns = [r[1] for r in connection.execute(f"PRAGMA table_info({quote_identifier(table)})")]
    if not columns:
        raise ValueError("Table has no columns")
    quoted = quote_identifier(table)
    count = connection.execute(f"SELECT COUNT(*) FROM {quoted}").fetchone()[0]
    nulls = {}
    for col in columns:
        qcol = quote_identifier(col)
        nulls[col] = connection.execute(f"SELECT COUNT(*) FROM {quoted} WHERE {qcol} IS NULL").fetchone()[0]
    group = ", ".join(quote_identifier(c) for c in columns)
    duplicates = connection.execute(
        f"SELECT COALESCE(SUM(n-1),0) FROM (SELECT COUNT(*) AS n FROM {quoted} GROUP BY {group} HAVING COUNT(*) > 1)"
    ).fetchone()[0]
    return {"table": table, "rows": count, "columns": columns, "null_counts": nulls, "duplicate_rows": duplicates}

def main(argv=None):
    parser = argparse.ArgumentParser(description="Read-only SQLite data quality scan")
    parser.add_argument("database")
    parser.add_argument("table")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    db = Path(args.database)
    if not db.is_file():
        parser.error("Database file does not exist")
    try:
        uri = db.resolve().as_uri() + "?mode=ro"
        with sqlite3.connect(uri, uri=True) as connection:
            report = inspect_table(connection, args.table)
    except (sqlite3.Error, ValueError) as exc:
        parser.error(str(exc))
    result = json.dumps(report, indent=2)
    print(result)
    if args.output:
        Path(args.output).write_text(result + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
