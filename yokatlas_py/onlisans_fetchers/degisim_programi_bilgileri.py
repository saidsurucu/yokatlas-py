"""
Degisim Programi Bilgileri (Exchange Program Info) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use DegisimProgramiBilgileriOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.degisim_programi_bilgileri import DegisimProgramiBilgileriOnlisansFetcher


async def fetch_degisim_programi_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch exchange program information for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = DegisimProgramiBilgileriOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
