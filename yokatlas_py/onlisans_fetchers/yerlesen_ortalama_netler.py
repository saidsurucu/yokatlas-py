"""
Yerlesen Ortalama Netler (Placement Average Scores) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use YerlesenOrtalamaNetlerOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.yerlesen_ortalama_netler import YerlesenOrtalamaNetlerOnlisansFetcher


async def fetch_yerlesen_ortalama_netler(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch placement average scores data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenOrtalamaNetlerOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
