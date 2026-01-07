"""
Tercih Edilen Universiteler (Preferred Universities) Fetcher.

Multi-table parser for preferred universities (devlet/vakif).
"""

from typing import Any

from ..base_fetcher import BaseFetcher


class TercihEdilenUniversitelerBaseFetcher(BaseFetcher):
    """Base fetcher for preferred universities."""

    RESULT_KEY = "tercih_edilen_universiteler"

    def parse(self, html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract preferred universities."""
        soup = self.create_soup(html_content, clean=True)
        tables = soup.find_all("table", {"class": "table table-bordered"})

        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}

        result: dict[str, Any] = {"devlet": [], "vakif": []}

        for i, table in enumerate(tables[:2]):
            rows = table.find_all("tr")
            for row in rows[2:]:  # Skip the first two header rows
                cols = row.find_all("td")
                if len(cols) == 2:
                    university = cols[0].get_text(strip=True)
                    try:
                        preference_count = int(cols[1].get_text(strip=True))
                    except ValueError:
                        preference_count = 0

                    if i == 0:
                        result["devlet"].append(
                            {"universite": university, "tercih_sayisi": preference_count}
                        )
                    else:
                        result["vakif"].append(
                            {"universite": university, "tercih_sayisi": preference_count}
                        )

        return result


class TercihEdilenUniversitelerLisansFetcher(TercihEdilenUniversitelerBaseFetcher):
    """Lisans fetcher for preferred universities."""

    ENDPOINT = "1320.php"
    PROGRAM_TYPE = "lisans"


class TercihEdilenUniversitelerOnlisansFetcher(TercihEdilenUniversitelerBaseFetcher):
    """Onlisans fetcher for preferred universities."""

    ENDPOINT = "3320b.php"
    PROGRAM_TYPE = "onlisans"
