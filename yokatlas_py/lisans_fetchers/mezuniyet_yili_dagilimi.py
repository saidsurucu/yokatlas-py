import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union
from yokatlas_py.config import settings


async def fetch_mezuniyet_yili_dagilimi(program_id: str, year: int) -> dict[str, Any]:
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
        f"/{year}/content/lisans-dynamic/1030b.php?y={program_id}"
        if year != 2024
        else f"/content/lisans-dynamic/1030b.php?y={program_id}"
    )
    url = f"{base_url}{url_suffix}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text
        except httpx.RequestError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

    soup = BeautifulSoup(html_content.replace("---", "0"), "html.parser")
    table = soup.find("table", {"class": "table table-bordered"})

    if not table:
        return {"error": "Table not found in the HTML content"}

    headers = [header.get_text(strip=True) for header in table.find_all("th")]
    rows = table.find("tbody").find_all("tr")

    result = []
    toplam = {}

    for row in rows:
        cols = row.find_all("td")
        row_data = {}
        for i, header in enumerate(headers):
            if i == 0:  # Mezuniyet Yılı
                row_data["Mezuniyet Yılı"] = cols[i].get_text(strip=True)
            elif i < len(cols):
                value = cols[i].get_text(strip=True).replace("%", "").replace(",", ".")
                try:
                    row_data[header] = float(value) if "." in value else int(value)
                except ValueError:
                    row_data[header] = value
        if row_data["Mezuniyet Yılı"] == "Toplam":
            toplam = row_data
        else:
            result.append(row_data)
    return {"mezuniyet_yili_dagilimi": result, "toplam": toplam}
