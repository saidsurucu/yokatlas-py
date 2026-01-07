"""
Mezuniyet Yili Cinsiyet Dagilimi (Graduation Year Gender) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use MezuniyetYiliCinsiyetDagilimiOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.mezuniyet_yili_cinsiyet_dagilimi import MezuniyetYiliCinsiyetDagilimiOnlisansFetcher


async def fetch_mezuniyet_yili_cinsiyet_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch graduation year gender distribution data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = MezuniyetYiliCinsiyetDagilimiOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
