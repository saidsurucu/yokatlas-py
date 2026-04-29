"""Tests for the pydantic models."""

from __future__ import annotations

import pytest

from yokatlas_py.models import Program, SearchFilters, SearchPage, YearlyStats

from .conftest import SAMPLE_PROGRAM_RAW, make_search_response


def test_program_groups_yearly_into_current_and_history() -> None:
    program = Program.model_validate(SAMPLE_PROGRAM_RAW)
    assert program.kilavuz_kodu == 105490029
    assert program.universite_adi == "İSTANBUL MEDENİYET ÜNİVERSİTESİ"
    assert program.birim_turu_adi == "LISANS"
    assert program.universite_turu == "DEVLET"

    # current year stats
    assert program.current.year == 2025
    assert program.current.kontenjan == 55
    assert program.current.yerlesen == 55
    assert program.current.min_puan == pytest.approx(370.09443)
    assert program.current.basari_sirasi == 28226
    assert program.current.kpss1 == pytest.approx(66.593874)
    assert program.current.prof == 2

    # history → 3 entries, newest first (yıl-1, yıl-2, yıl-3)
    assert len(program.history) == 3
    assert [h.year for h in program.history] == [2024, 2023, 2022]
    assert program.history[0].min_puan == pytest.approx(397.21128)
    assert program.history[0].basari_sirasi == 35310
    assert program.history[2].min_puan == pytest.approx(377.39965)


def test_program_all_years_helper_orders_descending() -> None:
    program = Program.model_validate(SAMPLE_PROGRAM_RAW)
    years = [s.year for s in program.all_years]
    assert years == [2025, 2024, 2023, 2022]


def test_yearly_stats_handles_missing_fields() -> None:
    raw = {
        "yil": 2025,
        "kilavuzKodu": 1,
        "universiteId": 1,
        "universiteAdi": "X",
        "birimAdi": "Y",
        "birimTuruAdi": "LISANS",
        "puanTuru": "SAY",
        "universiteTuru": "DEVLET",
        # No yearly fields whatsoever
    }
    program = Program.model_validate(raw)
    assert program.current.year == 2025
    assert program.current.kontenjan is None
    assert program.current.min_puan is None
    assert all(h.kontenjan is None for h in program.history)


def test_search_page_validates_spring_payload() -> None:
    page = SearchPage[Program].model_validate(make_search_response([SAMPLE_PROGRAM_RAW], total=1, size=10))
    assert page.total_elements == 1
    assert page.total_pages == 1
    assert page.size == 10
    assert page.first is True and page.last is True
    assert len(page.content) == 1
    assert page.content[0].kilavuz_kodu == 105490029


def test_search_filters_payload_camel_case_and_defaults() -> None:
    payload = SearchFilters().to_payload()
    assert payload == {
        "puanTuru": None,
        "universiteId": [],
        "birimGrupId": [],
        "ilKodu": [],
        "birimTuruId": None,
        "universiteTuru": None,
        "bursOraniId": None,
        "ogrenimTuruId": None,
        "kilavuzKodu": None,
        "minBasariSirasi": None,
        "maxBasariSirasi": None,
    }


def test_search_filters_normalizes_puan_turu_aliases() -> None:
    assert SearchFilters(puan_turu="SAY").to_payload()["puanTuru"] == "SAY"
    f = SearchFilters.model_validate({"puan_turu": "SÖZ"})
    assert f.to_payload()["puanTuru"] == "SÖZ"


def test_search_filters_rejects_smart_id_collision() -> None:
    with pytest.raises(ValueError, match="universite/universite_id"):
        SearchFilters(universite="boğaziçi", universite_id=[1])
    with pytest.raises(ValueError, match="program/birim_grup_id"):
        SearchFilters(program="bilgisayar", birim_grup_id=[1])
    with pytest.raises(ValueError, match="il/il_kodu"):
        SearchFilters(il="ankara", il_kodu=[6])


def test_search_filters_rejects_unknown_fields() -> None:
    with pytest.raises(ValueError):
        SearchFilters.model_validate({"unknown_field": 1})
