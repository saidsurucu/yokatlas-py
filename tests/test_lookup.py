"""Tests for the lookup cache and fuzzy resolver."""

from __future__ import annotations

import pytest

from yokatlas_py._lookup import LookupCache, normalize
from yokatlas_py.exceptions import LookupError


def test_normalize_handles_turkish_characters() -> None:
    assert normalize("İSTANBUL") == "istanbul"
    assert normalize("Boğaziçi") == "bogazici"
    assert normalize("  ŞIŞLI  Ünal ") == "sisli unal"


@pytest.fixture()
def populated_cache() -> LookupCache:
    cache = LookupCache(ttl=60)
    cache.populate(
        universities=[
            {"universiteId": 1, "universiteAdi": "BOĞAZİÇİ ÜNİVERSİTESİ"},
            {"universiteId": 2, "universiteAdi": "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"},
        ],
        program_groups=[
            {"birimGrupId": 100, "birimGrupAdi": "Bilgisayar Mühendisliği", "puanTuru": "SAY"},
            {"birimGrupId": 200, "birimGrupAdi": "Tıp", "puanTuru": "SAY"},
        ],
        cities=[
            {"ilKodu": 34, "ilAdi": "İSTANBUL"},
            {"ilKodu": 6, "ilAdi": "ANKARA"},
        ],
    )
    return cache


def test_resolve_exact_match(populated_cache: LookupCache) -> None:
    uni = populated_cache.resolve_university("BOĞAZİÇİ ÜNİVERSİTESİ")
    assert uni.universite_id == 1


def test_resolve_normalized_match(populated_cache: LookupCache) -> None:
    assert populated_cache.resolve_university("bogazici universitesi").universite_id == 1


def test_resolve_substring_match(populated_cache: LookupCache) -> None:
    # "boğaziçi" alone resolves to "BOĞAZİÇİ ÜNİVERSİTESİ" via substring fallback
    assert populated_cache.resolve_university("boğaziçi").universite_id == 1


def test_resolve_fuzzy_match(populated_cache: LookupCache) -> None:
    # Slight typo
    assert populated_cache.resolve_university("bogazıcı universite").universite_id == 1


def test_resolve_unknown_raises_with_suggestions(populated_cache: LookupCache) -> None:
    with pytest.raises(LookupError) as exc:
        populated_cache.resolve_university("zzzzzzzzz")
    assert exc.value.kind == "university"


def test_resolve_program_partial(populated_cache: LookupCache) -> None:
    assert populated_cache.resolve_program("bilgisayar").birim_grup_id == 100


def test_resolve_city(populated_cache: LookupCache) -> None:
    assert populated_cache.resolve_city("ankara").il_kodu == 6


def test_cache_is_fresh_after_populate(populated_cache: LookupCache) -> None:
    assert populated_cache.is_fresh() is True


def test_cache_invalidate_clears_entries(populated_cache: LookupCache) -> None:
    populated_cache.invalidate()
    assert populated_cache.is_fresh() is False
    assert populated_cache.universities == []


def test_zero_ttl_means_fresh_forever() -> None:
    cache = LookupCache(ttl=0)
    cache.populate(
        universities=[{"universiteId": 1, "universiteAdi": "X"}],
        program_groups=[],
        cities=[],
    )
    assert cache.is_fresh() is True
