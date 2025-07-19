import httpx
from bs4 import BeautifulSoup
import asyncio
from typing import Any, Optional, Union

async def fetch_lise_grubu_ve_tipi_dagilimi(program_id: str, year: int) -> dict[str, Any]:
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
    url_suffix = f"/{year}/content/onlisans-dynamic/3050a.php?y={program_id}" if year != 2024 else f"/content/onlisans-dynamic/3050a.php?y={program_id}"
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
    
    if len(tables) < 1:
        return {"error": "Required table not found in the HTML content"}
    
    result = {
        'genel_liseler_grubu': [],
        'meslek_lisesi_grubu': []
    }
    
    for i, table in enumerate(tables[:2]):  # Process up to two tables if they exist
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) != 3:  # We expect 3 columns: Lise Tipi, Yerleşen, % Oran
                continue
            row_data = {}
            for j, header in enumerate(['Lise Tipi', 'Yerleşen', '% Oran']):
                value = cols[j].get_text(strip=True).replace('%', '').replace(',', '.')
                if header == 'Lise Tipi':
                    row_data[header] = value
                else:
                    try:
                        row_data[header] = float(value) if '.' in value else int(value)
                    except ValueError:
                        row_data[header] = value
            if i == 0:
                result['genel_liseler_grubu'].append(row_data)
            else:
                result['meslek_lisesi_grubu'].append(row_data)
    return result