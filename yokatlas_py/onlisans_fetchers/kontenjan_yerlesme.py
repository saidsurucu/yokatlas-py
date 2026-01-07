"""
Kontenjan Yerlesme (Quota and Placement) Fetcher for Onlisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use KontenjanYerlesmeOnlisansFetcher directly.
"""

from typing import Any

from ..fetchers.kontenjan_yerlesme import KontenjanYerlesmeOnlisansFetcher


async def fetch_kontenjan_yerlesme(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch quota and placement data for an onlisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = KontenjanYerlesmeOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
