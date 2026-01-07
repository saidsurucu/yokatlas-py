"""Şehir ve Coğrafi Bölge Dağılımı (City and Geographic Region Distribution) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.sehir_ve_cografi_bolge_dagilimi import SehirVeCografiBolgeDagilimiLisansFetcher


async def fetch_sehir_ve_cografi_bolge_dagilimi(
    program_id: str, year: int
) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = SehirVeCografiBolgeDagilimiLisansFetcher(program_id, year)
    return await fetcher.fetch()
