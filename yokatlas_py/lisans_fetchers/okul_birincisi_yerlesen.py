"""
Okul Birincisi Yerlesen (Valedictorian Placement) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use OkulBirincisiYerlesenLisansFetcher directly.
"""

from typing import Any

from ..fetchers.okul_birincisi_yerlesen import OkulBirincisiYerlesenLisansFetcher


async def fetch_okul_birincisi_yerlesen(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch valedictorian placement data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = OkulBirincisiYerlesenLisansFetcher(program_id, year)
    return await fetcher.fetch()
