"""
Akademisyen Sayilari (Academic Staff Numbers) Fetcher.

This module provides class-based fetchers for retrieving academic staff
numbers from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class AkademisyenSayilariBaseFetcher(BaseFetcher):
    """
    Base fetcher for akademisyen sayilari (academic staff numbers) data.

    Parses a table with academic titles and staff counts.

    Table format:
        | Unvan      | Sayı |
        |------------|------|
        | Profesör   | 15   |
        | Doçent     | 20   |
        | Dr. Öğr.   | 25   |
    """

    RESULT_KEY = "akademisyen_sayilari"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract academic staff numbers data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with akademisyen_sayilari key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Unvan"
        )


class AkademisyenSayilariLisansFetcher(AkademisyenSayilariBaseFetcher):
    """Fetcher for lisans (bachelor's) academic staff numbers."""

    ENDPOINT = "2050.php"
    PROGRAM_TYPE = "lisans"


class AkademisyenSayilariOnlisansFetcher(AkademisyenSayilariBaseFetcher):
    """Fetcher for onlisans (associate) academic staff numbers."""

    ENDPOINT = "2050.php"
    PROGRAM_TYPE = "onlisans"
