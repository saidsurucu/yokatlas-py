"""
Akademisyen Sayilari (Academic Staff Numbers) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use AkademisyenSayilariOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.akademisyen_sayilari import AkademisyenSayilariOnlisansFetcher


async def fetch_akademisyen_sayilari(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch academic staff numbers data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = AkademisyenSayilariOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
