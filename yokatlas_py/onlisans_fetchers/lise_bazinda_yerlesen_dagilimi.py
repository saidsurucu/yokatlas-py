"""Lise Bazında Yerleşen Dağılımı (Placement Distribution by High School) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.lise_bazinda_yerlesen_dagilimi import LiseBazindaYerlesenDagilimiOnlisansFetcher


async def fetch_lise_bazinda_yerlesen_dagilimi(
    program_id: str, year: int
) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = LiseBazindaYerlesenDagilimiOnlisansFetcher(program_id, year)
    return await fetcher.fetch()
