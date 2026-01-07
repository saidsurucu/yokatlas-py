"""Yerleşen Puan Bilgileri (Placement Score Information) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.yerlesen_puan_bilgileri import YerlesenPuanBilgileriLisansFetcher


async def fetch_yerlesen_puan_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenPuanBilgileriLisansFetcher(program_id, year)
    return await fetcher.fetch()
