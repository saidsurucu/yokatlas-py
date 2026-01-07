"""
Genel Bilgiler (General Info) Fetcher.

Multi-table key-value parser for program general information.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class GenelBilgilerBaseFetcher(BaseFetcher):
    """Base fetcher for general program information."""

    RESULT_KEY = "genel_bilgiler"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract general program information."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        details: dict[str, Any] = {}

        if len(tables) > 0:
            rows = tables[0].find_all("tr")
            program_info = {}
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace("*", "")
                    value = cols[1].get_text(strip=True).replace("*", "")
                    program_info[key] = value
            details["program_info"] = program_info

        if len(tables) > 1:
            rows = tables[1].find_all("tr")
            kontenjan_info = {}
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace("*", "")
                    value = cols[1].get_text(strip=True).replace("*", "")
                    kontenjan_info[key] = value
            details["kontenjan_info"] = kontenjan_info

        if len(tables) > 2:
            rows = tables[2].find_all("tr")
            puan_info = {}
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace("*", "")
                    value = cols[1].get_text(strip=True).replace("*", "")
                    puan_info[key] = value
            details["puan_info"] = puan_info

        return details


class GenelBilgilerLisansFetcher(GenelBilgilerBaseFetcher):
    """Lisans fetcher for general program information."""

    ENDPOINT = "1000_1.php"
    PROGRAM_TYPE = "lisans"


class GenelBilgilerOnlisansFetcher(GenelBilgilerBaseFetcher):
    """Onlisans fetcher for general program information."""

    ENDPOINT = "3000_1.php"
    PROGRAM_TYPE = "onlisans"
