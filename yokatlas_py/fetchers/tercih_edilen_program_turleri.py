"""
Tercih Edilen Program Turleri (Preferred Program Types) Fetcher.

Key-value dictionary parser for preferred program types.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihEdilenProgramTurleriBaseFetcher(BaseFetcher):
    """Base fetcher for preferred program types."""

    RESULT_KEY = "tercih_edilen_program_turleri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract preferred program types."""
        soup = self.create_soup(html_content, clean=True)
        table = self.find_table(soup)

        if not table:
            return {"error": "Required table not found in the HTML content"}

        result: dict[str, Any] = {}

        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all("td")
            if len(cols) == 2:
                program_type = cols[0].get_text(strip=True).replace('"', "")
                tercih_sayisi = cols[1].get_text(strip=True)
                try:
                    result[program_type] = int(tercih_sayisi) if tercih_sayisi != "---" else 0
                except ValueError:
                    result[program_type] = 0

        return {self.RESULT_KEY: result}


class TercihEdilenProgramTurleriLisansFetcher(TercihEdilenProgramTurleriBaseFetcher):
    """Lisans fetcher for preferred program types."""

    ENDPOINT = "1340a.php"
    PROGRAM_TYPE = "lisans"


class TercihEdilenProgramTurleriOnlisansFetcher(TercihEdilenProgramTurleriBaseFetcher):
    """Onlisans fetcher for preferred program types."""

    ENDPOINT = "3340ab.php"
    PROGRAM_TYPE = "onlisans"
