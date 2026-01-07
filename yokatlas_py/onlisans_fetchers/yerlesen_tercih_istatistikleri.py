"""
Yerlesen Tercih Istatistikleri (Placement Preference Statistics) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YerlesenTercihIstatistikleriOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.yerlesen_tercih_istatistikleri import YerlesenTercihIstatistikleriOnlisansFetcher


async def fetch_yerlesen_tercih_istatistikleri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch placement preference statistics for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenTercihIstatistikleriOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
