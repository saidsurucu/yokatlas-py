"""
Yatay Gecis Bilgileri (Lateral Transfer Information) Fetcher.

This module provides class-based fetchers for retrieving lateral transfer
information from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YatayGecisBilgileriBaseFetcher(BaseFetcher):
    """
    Base fetcher for yatay gecis bilgileri (lateral transfer) data.

    Parses a table with transfer statistics by year.

    Table format:
        | Transfer Türü | 2024 | 2023 | 2022 |
        |---------------|------|------|------|
        | Gelen         | 10   | 8    | 7    |
        | Giden         | 5    | 6    | 4    |
    """

    RESULT_KEY = "yatay_gecis_bilgileri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract lateral transfer data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with yatay_gecis_bilgileri key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Transfer Türü"
        )


class YatayGecisBilgileriLisansFetcher(YatayGecisBilgileriBaseFetcher):
    """Fetcher for lisans (bachelor's) lateral transfer information."""

    ENDPOINT = "2060.php"
    PROGRAM_TYPE = "lisans"


class YatayGecisBilgileriOnlisansFetcher(YatayGecisBilgileriBaseFetcher):
    """Fetcher for onlisans (associate) lateral transfer information."""

    ENDPOINT = "2060.php"
    PROGRAM_TYPE = "onlisans"
