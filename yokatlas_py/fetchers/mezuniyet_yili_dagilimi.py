"""
Mezuniyet Yili Dagilimi (Graduation Year Distribution) Fetcher.

This module provides class-based fetchers for retrieving graduation year
distribution data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class MezuniyetYiliDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for mezuniyet yili dagilimi (graduation year distribution) data.

    Parses a table with graduation years, counts, and a totals row.

    Table format:
        | Mezuniyet Yılı | 2024 | 2023 | 2022 |
        |----------------|------|------|------|
        | 2024           | 50   | -    | -    |
        | 2023           | 30   | 45   | -    |
        | Toplam         | 100  | 100  | 100  |
    """

    RESULT_KEY = "mezuniyet_yili_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract graduation year distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with mezuniyet_yili_dagilimi list and toplam dict
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_table_with_totals(
            soup,
            self.RESULT_KEY,
            first_col_header="Mezuniyet Yılı"
        )


class MezuniyetYiliDagilimiLisansFetcher(MezuniyetYiliDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) program graduation year distribution."""

    ENDPOINT = "1030b.php"
    PROGRAM_TYPE = "lisans"


class MezuniyetYiliDagilimiOnlisansFetcher(MezuniyetYiliDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) program graduation year distribution."""

    ENDPOINT = "3030b.php"
    PROGRAM_TYPE = "onlisans"
