"""
Tercih Edilen Universite Turleri (Preferred University Types) Fetcher.

Key-value dictionary parser for preferred university types.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihEdilenUniversiteTurleriBaseFetcher(BaseFetcher):
    """Base fetcher for preferred university types."""

    RESULT_KEY = "tercih_edilen_universite_turleri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract preferred university types."""
        soup = self.create_soup(html_content, clean=True)
        table = self.find_table(soup)

        if not table:
            return {"error": "Required table not found in the HTML content"}

        result: dict[str, Any] = {}

        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                if value == "---":
                    value = 0
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                result[key] = value

        return {self.RESULT_KEY: result}


class TercihEdilenUniversiteTurleriLisansFetcher(TercihEdilenUniversiteTurleriBaseFetcher):
    """Lisans fetcher for preferred university types."""

    ENDPOINT = "1310.php"
    PROGRAM_TYPE = "lisans"


class TercihEdilenUniversiteTurleriOnlisansFetcher(TercihEdilenUniversiteTurleriBaseFetcher):
    """Onlisans fetcher for preferred university types."""

    ENDPOINT = "3310b.php"
    PROGRAM_TYPE = "onlisans"
