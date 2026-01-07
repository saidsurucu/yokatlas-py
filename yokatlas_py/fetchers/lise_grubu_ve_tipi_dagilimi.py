"""
Lise Grubu ve Tipi Dagilimi (High School Group and Type Distribution) Fetcher.

Multi-table parser for high school type distribution.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class LiseGrubuVeTipiDagilimiBaseFetcher(BaseFetcher):
    """Base fetcher for high school group and type distribution."""

    RESULT_KEY = "lise_grubu_ve_tipi_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract high school type distribution."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 1:
            return {"error": "Required table not found in the HTML content"}

        result: dict[str, Any] = {"genel_liseler_grubu": [], "meslek_lisesi_grubu": []}

        for i, table in enumerate(tables[:2]):  # Process up to two tables
            tbody = table.find("tbody")
            if not tbody:
                continue
            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) != 3:  # We expect 3 columns: Lise Tipi, Yerleşen, % Oran
                    continue
                row_data = {}
                for j, header in enumerate(["Lise Tipi", "Yerleşen", "% Oran"]):
                    value = cols[j].get_text(strip=True).replace("%", "").replace(",", ".")
                    if header == "Lise Tipi":
                        row_data[header] = value
                    else:
                        try:
                            row_data[header] = float(value) if "." in value else int(value)
                        except ValueError:
                            row_data[header] = value
                if i == 0:
                    result["genel_liseler_grubu"].append(row_data)
                else:
                    result["meslek_lisesi_grubu"].append(row_data)

        return result


class LiseGrubuVeTipiDagilimiLisansFetcher(LiseGrubuVeTipiDagilimiBaseFetcher):
    """Lisans fetcher for high school group and type distribution."""

    ENDPOINT = "1050a.php"
    PROGRAM_TYPE = "lisans"


class LiseGrubuVeTipiDagilimiOnlisansFetcher(LiseGrubuVeTipiDagilimiBaseFetcher):
    """Onlisans fetcher for high school group and type distribution."""

    ENDPOINT = "3050a.php"
    PROGRAM_TYPE = "onlisans"
