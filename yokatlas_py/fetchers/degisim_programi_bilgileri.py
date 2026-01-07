"""
Degisim Programi Bilgileri (Exchange Program Information) Fetcher.

This module provides class-based fetchers for retrieving exchange program
information from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class DegisimProgramiBilgileriBaseFetcher(BaseFetcher):
    """
    Base fetcher for degisim programi bilgileri data.

    Parses a table with exchange program details and statistics.

    Table format:
        | Program      | Giden | Gelen |
        |--------------|-------|-------|
        | Erasmus      | 25    | 30    |
        | Mevlana      | 10    | 15    |
    """

    RESULT_KEY = "degisim_programi_bilgileri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract exchange program data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with degisim_programi_bilgileri key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Program"
        )


class DegisimProgramiBilgileriLisansFetcher(DegisimProgramiBilgileriBaseFetcher):
    """Fetcher for lisans (bachelor's) exchange program information."""

    ENDPOINT = "2040.php"
    PROGRAM_TYPE = "lisans"


class DegisimProgramiBilgileriOnlisansFetcher(DegisimProgramiBilgileriBaseFetcher):
    """Fetcher for onlisans (associate) exchange program information."""

    ENDPOINT = "2040.php"
    PROGRAM_TYPE = "onlisans"
