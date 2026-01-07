"""Taban Puan ve Başarı Sırası İstatistikleri (Base Score and Success Ranking Statistics) fetcher wrapper for backward compatibility."""

from typing import Any

from ..fetchers.taban_puan_ve_basari_sirasi_istatistikleri import TabanPuanVeBasariSirasiIstatistikleriLisansFetcher


async def fetch_taban_puan_ve_basari_sirasi_istatistikleri(
    program_id: str, year: int
) -> dict[str, Any]:
    """Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    fetcher = TabanPuanVeBasariSirasiIstatistikleriLisansFetcher(program_id, year)
    return await fetcher.fetch()
