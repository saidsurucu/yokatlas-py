"""
Yerlesen Il Dagilimi (City Distribution) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YerlesenIlDagilimiLisansFetcher directly.
"""

from typing import Any

from ..fetchers.yerlesen_il_dagilimi import YerlesenIlDagilimiLisansFetcher


async def fetch_yerlesen_il_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch city distribution data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenIlDagilimiLisansFetcher(program_id, year)
    return await fetcher.fetch()
