"""Tercih İstatistikleri (Preference Statistics) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.tercih_istatistikleri import TercihIstatistikleriLisansFetcher


async def fetch_tercih_istatistikleri(program_id: str, year: int) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = TercihIstatistikleriLisansFetcher(program_id, year)
    return await fetcher.fetch()
