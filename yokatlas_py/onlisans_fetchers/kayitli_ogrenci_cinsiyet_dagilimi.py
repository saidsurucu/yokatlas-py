"""
Kayitli Ogrenci Cinsiyet Dagilimi (Enrolled Students Gender) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use KayitliOgrenciCinsiyetDagilimiOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.kayitli_ogrenci_cinsiyet_dagilimi import KayitliOgrenciCinsiyetDagilimiOnlisansFetcher


async def fetch_kayitli_ogrenci_cinsiyet_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch enrolled students gender distribution data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = KayitliOgrenciCinsiyetDagilimiOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
