"""
Okul Birincisi Yerlesen (School Valedictorian Placement) Fetcher.

This module provides class-based fetchers for retrieving school valedictorian
placement data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class OkulBirincisiYerlesenBaseFetcher(BaseFetcher):
    """
    Base fetcher for okul birincisi yerlesen (valedictorian placement) data.

    Parses a table with placement types and yearly counts with totals.

    Table format:
        | Yerleşme Türü     | 2024 | 2023 | 2022 |
        |-------------------|------|------|------|
        | Normal            | 95   | 90   | 88   |
        | Okul Birincisi    | 5    | 10   | 12   |
        | Toplam            | 100  | 100  | 100  |
    """

    RESULT_KEY = "okul_birincisi_yerlesen"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract valedictorian placement data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with okul_birincisi_yerlesen list and toplam dict
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_table_with_totals(
            soup,
            self.RESULT_KEY,
            first_col_header="Yerleşme Türü"
        )


class OkulBirincisiYerlesenLisansFetcher(OkulBirincisiYerlesenBaseFetcher):
    """Fetcher for lisans (bachelor's) valedictorian placement."""

    ENDPOINT = "1030c.php"
    PROGRAM_TYPE = "lisans"


class OkulBirincisiYerlesenOnlisansFetcher(OkulBirincisiYerlesenBaseFetcher):
    """Fetcher for onlisans (associate) valedictorian placement."""

    ENDPOINT = "3030c.php"
    PROGRAM_TYPE = "onlisans"
