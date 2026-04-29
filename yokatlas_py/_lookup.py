"""Lookup tables (universities, program groups, cities) and fuzzy resolver."""

from __future__ import annotations

import time
from difflib import get_close_matches
from typing import Iterable

from .exceptions import LookupError as _LookupError
from .models import City, ProgramGroup, University

_TR_TRANSLATION = str.maketrans(
    {
        "İ": "I", "ı": "i",
        "Ğ": "G", "ğ": "g",
        "Ş": "S", "ş": "s",
        "Ç": "C", "ç": "c",
        "Ö": "O", "ö": "o",
        "Ü": "U", "ü": "u",
    }
)


def normalize(text: str) -> str:
    """Turkish-aware normalization for fuzzy matching keys."""
    return " ".join(text.translate(_TR_TRANSLATION).lower().split())


class LookupCache:
    """In-process TTL cache holding the three lookup tables."""

    def __init__(self, *, ttl: int) -> None:
        self.ttl = ttl
        self._fetched_at: float = 0.0
        self._universities: list[University] = []
        self._program_groups: list[ProgramGroup] = []
        self._cities: list[City] = []
        self._uni_index: dict[str, University] = {}
        self._prog_index: dict[str, ProgramGroup] = {}
        self._city_index: dict[str, City] = {}

    def is_fresh(self) -> bool:
        if not self._universities:
            return False
        if self.ttl <= 0:
            return True
        return (time.monotonic() - self._fetched_at) < self.ttl

    def populate(
        self,
        *,
        universities: Iterable[University | dict],
        program_groups: Iterable[ProgramGroup | dict],
        cities: Iterable[City | dict],
    ) -> None:
        self._universities = [u if isinstance(u, University) else University.model_validate(u) for u in universities]
        self._program_groups = [p if isinstance(p, ProgramGroup) else ProgramGroup.model_validate(p) for p in program_groups]
        self._cities = [c if isinstance(c, City) else City.model_validate(c) for c in cities]

        self._uni_index = {normalize(u.universite_adi): u for u in self._universities}
        self._prog_index = {normalize(p.birim_grup_adi): p for p in self._program_groups}
        self._city_index = {normalize(c.il_adi): c for c in self._cities}
        self._fetched_at = time.monotonic()

    def invalidate(self) -> None:
        self._fetched_at = 0.0
        self._universities = []
        self._program_groups = []
        self._cities = []
        self._uni_index = {}
        self._prog_index = {}
        self._city_index = {}

    @property
    def universities(self) -> list[University]:
        return list(self._universities)

    @property
    def program_groups(self) -> list[ProgramGroup]:
        return list(self._program_groups)

    @property
    def cities(self) -> list[City]:
        return list(self._cities)

    # --- fuzzy resolution ---------------------------------------------------

    def resolve_university(self, name: str, *, cutoff: float = 0.6) -> University:
        return self._resolve(name, self._uni_index, kind="university", cutoff=cutoff)  # type: ignore[return-value]

    def resolve_program(self, name: str, *, cutoff: float = 0.6) -> ProgramGroup:
        return self._resolve(name, self._prog_index, kind="program", cutoff=cutoff)  # type: ignore[return-value]

    def resolve_city(self, name: str, *, cutoff: float = 0.6) -> City:
        return self._resolve(name, self._city_index, kind="city", cutoff=cutoff)  # type: ignore[return-value]

    @staticmethod
    def _resolve(name: str, index: dict[str, object], *, kind: str, cutoff: float):  # noqa: ANN401
        if not name:
            raise _LookupError(name, kind=kind)
        key = normalize(name)
        if key in index:
            return index[key]
        # Substring contains
        for k, v in index.items():
            if key in k or k in key:
                return v
        # Fuzzy fallback
        keys = list(index.keys())
        matches = get_close_matches(key, keys, n=5, cutoff=cutoff)
        if matches:
            return index[matches[0]]
        raise _LookupError(name, kind=kind, suggestions=get_close_matches(key, keys, n=3, cutoff=0.4))


__all__ = ["LookupCache", "normalize"]
