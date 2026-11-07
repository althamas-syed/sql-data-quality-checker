# SQL Data Quality Checker

Open-source, read-only SQL data-quality checker for analysts and developers.

## Features
- Row and column counts
- Null counts by column
- Exact duplicate-row detection
- JSON report export
- SQLite read-only mode
- No third-party runtime dependencies

## Quick start
```bash
python -m pip install -e .
python examples/create_demo.py
sql-quality examples/demo.db sales --output report.json
python -m unittest discover -s tests -v
```

Negative values are not automatically treated as errors because refunds, returns and credits may be valid.

## Roadmap
SQL Server/MySQL support, configurable rules, referential-integrity checks, HTML reports and CI.

## License
MIT
