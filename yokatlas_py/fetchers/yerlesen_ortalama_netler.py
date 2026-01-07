"""
Yerlesen Ortalama Netler (Placed Students Average Net Scores) Fetcher.

This module provides class-based fetchers for retrieving average net scores
of placed students from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenOrtalamaNetlerBaseFetcher(BaseFetcher):
    """
    Base fetcher for yerlesen ortalama netler (average net scores) data.

    Parses a table with subject areas and average net scores by year.

    Table format:
        | Ders          | 2024  | 2023  | 2022  |
        |---------------|-------|-------|-------|
        | Matematik     | 35.5  | 34.2  | 33.8  |
        | Fen Bilimleri | 28.3  | 27.1  | 26.5  |
    """

    RESULT_KEY = "yerlesen_ortalama_netler"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract average net scores data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with yerlesen_ortalama_netler key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Ders"
        )


class YerlesenOrtalamaNetlerLisansFetcher(YerlesenOrtalamaNetlerBaseFetcher):
    """Fetcher for lisans (bachelor's) average net scores."""

    ENDPOINT = "1210a.php"
    PROGRAM_TYPE = "lisans"


class YerlesenOrtalamaNetlerOnlisansFetcher(YerlesenOrtalamaNetlerBaseFetcher):
    """Fetcher for onlisans (associate) average net scores."""

    ENDPOINT = "3210a.php"
    PROGRAM_TYPE = "onlisans"
