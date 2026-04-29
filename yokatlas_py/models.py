"""Pydantic models for the YÖK Atlas JSON API (v1)."""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ._serialization import to_camel

PuanTuru = Literal["SAY", "SÖZ", "EA", "DİL", "TYT"]


def _model_config(*, populate_by_name: bool = True, alias: bool = True) -> ConfigDict:
    cfg: ConfigDict = ConfigDict(populate_by_name=populate_by_name, str_strip_whitespace=True)
    if alias:
        cfg["alias_generator"] = to_camel
    return cfg


# ---------------------------------------------------------------------------
# Lookup tables
# ---------------------------------------------------------------------------


class University(BaseModel):
    model_config = _model_config()
    universite_id: int
    universite_adi: str


class ProgramGroup(BaseModel):
    model_config = _model_config()
    birim_grup_id: int
    birim_grup_adi: str
    puan_turu: str


class City(BaseModel):
    model_config = _model_config()
    il_kodu: int
    il_adi: str


# ---------------------------------------------------------------------------
# Yearly snapshot (kontenjan/kadro/puan/sıra/kpss for a single year)
# ---------------------------------------------------------------------------


class YearlyStats(BaseModel):
    """Per-year statistics for a single program."""

    model_config = ConfigDict(populate_by_name=True)

    year: int
    kontenjan: int | None = None
    yerlesen: int | None = Field(default=None, description="Genel kontenjandan yerleşen (gkY).")
    kontenjan_obs: int | None = None
    kontenjan_y34: int | None = None
    prof: int | None = None
    doc: int | None = None
    dou: int | None = None
    ogr_gor: int | None = None
    ar_gor: int | None = None
    kpss1: float | None = None
    kpss2: float | None = None
    min_puan: float | None = None
    basari_sirasi: int | None = None


# ---------------------------------------------------------------------------
# Program (one row from /api/tercih-kilavuz/search)
# ---------------------------------------------------------------------------


_FLAT_TO_YEARLY = {
    "kontenjan": "kontenjan",
    "gkY": "yerlesen",
    "kontenjanObs": "kontenjan_obs",
    "kontenjanY34": "kontenjan_y34",
    "prof": "prof",
    "doc": "doc",
    "dou": "dou",
    "ogrGor": "ogr_gor",
    "arGor": "ar_gor",
    "kpss1": "kpss1",
    "kpss2": "kpss2",
    "minPuan": "min_puan",
    "basariSirasi": "basari_sirasi",
}


def _coerce_int(value: Any) -> int | None:
    if value is None or value == "":
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return None


def _coerce_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


_YEARLY_FIELD_TYPES = {
    "kontenjan": _coerce_int,
    "yerlesen": _coerce_int,
    "kontenjan_obs": _coerce_int,
    "kontenjan_y34": _coerce_int,
    "prof": _coerce_int,
    "doc": _coerce_int,
    "dou": _coerce_int,
    "ogr_gor": _coerce_int,
    "ar_gor": _coerce_int,
    "kpss1": _coerce_float,
    "kpss2": _coerce_float,
    "min_puan": _coerce_float,
    "basari_sirasi": _coerce_int,
}


def _build_yearly_stats(data: dict[str, Any], suffix: str, year: int) -> YearlyStats:
    raw: dict[str, Any] = {"year": year}
    for camel, snake in _FLAT_TO_YEARLY.items():
        key_camel = f"{camel}{suffix}"
        key_snake = f"{snake}{('_' + suffix) if suffix else ''}"
        if key_camel in data:
            raw[snake] = _YEARLY_FIELD_TYPES[snake](data[key_camel])
        elif key_snake in data:
            raw[snake] = _YEARLY_FIELD_TYPES[snake](data[key_snake])
    return YearlyStats.model_validate(raw)


