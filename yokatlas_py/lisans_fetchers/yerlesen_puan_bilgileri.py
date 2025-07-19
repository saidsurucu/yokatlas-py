import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union

async def fetch_yerlesen_puan_bilgileri(program_id: str, year: int) -> dict[str, Any]:
    """
    Fetch data for a specific program and year.
    
    Args:
        program_id: YÖK program kodu (9 digit string)
        year: Year (2021-2024)
        
    Returns:
        Dictionary containing fetched data or error message
    """
    if year not in [2021, 2022, 2023, 2024]:
        return {"error": "Invalid year. Only 2021, 2022, 2023 and 2024 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1220.php?y={program_id}" if year != 2024 else f"/content/lisans-dynamic/1220.php?y={program_id}"
    url = f"{base_url}{url_suffix}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            html_content = response.text
        except httpx.RequestError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

    soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
    tables = soup.find_all('table', {'class': 'table table-bordered'})

    if len(tables) < 2:
        return {"error": "Required tables not found in the HTML content"}

    # Initialize result dictionary dynamically
    result = {}
    table_headers = []

    for i, table in enumerate(tables):
        rows = table.find_all('tr')
        headers = [header.get_text(strip=True) for header in rows[0].find_all('th')]
        
        # Ensure the structure exists based on the headers
        if i == 0:  # First table (ortalama puanlar)
            table_headers = headers
            result['ortalama_puanlar'] = {headers[1]: {}, headers[2]: {}}
        else:  # Second table (en düşük puanlar)
            result['en_dusuk_puanlar'] = {headers[1]: {}, headers[2]: {}}

        for row in rows[1:]:  # Skip the first header row
            cols = row.find_all('td')
            if len(cols) == 3:
                key = cols[0].get_text(strip=True)
                for j, header in enumerate(headers[1:], start=1):
                    value = cols[j].get_text(strip=True).replace(',', '.')
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                    if i == 0:
                        result['ortalama_puanlar'][header][key] = value
                    else:
                        result['en_dusuk_puanlar'][header][key] = value
    return result
