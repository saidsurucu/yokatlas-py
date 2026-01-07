"""
Yerlesen Il Dagilimi (Placed Students City Distribution) Fetcher.

This module provides class-based fetchers for retrieving placed students
city distribution from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenIlDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for yerlesen il dagilimi (city distribution) data.

    Parses a table with city names and placement counts by year.

    Table format:
        | İl         | 2024 | 2023 | 2022 |
        |------------|------|------|------|
        | İstanbul   | 30   | 28   | 25   |
        | Ankara     | 20   | 22   | 18   |
    """

    RESULT_KEY = "yerlesen_il_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract city distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with yerlesen_il_dagilimi key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="İl"
        )


class YerlesenIlDagilimiLisansFetcher(YerlesenIlDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) city distribution."""

    ENDPOINT = "1020c.php"
    PROGRAM_TYPE = "lisans"


class YerlesenIlDagilimiOnlisansFetcher(YerlesenIlDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) city distribution."""

    ENDPOINT = "3020c.php"
    PROGRAM_TYPE = "onlisans"
