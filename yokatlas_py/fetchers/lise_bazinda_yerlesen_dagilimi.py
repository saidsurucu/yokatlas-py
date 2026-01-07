"""
Lise Bazinda Yerlesen Dagilimi (School-based Placement Distribution) Fetcher.

Table with totals parser for school-based placement data.
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class LiseBazindaYerlesenDagilimiBaseFetcher(BaseFetcher):
    """Base fetcher for school-based placement distribution."""

    RESULT_KEY = "lise_bazinda_yerlesen_dagilimi"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract school-based placement distribution."""
        soup = self.create_soup(html_content, clean=True)
        table = self.find_table(soup)

        if not table:
            return {"error": "Table not found in the HTML content"}

        headers = ["Lise", "Toplam", "Lise'den Yeni Mezun", "Önceki Mezun"]
        tbody = table.find("tbody")
        rows = tbody.find_all("tr") if tbody else table.find_all("tr")

        result = []
        toplam = {}

        for row in rows:
            cols = row.find_all(["td", "th"])
            if len(cols) != 4:  # We expect 4 columns
                continue

            row_data = {}
            for i, header in enumerate(headers):
                value = (
                    cols[i]
                    .get_text(strip=True)
                    .replace("---", "0")
                    .replace("%", "")
                    .replace(",", ".")
                )
                if i == 0:  # 'Lise' column
                    row_data[header] = value
                else:
                    try:
                        row_data[header] = int(value)
                    except ValueError:
                        row_data[header] = value

            if row_data.get("Lise", "").upper() == "TOPLAM":
                toplam = row_data
            else:
                result.append(row_data)

        return {"lise_bazinda_yerlesen": result, "toplam": toplam}


class LiseBazindaYerlesenDagilimiLisansFetcher(LiseBazindaYerlesenDagilimiBaseFetcher):
    """Lisans fetcher for school-based placement distribution."""

    ENDPOINT = "1060.php"
    PROGRAM_TYPE = "lisans"


class LiseBazindaYerlesenDagilimiOnlisansFetcher(LiseBazindaYerlesenDagilimiBaseFetcher):
    """Onlisans fetcher for school-based placement distribution."""

    ENDPOINT = "3060.php"
    PROGRAM_TYPE = "onlisans"
