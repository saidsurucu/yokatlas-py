"""
Sehir ve Cografi Bolge Dagilimi (City and Geographic Region Distribution) Fetcher.

Multi-table parser for city and geographic region distribution.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class SehirVeCografiBolgeDagilimiBaseFetcher(BaseFetcher):
    """Base fetcher for city and geographic region distribution."""

    RESULT_KEY = "sehir_ve_cografi_bolge_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract city and region distribution."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        result: dict[str, Any] = {
            "sehir_dagilimi": [],
            "cografi_bolge_dagilimi": [],
        }

        if len(tables) > 0:
            # Parse city distribution
            headers = [header.get_text(strip=True) for header in tables[0].find_all("th")]
            if headers:
                headers[0] = "Tür"  # Change the first header to "Tür"
            tbody = tables[0].find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    row_data = {}
                    for i, header in enumerate(headers):
                        if i < len(cols):
                            row_data[header] = cols[i].get_text(strip=True).replace("*", "")
                    result["sehir_dagilimi"].append(row_data)

        if len(tables) > 1:
            # Parse geographic region distribution
            headers = [header.get_text(strip=True) for header in tables[1].find_all("th")]
            if headers:
                headers[0] = "Bölge"
            tbody = tables[1].find("tbody")
            if tbody:
                rows = tbody.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    row_data = {}
                    for i, header in enumerate(headers):
                        if i < len(cols):
                            row_data[header] = cols[i].get_text(strip=True).replace("*", "")
                    result["cografi_bolge_dagilimi"].append(row_data)

        return result


class SehirVeCografiBolgeDagilimiLisansFetcher(SehirVeCografiBolgeDagilimiBaseFetcher):
    """Lisans fetcher for city and geographic region distribution."""

    ENDPOINT = "1020ab.php"
    PROGRAM_TYPE = "lisans"


class SehirVeCografiBolgeDagilimiOnlisansFetcher(SehirVeCografiBolgeDagilimiBaseFetcher):
    """Onlisans fetcher for city and geographic region distribution."""

    ENDPOINT = "3020ab.php"
    PROGRAM_TYPE = "onlisans"
