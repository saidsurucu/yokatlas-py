"""
Ogrenim Durumu (Education Status) Fetcher.

This module provides class-based fetchers for retrieving education status
distribution data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class OgrenimDurumuBaseFetcher(BaseFetcher):
    """
    Base fetcher for ogrenim durumu (education status) data.

    Parses a table with education status types, yearly counts, and a totals row.
    The totals row is separated from the main data.

    Table format:
        | Öğrenim Durumu | 2024 | 2023 | 2022 |
        |----------------|------|------|------|
        | İlk Öğretim    | 50   | 48   | 45   |
        | Orta Öğretim   | 50   | 52   | 55   |
        | Toplam         | 100  | 100  | 100  |
    """

    RESULT_KEY = "ogrenim_durumu"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract education status data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with ogrenim_durumu list and toplam dict
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_table_with_totals(
            soup,
            self.RESULT_KEY,
            first_col_header="Öğrenim Durumu"
        )


class OgrenimDurumuLisansFetcher(OgrenimDurumuBaseFetcher):
    """Fetcher for lisans (bachelor's) program education status."""

    ENDPOINT = "1030a.php"
    PROGRAM_TYPE = "lisans"


class OgrenimDurumuOnlisansFetcher(OgrenimDurumuBaseFetcher):
    """Fetcher for onlisans (associate) program education status."""

    ENDPOINT = "3030a.php"
    PROGRAM_TYPE = "onlisans"
