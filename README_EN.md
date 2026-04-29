# yokatlas-py

A modern, type-safe Python client for the YÖK Atlas tercih kılavuzu JSON API.

[![PyPI version](https://badge.fury.io/py/yokatlas-py.svg)](https://badge.fury.io/py/yokatlas-py)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[Türkçe README](README.md) · [API Reference](API.md) · [Migration Guide](MIGRATION.md)

> ⚠️ **v0.6.0 is a major rewrite.** YÖK Atlas migrated to a React SPA in 2025 and the legacy HTML-scraping endpoints were retired. v0.6.0 targets the new JSON API. v0.x users should consult [MIGRATION.md](MIGRATION.md).

## Features

- **One client**: `YokAtlasClient` (sync) and `AsyncYokAtlasClient` (async) with the same surface.
- **4 years in one shot**: Each program ships with current-year + 3 prior years of min score, success rank, quota/placement, and academic staff counts.
- **Smart search**: Free-form `universite="boğaziçi"`, `program="bilgisayar"`, `il="ankara"` resolve to IDs via fuzzy matching with Turkish-aware normalization.
- **Pydantic v2 models**: Full type safety, IDE auto-complete, runtime validation.
- **No HTML parsing**: Pure JSON; no `beautifulsoup4` dependency.

## Install

```bash
pip install yokatlas-py
# or
uv add yokatlas-py
```

Requires Python ≥3.10.

## Quickstart

```python
from yokatlas_py import YokAtlasClient, SearchFilters

with YokAtlasClient() as client:
    page = client.search(
        SearchFilters(puan_turu="SAY", universite="boğaziçi"),
        size=20,
    )
    print(f"Total: {page.total_elements}")
    for prog in page.content:
        print(prog.universite_adi, prog.birim_adi, prog.current.min_puan)

    prog = client.get_program(102210277)
    if prog:
        for stats in prog.all_years:
            print(stats.year, stats.min_puan, stats.basari_sirasi)
```

### Async

```python
import asyncio
from yokatlas_py import AsyncYokAtlasClient, SearchFilters

async def main() -> None:
    async with AsyncYokAtlasClient() as client:
        page = await client.search(SearchFilters(il="ankara", program="tıp"))
        for prog in page.content:
            print(prog.universite_adi, prog.current.min_puan)

asyncio.run(main())
```

### Module-level shortcuts

```python
from yokatlas_py import search_programs, get_program, list_universities

page = search_programs({"puan_turu": "EA", "universite": "boğaziçi"}, size=10)
prog = get_program(102210277)
unis = list_universities()
```

## Filters

See [API.md](API.md) for the full reference. Smart fields (`universite`, `program`, `il`) and ID fields (`universite_id`, `birim_grup_id`, `il_kodu`) are mutually exclusive.

## Configuration

Override via `YOKATLAS_*` env vars or by passing a `Settings` object to the client:

```python
from yokatlas_py import Settings, YokAtlasClient

client = YokAtlasClient(settings=Settings(timeout=60.0, lookup_cache_ttl=600))
```

## Limitation

The new API drops the per-program detail breakdowns that v0.x exposed (gender distribution, high school field/group, placed-by-city, preferred universities/programs, academic staff title distribution, transfers, graduation year, etc. — ~25 sub-categories). v0.6.0 only returns what the official API provides.

## Development

```bash
uv sync
uv run pytest
uv run pytest -m integration
uv run mypy yokatlas_py/
```

## License

MIT
