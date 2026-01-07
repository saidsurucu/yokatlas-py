"""
Kontenjan Yerlesme (Quota and Placement) Fetcher.

This module provides class-based fetchers for retrieving quota and placement
data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class KontenjanYerlesmeBaseFetcher(BaseFetcher):
    """
    Base fetcher for kontenjan yerlesme (quota and placement) data.

    Parses a simple table with quota types and yearly placement data.

    Table format:
        | Tür           | 2024 | 2023 | 2022 |
        |---------------|------|------|------|
        | Genel         | 100  | 95   | 90   |
        | Ek Kontenjan  | 5    | 5    | 5    |
    """

    RESULT_KEY = "kontenjan_yerlesme"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract quota and placement data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with kontenjan_yerlesme key containing list of dicts
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(soup, self.RESULT_KEY, first_col_header="Tür")


class KontenjanYerlesmeLisansFetcher(KontenjanYerlesmeBaseFetcher):
    """Fetcher for lisans (bachelor's) program quota and placement."""

    ENDPOINT = "1000_2.php"
    PROGRAM_TYPE = "lisans"


class KontenjanYerlesmeOnlisansFetcher(KontenjanYerlesmeBaseFetcher):
    """Fetcher for onlisans (associate) program quota and placement."""

    ENDPOINT = "3000_2.php"
    PROGRAM_TYPE = "onlisans"
