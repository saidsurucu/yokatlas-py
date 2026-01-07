"""Lise Grubu ve Tipi Dağılımı (High School Group and Type Distribution) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.lise_grubu_ve_tipi_dagilimi import LiseGrubuVeTipiDagilimiOnlisansFetcher


async def fetch_lise_grubu_ve_tipi_dagilimi(
    program_id: str, year: int
) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = LiseGrubuVeTipiDagilimiOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
