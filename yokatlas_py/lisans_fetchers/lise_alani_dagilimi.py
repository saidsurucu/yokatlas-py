"""
Lise Alani Dagilimi (High School Field Distribution) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use LiseAlaniDagilimiLisansFetcher directly.
"""

from typing import Any

from ..fetchers.lise_alani_dagilimi import LiseAlaniDagilimiLisansFetcher


async def fetch_lise_alani_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch high school field distribution data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = LiseAlaniDagilimiLisansFetcher(program_id, year)
    return await fetcher.fetch()
