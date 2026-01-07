"""Yerleşen Başarı Sıraları (Placement Success Rankings) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.yerlesen_basari_siralari import YerlesenBasariSiralariLisansFetcher


async def fetch_yerlesen_basari_siralari(program_id: str, year: int) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = YerlesenBasariSiralariLisansFetcher(program_id, year)
    return await fetcher.fetch()
