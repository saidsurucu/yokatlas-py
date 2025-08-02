import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Dict, Any, List, Optional
from yokatlas_py.config import settings


async def fetch_sehir_ve_cografi_bolge_dagilimi(
    program_id: str, year: int
) -> dict[str, Any]:
    """
    Fetch şehir ve coğrafi bölge dağılımı data for a specific program and year.

    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2022-2025)

    Returns:
        Dictionary containing şehir ve coğrafi bölge dağılımı data or error message
    """
    if year not in settings.supported_years:
        return {
            "error": f"Invalid year. Only {settings.supported_years} are supported."
        }

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = (
        f"/{year}/content/lisans-dynamic/1020ab.php?y={program_id}"
        if year != 2024
        else f"/content/lisans-dynamic/1020ab.php?y={program_id}"
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
            return parse_html_to_json(html_content)
        except httpx.RequestError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}


def parse_html_to_json(html_content: str) -> Dict[str, List[Dict[str, str]]]:
    """Parse HTML content to extract şehir ve coğrafi bölge dağılımı data."""
    soup = BeautifulSoup(html_content.replace("---", "0"), "html.parser")
    tables = soup.find_all("table", {"class": "table table-bordered"})

    result: dict[str, list[dict[str, str]]] = {
        "sehir_dagilimi": [],
        "cografi_bolge_dagilimi": [],
    }

    if len(tables) > 0:
        # Parse yerlesme dagilimi
        headers = [header.get_text(strip=True) for header in tables[0].find_all("th")]
        headers[0] = "Tür"  # Change the first header to "Tür"
        rows = tables[0].find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            row_data = {}
            for i, header in enumerate(headers):
                row_data[header] = cols[i].get_text(strip=True).replace("*", "")
            result["sehir_dagilimi"].append(row_data)

    if len(tables) > 1:
        # Parse cografi bolge dagilimi
        headers = [header.get_text(strip=True) for header in tables[1].find_all("th")]
        headers[0] = "Bölge"
        rows = tables[1].find("tbody").find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            row_data = {}
            for i, header in enumerate(headers):
                row_data[header] = cols[i].get_text(strip=True).replace("*", "")
            result["cografi_bolge_dagilimi"].append(row_data)

    return result
