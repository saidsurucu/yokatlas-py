import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union

async def fetch_kontenjan_yerlesme(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch kontenjan yerleşme data for a specific program and year.
    
    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2021-2024)
        
    Returns:
        Dictionary containing kontenjan yerleşme data or error message
    """
    if year not in [2021, 2022, 2023, 2024]:
        return {"error": "Invalid year. Only 2021, 2022, 2023 and 2024 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1000_2.php?y={program_id}" if year != 2024 else f"/content/lisans-dynamic/1000_2.php?y={program_id}"
    url = f"{base_url}{url_suffix}"

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            html_content = response.text
        except httpx.RequestError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

    def parse_html_to_json(html_content: str) -> dict[str, Any]:
        """Parse HTML content to extract kontenjan yerleşme data."""
        soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
        table = soup.find('table', {'class': 'table table-bordered'})
        details: dict[str, Any] = {}

        if table:
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            headers[0] = 'Tür'  # Change the first header to "Tür"
            rows = table.find('tbody').find_all('tr')
            
            data: list[dict[str, Optional[str]]] = []
            for row in rows:
                cols = row.find_all('td')
                row_data: Dict[str, Optional[str]] = {}
                for i, header in enumerate(headers):
                    row_data[header] = cols[i].get_text(strip=True).replace('*', '') if i < len(cols) else None
                data.append(row_data)
            
            details['kontenjan_yerlesme'] = data

        return details

    json_data = parse_html_to_json(html_content)
    return json_data
