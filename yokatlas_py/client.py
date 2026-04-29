"""High-level YÖK Atlas API client (sync + async)."""

from __future__ import annotations

import asyncio
import atexit
from typing import Any

from ._lookup import LookupCache
from .config import Settings, settings as default_settings
from .http_client import AsyncHttpClient, HttpClient
from .models import City, Program, ProgramGroup, SearchFilters, SearchPage, University

_SEARCH_PATH = "/api/tercih-kilavuz/search"
_UNIVERSITIES_PATH = "/api/tercih-kilavuz/universiteler"
_PROGRAMS_PATH = "/api/tercih-kilavuz/universite-programlar"
_CITIES_PATH = "/api/tercih-kilavuz/universite-iller"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _coerce_filters(value: SearchFilters | dict[str, Any] | None) -> SearchFilters:
    if value is None:
        return SearchFilters()
    if isinstance(value, SearchFilters):
        return value
    return SearchFilters.model_validate(value)


def _build_request(
    filters: SearchFilters,
    *,
    page: int,
    size: int,
    sort_by: str,
    direction: str,
) -> dict[str, Any]:
    return {
        "filters": filters.to_payload(),
        "page": int(page),
        "size": int(size),
        "sortBy": sort_by,
        "direction": direction.upper(),
    }


def _resolve_smart_fields(filters: SearchFilters, cache: LookupCache) -> SearchFilters:
    """Replace string filters (universite/program/il) with their ID counterparts."""
    if not any((filters.universite, filters.program, filters.il)):
        return filters

    data = filters.model_dump()
    if filters.universite is not None:
        names = filters.universite if isinstance(filters.universite, list) else [filters.universite]
        data["universite_id"] = [cache.resolve_university(n).universite_id for n in names]
        data["universite"] = None
    if filters.program is not None:
        names = filters.program if isinstance(filters.program, list) else [filters.program]
        data["birim_grup_id"] = [cache.resolve_program(n).birim_grup_id for n in names]
        data["program"] = None
    if filters.il is not None:
        names = filters.il if isinstance(filters.il, list) else [filters.il]
        data["il_kodu"] = [cache.resolve_city(n).il_kodu for n in names]
        data["il"] = None
    return SearchFilters.model_validate(data)


# ---------------------------------------------------------------------------
# Sync client
# ---------------------------------------------------------------------------


