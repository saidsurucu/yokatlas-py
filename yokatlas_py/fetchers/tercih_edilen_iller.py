"""
Tercih Edilen Iller (Preferred Cities) Fetcher.

This module provides class-based fetchers for retrieving preferred cities
data from YOKATLAS for both lisans and onlisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihEdilenIllerBaseFetcher(BaseFetcher):
    """
    Base fetcher for tercih edilen iller (preferred cities) data.

    Parses a simple two-column table with city names and preference counts.

    Table format:
        | Il         | Tercih Sayısı |
        |------------|---------------|
        | İstanbul   | 150           |
        | Ankara     | 120           |
    """

    RESULT_KEY = "tercih_edilen_iller"

    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract preferred cities data.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with tercih_edilen_iller key containing list of dicts
        """
        soup = self.create_soup(html_content, clean=True)
        table = self.find_table(soup)

        if not table:
            return {self.RESULT_KEY: []}

        result = []
        rows = table.find_all("tr")

        for row in rows[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) == 2:
                il = cols[0].get_text(strip=True)
                try:
                    tercih_sayisi = int(cols[1].get_text(strip=True))
                except ValueError:
                    tercih_sayisi = 0
                result.append({"il": il, "tercih_sayisi": tercih_sayisi})

        return {self.RESULT_KEY: result}


class TercihEdilenIllerLisansFetcher(TercihEdilenIllerBaseFetcher):
    """Fetcher for lisans (bachelor's) program preferred cities."""

    ENDPOINT = "1330.php"
    PROGRAM_TYPE = "lisans"


class TercihEdilenIllerOnlisansFetcher(TercihEdilenIllerBaseFetcher):
    """Fetcher for onlisans (associate) program preferred cities."""

    ENDPOINT = "3330b.php"
    PROGRAM_TYPE = "onlisans"
