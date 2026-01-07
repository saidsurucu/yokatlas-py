"""
Lise Alani Dagilimi (High School Field Distribution) Fetcher.

This module provides class-based fetchers for retrieving high school field
distribution data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class LiseAlaniDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for lise alani dagilimi (high school field distribution) data.

    Parses a table with high school fields and yearly placement counts.

    Table format:
        | Lise Alanı | 2024 | 2023 | 2022 |
        |------------|------|------|------|
        | Sayısal    | 80   | 75   | 70   |
        | Eşit Ağ.   | 20   | 25   | 30   |
    """

    RESULT_KEY = "lise_alani_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract high school field distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with lise_alani_dagilimi key containing list of dicts
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Lise Alanı"
        )


class LiseAlaniDagilimiLisansFetcher(LiseAlaniDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) program high school field distribution."""

    ENDPOINT = "1050b.php"
    PROGRAM_TYPE = "lisans"


class LiseAlaniDagilimiOnlisansFetcher(LiseAlaniDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) program high school field distribution."""

    ENDPOINT = "3050b.php"
    PROGRAM_TYPE = "onlisans"
