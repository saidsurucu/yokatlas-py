"""
Tercih Edilen Programlar (Preferred Programs) Fetcher.

Simple 2-column table parser for preferred programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihEdilenProgramlarBaseFetcher(BaseFetcher):
    """Base fetcher for preferred programs."""

    RESULT_KEY = "tercih_edilen_programlar"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract preferred programs."""
        soup = self.create_soup(html_content, clean=True)
        table = self.find_table(soup)

        if not table:
            return {"error": "Required table not found in the HTML content"}

        result = []

        rows = table.find_all("tr")
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all("td")
            if len(cols) == 2:
                program = cols[0].get_text(strip=True)
                try:
                    tercih_sayisi = int(cols[1].get_text(strip=True))
                except ValueError:
                    tercih_sayisi = 0
                result.append({"program": program, "tercih_sayisi": tercih_sayisi})

        return {self.RESULT_KEY: result}


class TercihEdilenProgramlarLisansFetcher(TercihEdilenProgramlarBaseFetcher):
    """Lisans fetcher for preferred programs."""

    ENDPOINT = "1340b.php"
    PROGRAM_TYPE = "lisans"


class TercihEdilenProgramlarOnlisansFetcher(TercihEdilenProgramlarBaseFetcher):
    """Onlisans fetcher for preferred programs."""

    ENDPOINT = "3340bb.php"
    PROGRAM_TYPE = "onlisans"
