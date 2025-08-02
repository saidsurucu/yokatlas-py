import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union
from yokatlas_py.config import settings


async def fetch_yerlesen_basari_siralari(program_id: str, year: int) -> dict[str, Any]:
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
        f"/{year}/content/lisans-dynamic/1230.php?y={program_id}"
        if year != 2024
        else f"/content/lisans-dynamic/1230.php?y={program_id}"
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
    tables = soup.find_all("table", {"class": "table table-bordered"})

    if len(tables) < 2:
        return {"error": "Required tables not found in the HTML content"}

    # Initialize result dictionary dynamically
    result = {"ortalama_basari_siralari": {}, "en_dusuk_basari_siralari": {}}

    for i, table in enumerate(tables):
        rows = table.find_all("tr")
        headers = [
            header.get_text(strip=True) for header in rows[0].find_all("th")
        ]  # Extract headers dynamically

        # Ensure the structure exists based on the headers
        if i == 0:  # First table (ortalama başarı sıraları)
            result["ortalama_basari_siralari"][headers[1]] = {}
            result["ortalama_basari_siralari"][headers[2]] = {}
        else:  # Second table (en düşük başarı sıraları)
            result["en_dusuk_basari_siralari"][headers[1]] = {}
            result["en_dusuk_basari_siralari"][headers[2]] = {}

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
                category = (
                    "ortalama_basari_siralari" if i == 0 else "en_dusuk_basari_siralari"
                )
                result[category][headers[1]][key] = value_012
                result[category][headers[2]][key] = value_012_006
    return result
