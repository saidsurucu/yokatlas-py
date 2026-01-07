"""Genel Bilgiler (General Information) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.genel_bilgiler import GenelBilgilerLisansFetcher


async def fetch_genel_bilgiler(program_id: str, year: int) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = GenelBilgilerLisansFetcher(program_id, year)
    return await fetcher.fetch()
