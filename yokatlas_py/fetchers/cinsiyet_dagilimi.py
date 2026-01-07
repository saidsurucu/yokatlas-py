"""
Cinsiyet Dagilimi (Gender Distribution) Fetcher.

This module provides class-based fetchers for retrieving gender distribution
data from YOKATLAS for both lisans and onlisans programs.

Usage:
    # Direct class usage (new pattern)
    fetcher = CinsiyetDagilimiLisansFetcher("123456789", 2024)
    result = await fetcher.fetch()

    # Legacy function usage (backward compatible)
    from yokatlas_py.lisans_fetchers.cinsiyet_dagilimi import fetch_cinsiyet_dagilimi
    result = await fetch_cinsiyet_dagilimi("123456789", 2024)
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class CinsiyetDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for cinsiyet dagilimi (gender distribution) data.

    Parses a simple table with gender types (Erkek/Kadin) and yearly counts.

    Table format:
        | Cinsiyet | 2024 | 2023 | 2022 |
        |----------|------|------|------|
        | Erkek    | 50   | 48   | 45   |
        | Kadin    | 50   | 52   | 55   |
    """

    RESULT_KEY = "cinsiyet_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract gender distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with cinsiyet_dagilimi key containing list of dicts
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(soup, self.RESULT_KEY, first_col_header="Type")


class CinsiyetDagilimiLisansFetcher(CinsiyetDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) program gender distribution."""

    ENDPOINT = "1010.php"
    PROGRAM_TYPE = "lisans"


class CinsiyetDagilimiOnlisansFetcher(CinsiyetDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) program gender distribution."""

    ENDPOINT = "3010.php"
    PROGRAM_TYPE = "onlisans"
