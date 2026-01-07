"""
Yerlesen Ortalama Netler (Average Net Scores) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YerlesenOrtalamaNetlerLisansFetcher directly.
"""

from typing import Any

from ..fetchers.yerlesen_ortalama_netler import YerlesenOrtalamaNetlerLisansFetcher


async def fetch_yerlesen_ortalama_netler(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch average net scores data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenOrtalamaNetlerLisansFetcher(program_id, year)
    return await fetcher.fetch()