class YokAtlasClient:
    """Synchronous client for the YÖK Atlas tercih-kılavuz JSON API."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        http: HttpClient | None = None,
    ) -> None:
        self.settings = settings or default_settings
        self._http = http or HttpClient(settings=self.settings)
        self._lookups = LookupCache(ttl=self.settings.lookup_cache_ttl)

    # ---- context management ------------------------------------------------

    def __enter__(self) -> "YokAtlasClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    # ---- public API --------------------------------------------------------

    def search(
        self,
        filters: SearchFilters | dict[str, Any] | None = None,
        *,
        page: int = 0,
        size: int = 20,
        sort_by: str = "basariSirasi",
        direction: str = "ASC",
        smart_search: bool = True,
    ) -> SearchPage[Program]:
        """Search the YÖK Atlas tercih kılavuzu."""
        f = _coerce_filters(filters)
        if smart_search and any((f.universite, f.program, f.il)):
            self._ensure_lookups()
            f = _resolve_smart_fields(f, self._lookups)
        body = _build_request(f, page=page, size=size, sort_by=sort_by, direction=direction)
        raw = self._http.post_json(_SEARCH_PATH, json_body=body)
        return SearchPage[Program].model_validate(raw)

    def get_program(self, kilavuz_kodu: int | str) -> Program | None:
        """Return a single program by its ÖSYM kılavuz kodu, or ``None`` if not found."""
        try:
            code = int(kilavuz_kodu)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"kilavuz_kodu must be an int (got {kilavuz_kodu!r})") from exc
        page = self.search(SearchFilters(kilavuz_kodu=code), size=1, smart_search=False)
        return page.content[0] if page.content else None

    def list_universities(self) -> list[University]:
        self._ensure_lookups()
        return self._lookups.universities

    def list_program_groups(self) -> list[ProgramGroup]:
        self._ensure_lookups()
        return self._lookups.program_groups

    def list_cities(self) -> list[City]:
        self._ensure_lookups()
        return self._lookups.cities

    def refresh_lookups(self) -> None:
        """Force a refresh of the universities/programs/cities cache."""
        self._lookups.invalidate()
        self._fetch_lookups()

    # ---- internals ---------------------------------------------------------

    def _ensure_lookups(self) -> None:
        if self._lookups.is_fresh():
            return
        self._fetch_lookups()

    def _fetch_lookups(self) -> None:
        unis = self._http.get_json(_UNIVERSITIES_PATH)
        progs = self._http.get_json(_PROGRAMS_PATH)
        cities = self._http.get_json(_CITIES_PATH)
        self._lookups.populate(universities=unis, program_groups=progs, cities=cities)


# ---------------------------------------------------------------------------
# Async client
# ---------------------------------------------------------------------------


class AsyncYokAtlasClient:
    """Asynchronous client for the YÖK Atlas tercih-kılavuz JSON API."""

    def __init__(
        self,
        *,
        settings: Settings | None = None,
        http: AsyncHttpClient | None = None,
    ) -> None:
        self.settings = settings or default_settings
        self._http = http or AsyncHttpClient(settings=self.settings)
        self._lookups = LookupCache(ttl=self.settings.lookup_cache_ttl)

    async def __aenter__(self) -> "AsyncYokAtlasClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        await self._http.aclose()

    async def search(
        self,
        filters: SearchFilters | dict[str, Any] | None = None,
        *,
        page: int = 0,
        size: int = 20,
        sort_by: str = "basariSirasi",
        direction: str = "ASC",
        smart_search: bool = True,
    ) -> SearchPage[Program]:
        f = _coerce_filters(filters)
        if smart_search and any((f.universite, f.program, f.il)):
            await self._ensure_lookups()
            f = _resolve_smart_fields(f, self._lookups)
        body = _build_request(f, page=page, size=size, sort_by=sort_by, direction=direction)
        raw = await self._http.post_json(_SEARCH_PATH, json_body=body)
        return SearchPage[Program].model_validate(raw)

    async def get_program(self, kilavuz_kodu: int | str) -> Program | None:
        try:
            code = int(kilavuz_kodu)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"kilavuz_kodu must be an int (got {kilavuz_kodu!r})") from exc
        page = await self.search(SearchFilters(kilavuz_kodu=code), size=1, smart_search=False)
        return page.content[0] if page.content else None

    async def list_universities(self) -> list[University]:
        await self._ensure_lookups()
        return self._lookups.universities

    async def list_program_groups(self) -> list[ProgramGroup]:
        await self._ensure_lookups()
        return self._lookups.program_groups

    async def list_cities(self) -> list[City]:
        await self._ensure_lookups()
        return self._lookups.cities

    async def refresh_lookups(self) -> None:
        self._lookups.invalidate()
        await self._fetch_lookups()

    async def _ensure_lookups(self) -> None:
        if self._lookups.is_fresh():
            return
        await self._fetch_lookups()

    async def _fetch_lookups(self) -> None:
        unis_task = self._http.get_json(_UNIVERSITIES_PATH)
        progs_task = self._http.get_json(_PROGRAMS_PATH)
        cities_task = self._http.get_json(_CITIES_PATH)
        unis, progs, cities = await asyncio.gather(unis_task, progs_task, cities_task)
        self._lookups.populate(universities=unis, program_groups=progs, cities=cities)


# ---------------------------------------------------------------------------
# Module-level convenience (lazy singleton)
# ---------------------------------------------------------------------------


_default_client: YokAtlasClient | None = None


def _get_default_client() -> YokAtlasClient:
    global _default_client
    if _default_client is None:
        _default_client = YokAtlasClient()
        atexit.register(_default_client.close)
    return _default_client


def search_programs(
    filters: SearchFilters | dict[str, Any] | None = None,
    *,
    page: int = 0,
    size: int = 20,
    sort_by: str = "basariSirasi",
    direction: str = "ASC",
    smart_search: bool = True,
) -> SearchPage[Program]:
    """Convenience wrapper around :meth:`YokAtlasClient.search` using a process-wide client."""
    return _get_default_client().search(
        filters,
        page=page,
        size=size,
        sort_by=sort_by,
        direction=direction,
        smart_search=smart_search,
    )


def get_program(kilavuz_kodu: int | str) -> Program | None:
    return _get_default_client().get_program(kilavuz_kodu)


def list_universities() -> list[University]:
    return _get_default_client().list_universities()


def list_program_groups() -> list[ProgramGroup]:
    return _get_default_client().list_program_groups()


def list_cities() -> list[City]:
    return _get_default_client().list_cities()


__all__ = [
    "AsyncYokAtlasClient",
    "YokAtlasClient",
    "get_program",
    "list_cities",
    "list_program_groups",
    "list_universities",
    "search_programs",
]
