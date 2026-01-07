"""
Yerlesen Tercih Istatistikleri (Placed Students Preference Statistics) Fetcher.

This module provides class-based fetchers for retrieving preference statistics
of placed students from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenTercihIstatistikleriBaseFetcher(BaseFetcher):
    """
    Base fetcher for yerlesen tercih istatistikleri data.

    Parses a table with preference order statistics and yearly data.

    Table format:
        | Tercih Sırası | 2024 | 2023 | 2022 |
        |---------------|------|------|------|
        | 1             | 20   | 18   | 15   |
        | 2             | 15   | 14   | 12   |
    """

    RESULT_KEY = "yerlesen_tercih_istatistikleri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract preference statistics data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with yerlesen_tercih_istatistikleri key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Tercih Sırası"
        )


class YerlesenTercihIstatistikleriLisansFetcher(YerlesenTercihIstatistikleriBaseFetcher):
    """Fetcher for lisans (bachelor's) preference statistics."""

    ENDPOINT = "1040.php"
    PROGRAM_TYPE = "lisans"


class YerlesenTercihIstatistikleriOnlisansFetcher(YerlesenTercihIstatistikleriBaseFetcher):
    """Fetcher for onlisans (associate) preference statistics."""

    ENDPOINT = "3040.php"
    PROGRAM_TYPE = "onlisans"
