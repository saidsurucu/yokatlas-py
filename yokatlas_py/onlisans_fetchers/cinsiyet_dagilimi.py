import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union
from yokatlas_py.config import settings


async def fetch_cinsiyet_dagilimi(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing fetched data or error message
    """
    if year not in settings.supported_years:
        return {
            "error": f"Invalid year. Only {settings.supported_years} are supported."
        }

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = (
        f"/{year}/content/onlisans-dynamic/3010.php?y={program_id}"
        if year != 2024
        else f"/content/onlisans-dynamic/3010.php?y={program_id}"
    )
    url = f"{base_url}{url_suffix}"

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        if response.status_code != 200:
            return {"error": "Failed to fetch data from YOKATLAS"}

        html_content = response.text

    def parse_html_to_json(html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract structured data."""
        soup = BeautifulSoup(html_content.replace("---", "0"), "html.parser")
        table = soup.find("table", {"class": "table table-bordered"})
        details = {}

        if table:
            headers = [
                header.get_text(strip=True) for header in table.find_all("th")[1:]
            ]
            rows = table.find("tbody").find_all("tr")

            data = []
            for row in rows:
                cols = row.find_all("td")
                row_data = {}
                row_data["Type"] = cols[0].get_text(strip=True).replace("*", "")
                for i, header in enumerate(headers):
                    if i + 1 < len(cols):
                        row_data[header] = (
                            cols[i + 1].get_text(strip=True).replace("*", "")
                        )
                    else:
                        row_data[header] = None
                data.append(row_data)

            details["cinsiyet_dagilimi"] = data

        return details

    json_data = parse_html_to_json(html_content)
    return json_data
