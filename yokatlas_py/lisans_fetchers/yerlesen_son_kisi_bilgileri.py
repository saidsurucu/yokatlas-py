"""
Yerlesen Son Kisi Bilgileri (Last Placed Student Info) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YerlesenSonKisiBilgileriLisansFetcher directly.
"""

from typing import Any

from ..fetchers.yerlesen_son_kisi_bilgileri import YerlesenSonKisiBilgileriLisansFetcher


async def fetch_yerlesen_son_kisi_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch last placed student info for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenSonKisiBilgileriLisansFetcher(program_id, year)
    return await fetcher.fetch()
