"""Shared test fixtures."""

from __future__ import annotations

from typing import Any

import httpx
import pytest

from yokatlas_py.client import AsyncYokAtlasClient, YokAtlasClient
from yokatlas_py.config import Settings
from yokatlas_py.http_client import AsyncHttpClient, HttpClient

# ---------------------------------------------------------------------------
# Fixture data — small but realistic samples mirroring the real API response.
# ---------------------------------------------------------------------------

SAMPLE_PROGRAM_RAW: dict[str, Any] = {
    "osymKilavuzId": 88079,
    "sinav": "YKS     ",
    "yil": 2025,
    "donem": "1       ",
    "tabloTuru": "TABLO 4",
    "birimId": 377415,
    "birimHiyerarsi": "173496|292945|292947",
    "kilavuzKodu": 105490029,
    "universiteId": 173496,
    "universiteAdi": "İSTANBUL MEDENİYET ÜNİVERSİTESİ",
    "uniIlKodu": 34,
    "uniIlAdi": "İSTANBUL",
    "uniIlceKodu": 1708,
    "uniIlceAdi": "ÜSKÜDAR",
    "fymkId": 292945,
    "fymkAdi": "Sanat, Tasarım ve Mimarlık Fakültesi",
    "birimAdi": "Görsel İletişim Tasarımı",
    "birimGrupId": 3118,
    "birimGrupAdi": "Görsel İletişim Tasarımı",
    "birimTuruId": 46,
    "birimTuruAdi": "LISANS",
    "ogrenimTuruId": 86,
    "ogrenimTuruAdi": "Örgün Öğretim",
    "ogrenimSuresi": 4,
    "puanTuru": "SÖZ",
    "ogrenimDiliId": 181,
    "ogrenimDiliAdi": "Türkçe",
    "bursOraniId": 0,
    "kontenjan": 55,
    "kontenjanObs": 2,
    "kontenjanY34": 2,
    "gkY": 55,
    "obkY": 2,
    "y34": 2,
    "prof": 2,
    "doc": 4,
    "dou": 0,
    "ogrGor": 2,
    "arGor": 2,
    "ilKodu": 34,
    "ilAdi": "İSTANBUL",
    "ilceKodu": 1708,
    "ilceAdi": "ÜSKÜDAR",
    "universiteTuru": "DEVLET",
    "kpss1": "66.593874",
    "kpss2": "70.851220",
    "minPuan": 370.09443,
    "basariSirasi": 28226,
    "gk1": 55,
    "minPuan1": "397.21128",
    "basariSirasi1": 35310,
    "gk2": 50,
    "minPuan2": "380.82506",
    "basariSirasi2": 43196,
    "gk3": 50,
    "minPuan3": "377.39965",
    "basariSirasi3": 50044,
}


def make_search_response(items: list[dict[str, Any]] | None = None, *, total: int | None = None, size: int = 20, page: int = 0) -> dict[str, Any]:
    items = items if items is not None else [SAMPLE_PROGRAM_RAW]
    total = total if total is not None else len(items)
    total_pages = max(1, (total + size - 1) // size) if size else 1
    return {
        "content": items,
        "empty": len(items) == 0,
        "first": page == 0,
        "last": page >= total_pages - 1,
        "number": page,
        "numberOfElements": len(items),
        "size": size,
        "totalElements": total,
        "totalPages": total_pages,
        "yil": 2025,
    }


SAMPLE_UNIVERSITIES = [
    {"universiteId": 173496, "universiteAdi": "İSTANBUL MEDENİYET ÜNİVERSİTESİ"},
    {"universiteId": 173500, "universiteAdi": "BOĞAZİÇİ ÜNİVERSİTESİ"},
    {"universiteId": 173510, "universiteAdi": "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"},
]
SAMPLE_PROGRAMS = [
    {"birimGrupId": 3118, "birimGrupAdi": "Görsel İletişim Tasarımı", "puanTuru": "SÖZ"},
    {"birimGrupId": 4001, "birimGrupAdi": "Bilgisayar Mühendisliği", "puanTuru": "SAY"},
    {"birimGrupId": 4002, "birimGrupAdi": "Tıp", "puanTuru": "SAY"},
]
SAMPLE_CITIES = [
    {"ilKodu": 34, "ilAdi": "İSTANBUL"},
    {"ilKodu": 6, "ilAdi": "ANKARA"},
    {"ilKodu": 35, "ilAdi": "İZMİR"},
]


# ---------------------------------------------------------------------------
# Mock transport
# ---------------------------------------------------------------------------


def _mock_handler(request: httpx.Request) -> httpx.Response:
    path = request.url.path
    if path == "/api/tercih-kilavuz/universiteler":
        return httpx.Response(200, json=SAMPLE_UNIVERSITIES)
    if path == "/api/tercih-kilavuz/universite-programlar":
        return httpx.Response(200, json=SAMPLE_PROGRAMS)
    if path == "/api/tercih-kilavuz/universite-iller":
        return httpx.Response(200, json=SAMPLE_CITIES)
    if path == "/api/tercih-kilavuz/search":
        import json as _json
        body = request.content
        try:
            payload = _json.loads(body) if body else {}
        except Exception:
            payload = {}
        filters = payload.get("filters") or {}
        kilavuz = filters.get("kilavuzKodu")
        if kilavuz:
            if int(kilavuz) == SAMPLE_PROGRAM_RAW["kilavuzKodu"]:
                return httpx.Response(200, json=make_search_response([SAMPLE_PROGRAM_RAW], total=1, size=payload.get("size", 20)))
            return httpx.Response(200, json=make_search_response([], total=0, size=payload.get("size", 20)))
        return httpx.Response(200, json=make_search_response(size=payload.get("size", 20), page=payload.get("page", 0)))
    return httpx.Response(404, json={"error": "not found", "path": path})


@pytest.fixture()
def settings() -> Settings:
    return Settings(base_url="https://yokatlas.example.test", timeout=5.0, verify_ssl=False, lookup_cache_ttl=60)


@pytest.fixture()
def http_client(settings: Settings) -> HttpClient:
    transport = httpx.MockTransport(_mock_handler)
    inner = httpx.Client(base_url=str(settings.base_url).rstrip("/"), transport=transport, headers=settings.headers())
    return HttpClient(settings=settings, client=inner)


@pytest.fixture()
def async_http_client(settings: Settings) -> AsyncHttpClient:
    transport = httpx.MockTransport(_mock_handler)
    inner = httpx.AsyncClient(base_url=str(settings.base_url).rstrip("/"), transport=transport, headers=settings.headers())
    return AsyncHttpClient(settings=settings, client=inner)


@pytest.fixture()
def client(settings: Settings, http_client: HttpClient) -> YokAtlasClient:
    return YokAtlasClient(settings=settings, http=http_client)


@pytest.fixture()
def async_client(settings: Settings, async_http_client: AsyncHttpClient) -> AsyncYokAtlasClient:
    return AsyncYokAtlasClient(settings=settings, http=async_http_client)
