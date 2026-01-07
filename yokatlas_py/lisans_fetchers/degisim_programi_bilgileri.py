"""
Degisim Programi Bilgileri (Exchange Program Info) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use DegisimProgramiBilgileriLisansFetcher directly.
"""

from typing import Any

from ..fetchers.degisim_programi_bilgileri import DegisimProgramiBilgileriLisansFetcher


async def fetch_degisim_programi_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch exchange program information for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = DegisimProgramiBilgileriLisansFetcher(program_id, year)
    return await fetcher.fetch()
