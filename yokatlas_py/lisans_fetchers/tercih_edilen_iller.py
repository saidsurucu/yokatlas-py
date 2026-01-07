"""
Tercih Edilen Iller (Preferred Cities) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use TercihEdilenIllerLisansFetcher directly.
"""

from typing import Any

from ..fetchers.tercih_edilen_iller import TercihEdilenIllerLisansFetcher


async def fetch_tercih_edilen_iller(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch preferred cities data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = TercihEdilenIllerLisansFetcher(program_id, year)
    return await fetcher.fetch()
