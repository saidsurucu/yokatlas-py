"""
Tercih Kullanma Oranlari (Preference Usage Rates) Fetcher.

This module provides class-based fetchers for retrieving preference usage
rates data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihKullanmaOranlariBaseFetcher(BaseFetcher):
    """
    Base fetcher for tercih kullanma oranlari (preference usage rates) data.

    Parses a table with preference counts and percentages.

    Table format:
        | Tercih Sayısı | Aday Sayısı | Oran (%) |
        |---------------|-------------|----------|
        | 1-5           | 500         | 25       |
        | 6-10          | 400         | 20       |
    """

    RESULT_KEY = "tercih_kullanma_oranlari"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract preference usage rates data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with tercih_kullanma_oranlari key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Tercih Sayısı"
        )


class TercihKullanmaOranlariLisansFetcher(TercihKullanmaOranlariBaseFetcher):
    """Fetcher for lisans (bachelor's) preference usage rates."""

    ENDPOINT = "1300.php"
    PROGRAM_TYPE = "lisans"


class TercihKullanmaOranlariOnlisansFetcher(TercihKullanmaOranlariBaseFetcher):
    """Fetcher for onlisans (associate) preference usage rates."""

    ENDPOINT = "3300_2.php"
    PROGRAM_TYPE = "onlisans"
