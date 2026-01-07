"""
Kontenjan Yerlesme (Quota and Placement) Fetcher for Lisans Programs.

This module provides backward-compatible function interface that delegates
to the new class-based fetcher.

Note: This is a wrapper for backward compatibility.
      New code should use KontenjanYerlesmeLisansFetcher directly.
"""

from typing import Any

from ..fetchers.kontenjan_yerlesme import KontenjanYerlesmeLisansFetcher


async def fetch_kontenjan_yerlesme(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch quota and placement data for a lisans program.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = KontenjanYerlesmeLisansFetcher(program_id, year)
    return await fetcher.fetch()
