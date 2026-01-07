"""
Yerlesen Puan Bilgileri (Placement Score Information) Fetcher.

Multi-table parser with dynamic headers for placement score information.
Note: This fetcher is only available for Lisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenPuanBilgileriBaseFetcher(BaseFetcher):
    """Base fetcher for placement score information."""

    RESULT_KEY = "yerlesen_puan_bilgileri"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract placement score information."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}

        # Initialize result dictionary
        result: dict[str, Any] = {}

        for i, table in enumerate(tables[:2]):
            rows = table.find_all("tr")
            headers = [header.get_text(strip=True) for header in rows[0].find_all("th")]

            if len(headers) >= 3:
                # First table: ortalama_puanlar, Second table: en_dusuk_puanlar
                category = "ortalama_puanlar" if i == 0 else "en_dusuk_puanlar"
                result[category] = {headers[1]: {}, headers[2]: {}}

                for row in rows[1:]:  # Skip the first header row
                    cols = row.find_all("td")
                    if len(cols) == 3:
                        key = cols[0].get_text(strip=True)
                        for j, header in enumerate(headers[1:], start=1):
                            value = cols[j].get_text(strip=True).replace(",", ".")
                            try:
                                value = float(value)
                            except ValueError:
                                pass
                            result[category][header][key] = value

        return result


class YerlesenPuanBilgileriLisansFetcher(YerlesenPuanBilgileriBaseFetcher):
    """Lisans fetcher for placement score information."""

    ENDPOINT = "1220.php"
    PROGRAM_TYPE = "lisans"


# Note: There is no onlisans equivalent for this fetcher
