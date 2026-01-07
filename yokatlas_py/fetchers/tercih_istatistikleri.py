"""
Tercih Istatistikleri (Preference Statistics) Fetcher.

Multi-table parser for preference statistics data.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihIstatistikleriBaseFetcher(BaseFetcher):
    """Base fetcher for preference statistics."""

    RESULT_KEY = "tercih_istatistikleri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract preference statistics."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}

        result: dict[str, Any] = {"genel_istatistikler": {}, "tercih_sira_dagilimi": []}

        # First table: General statistics
        rows = tables[0].find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                if len(cols) == 3:
                    value = [value, cols[2].get_text(strip=True)]
                result["genel_istatistikler"][key] = value

        # Second table: Preference order distribution
        headers = [header.get_text(strip=True) for header in tables[1].find_all("th")]
        rows = tables[1].find_all("tr")
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all("td")
            row_data = {}
            for i, header in enumerate(headers):
                if i < len(cols):
                    value = (
                        cols[i].get_text(strip=True).replace(".", "")
                        if header == "Aday Sayısı"
                        else cols[i].get_text(strip=True)
                    )
                    row_data[header] = int(value) if header == "Aday Sayısı" else value
            result["tercih_sira_dagilimi"].append(row_data)

        return result


class TercihIstatistikleriLisansFetcher(TercihIstatistikleriBaseFetcher):
    """Lisans fetcher for preference statistics."""

    ENDPOINT = "1080.php"
    PROGRAM_TYPE = "lisans"


class TercihIstatistikleriOnlisansFetcher(TercihIstatistikleriBaseFetcher):
    """Onlisans fetcher for preference statistics."""

    ENDPOINT = "3080.php"
    PROGRAM_TYPE = "onlisans"
