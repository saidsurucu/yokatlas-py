"""
Ogrenim Durumu (Education Status) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use OgrenimDurumuOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.ogrenim_durumu import OgrenimDurumuOnlisansFetcher


async def fetch_ogrenim_durumu(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch education status data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = OgrenimDurumuOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
