"""
Yerlesen Basari Siralari (Placement Success Rankings) Fetcher.

Multi-table parser with dynamic headers for placement success rankings.
Note: This fetcher is only available for Lisans programs.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class YerlesenBasariSiralariBaseFetcher(BaseFetcher):
    """Base fetcher for placement success rankings."""

    RESULT_KEY = "yerlesen_basari_siralari"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract placement success rankings."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}

        # Initialize result dictionary dynamically
        result: dict[str, Any] = {"ortalama_basari_siralari": {}, "en_dusuk_basari_siralari": {}}

        for i, table in enumerate(tables[:2]):
            rows = table.find_all("tr")
            headers = [
                header.get_text(strip=True) for header in rows[0].find_all("th")
            ]

            # Ensure the structure exists based on the headers
            if len(headers) >= 3:
                category = "ortalama_basari_siralari" if i == 0 else "en_dusuk_basari_siralari"
                result[category][headers[1]] = {}
                result[category][headers[2]] = {}

                for row in rows[1:]:  # Skip the first header row
                    cols = row.find_all("td")
                    if len(cols) == 3:
                        key = cols[0].get_text(strip=True)
                        value_012 = cols[1].get_text(strip=True)
                        value_012_006 = cols[2].get_text(strip=True)

                        # Convert numerical values to int, if possible
                        try:
                            value_012 = int(value_012.replace(".", ""))
                        except ValueError:
                            pass
                        try:
                            value_012_006 = int(value_012_006.replace(".", ""))
                        except ValueError:
                            pass

                        result[category][headers[1]][key] = value_012
                        result[category][headers[2]][key] = value_012_006

        return result


class YerlesenBasariSiralariLisansFetcher(YerlesenBasariSiralariBaseFetcher):
    """Lisans fetcher for placement success rankings."""

    ENDPOINT = "1230.php"
    PROGRAM_TYPE = "lisans"


# Note: There is no onlisans equivalent for this fetcher
