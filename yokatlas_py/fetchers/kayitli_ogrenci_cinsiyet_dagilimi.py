"""
Kayitli Ogrenci Cinsiyet Dagilimi (Enrolled Students Gender Distribution) Fetcher.

This module provides class-based fetchers for retrieving enrolled students
gender distribution from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class KayitliOgrenciCinsiyetDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for kayitli ogrenci cinsiyet dagilimi data.

    Parses a table with gender types and yearly enrolled student counts.

    Table format:
        | Cinsiyet | 2024 | 2023 | 2022 |
        |----------|------|------|------|
        | Erkek    | 250  | 245  | 240  |
        | Kadin    | 150  | 155  | 160  |
    """

    RESULT_KEY = "kayitli_ogrenci_cinsiyet_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract enrolled students gender distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with kayitli_ogrenci_cinsiyet_dagilimi key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Cinsiyet"
        )


class KayitliOgrenciCinsiyetDagilimiLisansFetcher(KayitliOgrenciCinsiyetDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) enrolled students gender distribution."""

    ENDPOINT = "2010.php"
    PROGRAM_TYPE = "lisans"


class KayitliOgrenciCinsiyetDagilimiOnlisansFetcher(KayitliOgrenciCinsiyetDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) enrolled students gender distribution."""

    ENDPOINT = "2010.php"
    PROGRAM_TYPE = "onlisans"
