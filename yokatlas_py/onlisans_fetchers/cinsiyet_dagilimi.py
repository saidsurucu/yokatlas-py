"""
Cinsiyet Dagilimi (Gender Distribution) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use CinsiyetDagilimiOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.cinsiyet_dagilimi import CinsiyetDagilimiOnlisansFetcher


async def fetch_cinsiyet_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch gender distribution data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message

    Example:
        >>> result = await fetch_cinsiyet_dagilimi("123456789", 2024)
        >>> print(result)
        {'cinsiyet_dagilimi': [{'Type': 'Erkek', '2024': '55', ...}, ...]}
    """
    fetcher = CinsiyetDagilimiOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
