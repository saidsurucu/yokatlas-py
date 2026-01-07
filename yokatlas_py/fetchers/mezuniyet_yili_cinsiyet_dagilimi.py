"""
Mezuniyet Yili Cinsiyet Dagilimi (Graduation Year Gender Distribution) Fetcher.

This module provides class-based fetchers for retrieving graduation year
gender distribution from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class MezuniyetYiliCinsiyetDagilimiBaseFetcher(BaseFetcher):
    """
    Base fetcher for mezuniyet yili cinsiyet dagilimi data.

    Parses a table with graduation years by gender and year.

    Table format:
        | Mezuniyet Yılı | Erkek 2024 | Kadin 2024 | Erkek 2023 | ...
        |----------------|------------|------------|------------|
        | 2024           | 30         | 20         | -          |
    """

    RESULT_KEY = "mezuniyet_yili_cinsiyet_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract graduation year gender distribution data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with mezuniyet_yili_cinsiyet_dagilimi key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Mezuniyet Yılı"
        )


class MezuniyetYiliCinsiyetDagilimiLisansFetcher(MezuniyetYiliCinsiyetDagilimiBaseFetcher):
    """Fetcher for lisans (bachelor's) graduation year gender distribution."""

    ENDPOINT = "2030.php"
    PROGRAM_TYPE = "lisans"


class MezuniyetYiliCinsiyetDagilimiOnlisansFetcher(MezuniyetYiliCinsiyetDagilimiBaseFetcher):
    """Fetcher for onlisans (associate) graduation year gender distribution."""

    ENDPOINT = "2030.php"
    PROGRAM_TYPE = "onlisans"
