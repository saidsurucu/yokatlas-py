"""
Yerlesen Son Kisi Bilgileri (Last Placed Student Info) Fetcher.

This module provides class-based fetchers for retrieving last placed student
information from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenSonKisiBilgileriBaseFetcher(BaseFetcher):
    """
    Base fetcher for yerlesen son kisi bilgileri data.

    Parses a table with last placed student statistics by year.

    Table format:
        | Bilgi        | 2024   | 2023   | 2022   |
        |--------------|--------|--------|--------|
        | Puan         | 450.5  | 445.3  | 440.1  |
        | Başarı Sır.  | 15000  | 16000  | 17000  |
    """

    RESULT_KEY = "yerlesen_son_kisi_bilgileri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract last placed student info.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with yerlesen_son_kisi_bilgileri key
        """
        soup = self.create_soup(html_content, clean=True)
        return self.parse_single_table(
            soup,
            self.RESULT_KEY,
            first_col_header="Bilgi"
        )


class YerlesenSonKisiBilgileriLisansFetcher(YerlesenSonKisiBilgileriBaseFetcher):
    """Fetcher for lisans (bachelor's) last placed student info."""

    ENDPOINT = "1070.php"
    PROGRAM_TYPE = "lisans"


class YerlesenSonKisiBilgileriOnlisansFetcher(YerlesenSonKisiBilgileriBaseFetcher):
    """Fetcher for onlisans (associate) last placed student info."""

    ENDPOINT = "3070.php"
    PROGRAM_TYPE = "onlisans"
