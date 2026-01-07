"""
Yatay Gecis Bilgileri (Lateral Transfer Info) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YatayGecisBilgileriOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.yatay_gecis_bilgileri import YatayGecisBilgileriOnlisansFetcher


async def fetch_yatay_gecis_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch lateral transfer information for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YatayGecisBilgileriOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
