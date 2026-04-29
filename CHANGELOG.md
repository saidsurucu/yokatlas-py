# Changelog

## 0.6.0

**BREAKING — Major rewrite.**

YÖK Atlas migrated to a React SPA in late 2025; the legacy HTML-scraping endpoints (`/lisans/{yil}/{kod}.php`, `/onlisans/{yil}/{kod}.php`, `/lisans-tercih-sihirbazi.php`, `/server_side/server_processing-atlas2016-TS-{t3,t4}.php`) now serve a 926-byte SPA shell. v0.x is broken end-to-end. v0.6.0 targets the new official JSON API (`/api/tercih-kilavuz/*`).

### Added

- `YokAtlasClient` (sync) and `AsyncYokAtlasClient` (async) — single, unified client with the same surface for both flavors.
- Module-level convenience: `search_programs`, `get_program`, `list_universities`, `list_program_groups`, `list_cities` (lazy singleton).
- Smart search: `universite`, `program`, `il` accept free-form strings and resolve to IDs via fuzzy matching with Turkish-aware normalization.
- Pydantic v2 models: `Program`, `YearlyStats` (current + 3-year history), `SearchFilters`, `SearchPage[T]`, `University`, `ProgramGroup`, `City`.
- `Settings` (pydantic-settings) with `YOKATLAS_*` env var overrides.
- Exception hierarchy: `YokAtlasError`, `APIError`, `NotFoundError`, `RateLimitError`, `LookupError`.
- Comprehensive test suite with `httpx.MockTransport`.

### Removed

- `YOKATLASLisansAtlasi`, `YOKATLASOnlisansAtlasi`, `YOKATLASLisansTercihSihirbazi`, `YOKATLASOnlisansTercihSihirbazi`.
- All 60+ HTML fetcher modules (`yokatlas_py/lisans_fetchers/`, `yokatlas_py/onlisans_fetchers/`, `yokatlas_py/fetchers/`).
- `form_data.py`, `onlisans_form_data.py` — IDs are now fetched from the API at runtime.
- `base_fetcher.py`, `search_wrappers.py`, `search_utils.py`, `utils.py`, `columnData.json`.
- `year` parameter — every search result already carries 4 years (current + 3 historical).
- `urllib3`, `beautifulsoup4`, `typing-extensions` dependencies.

### Changed

- `requires-python` raised to `>=3.10`.
- TLS verification default flipped to `True` (set `YOKATLAS_VERIFY_SSL=false` to opt out).
- `puan_turu` is now uppercase (`SAY` / `SÖZ` / `EA` / `DİL` / `TYT`).

See `MIGRATION.md` for a full v0.x → v0.6.0 transition guide.

## 0.5.x and earlier

See git history. All 0.x releases are now broken upstream and unsupported.