class Program(BaseModel):
    """A single program entry returned by the search endpoint.

    Yearly statistics (kontenjan, kadro, min puan, başarı sırası, KPSS) are
    grouped into :attr:`current` and :attr:`history` (3 previous years,
    newest → oldest).
    """

    model_config = _model_config()

    # Core identifiers
    osym_kilavuz_id: int | None = None
    sinav: str | None = None
    yil: int
    donem: str | None = None
    tablo_turu: str | None = None
    birim_id: int | None = None
    birim_hiyerarsi: str | None = None
    kilavuz_kodu: int

    # University
    universite_id: int
    universite_adi: str
    uni_il_kodu: int | None = None
    uni_il_adi: str | None = None
    uni_ilce_kodu: int | None = None
    uni_ilce_adi: str | None = None

    # Faculty / school
    fymk_id: int | None = None
    fymk_adi: str | None = None
    fymk_il_kodu: int | None = None
    fymk_il_adi: str | None = None
    fymk_ilce_kodu: int | None = None
    fymk_ilce_adi: str | None = None

    # Program
    birim_adi: str
    birim_grup_id: int | None = None
    birim_grup_adi: str | None = None
    birim_turu_id: int | None = None
    birim_turu_adi: Literal["LISANS", "ONLISANS"]

    ogrenim_turu_id: int | None = None
    ogrenim_turu_adi: str | None = None
    ogrenim_suresi: int | None = None
    puan_turu: str
    ogrenim_dili_id: int | None = None
    ogrenim_dili_adi: str | None = None
    burs_orani_id: int | None = None
    burs_orani_adi: str | None = None

    # Location
    il_kodu: int | None = None
    il_adi: str | None = None
    ilce_kodu: int | None = None
    ilce_adi: str | None = None
    universite_turu: Literal["DEVLET", "VAKIF"]

    # Yearly snapshots
    current: YearlyStats
    history: list[YearlyStats] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def _group_yearly(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data
        if "current" in data and "history" in data:
            return data  # already structured

        current_year = data.get("yil") or data.get("year") or 0
        try:
            current_year = int(current_year)
        except (TypeError, ValueError):
            current_year = 0

        data = dict(data)
        data["current"] = _build_yearly_stats(data, "", current_year)
        history: list[YearlyStats] = []
        for offset in (1, 2, 3):
            stats = _build_yearly_stats(data, str(offset), current_year - offset)
            history.append(stats)
        data["history"] = history
        return data

    @property
    def all_years(self) -> list[YearlyStats]:
        """Current year first, followed by historical years (newest → oldest)."""
        return [self.current, *self.history]


# ---------------------------------------------------------------------------
# Spring-style Page<T> wrapper
# ---------------------------------------------------------------------------

T = TypeVar("T")


class SearchPage(BaseModel, Generic[T]):
    model_config = _model_config()

    content: list[T]
    total_elements: int
    total_pages: int
    size: int
    number: int
    first: bool
    last: bool
    number_of_elements: int
    empty: bool
    yil: int | None = None


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------


class SearchFilters(BaseModel):
    """Filters accepted by :class:`yokatlas_py.client.YokAtlasClient.search`.

    *Smart* string fields (``universite``, ``program``, ``il``) are resolved at
    request time when ``smart_search=True``. They cannot be combined with their
    ID counterparts (``universite_id``, ``birim_grup_id``, ``il_kodu``).
    """

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    # ID-based filters (always honored)
    puan_turu: PuanTuru | None = None
    universite_id: list[int] | None = None
    birim_grup_id: list[int] | None = None
    il_kodu: list[int] | None = None
    birim_turu_id: int | None = None
    universite_turu: Literal["DEVLET", "VAKIF"] | None = None
    burs_orani_id: int | None = None
    ogrenim_turu_id: int | None = None
    kilavuz_kodu: int | None = None
    min_basari_sirasi: int | None = None
    max_basari_sirasi: int | None = None

    # Smart (string) filters — resolved when smart_search=True
    universite: str | list[str] | None = None
    program: str | list[str] | None = None
    il: str | list[str] | None = None

    @model_validator(mode="after")
    def _no_smart_id_collision(self) -> "SearchFilters":
        clashes: list[str] = []
        if self.universite is not None and self.universite_id is not None:
            clashes.append("universite/universite_id")
        if self.program is not None and self.birim_grup_id is not None:
            clashes.append("program/birim_grup_id")
        if self.il is not None and self.il_kodu is not None:
            clashes.append("il/il_kodu")
        if clashes:
            raise ValueError(
                "Smart filter and ID filter cannot be set together: " + ", ".join(clashes)
            )
        return self

    def to_payload(self) -> dict[str, Any]:
        """Render the filter object as the API expects (camelCase, ID-only)."""
        return {
            "puanTuru": self._normalize_puan_turu(self.puan_turu),
            "universiteId": list(self.universite_id) if self.universite_id else [],
            "birimGrupId": list(self.birim_grup_id) if self.birim_grup_id else [],
            "ilKodu": list(self.il_kodu) if self.il_kodu else [],
            "birimTuruId": self.birim_turu_id,
            "universiteTuru": self.universite_turu,
            "bursOraniId": self.burs_orani_id,
            "ogrenimTuruId": self.ogrenim_turu_id,
            "kilavuzKodu": self.kilavuz_kodu,
            "minBasariSirasi": self.min_basari_sirasi,
            "maxBasariSirasi": self.max_basari_sirasi,
        }

    @staticmethod
    def _normalize_puan_turu(value: str | None) -> str | None:
        if value is None:
            return None
        upper = value.upper()
        return {"SOZ": "SÖZ", "DIL": "DİL"}.get(upper, upper)


__all__ = [
    "City",
    "Program",
    "ProgramGroup",
    "PuanTuru",
    "SearchFilters",
    "SearchPage",
    "University",
    "YearlyStats",
]
