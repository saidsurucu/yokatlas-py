import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_yerlesen_il_dagilimi(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1020c.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/1020c.php?y={program_id}"
    url = f"{base_url}{url_suffix}"

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, ssl=False) as response:
                response.raise_for_status()
                html_content = await response.text()
        except aiohttp.ClientError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

    soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
    tables = soup.find_all('table', {'class': 'table table-bordered'})

    if not tables:
        return {"error": "No tables found in the HTML content"}

    table = tables[0]
    headers = [header.get_text(strip=True) for header in table.find_all('th')]
    headers[0] = 'İl'  
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')

    result = []
    toplam = {}

    for row in rows:
        cols = row.find_all('td')
        row_data = {}
        for i, header in enumerate(headers):
            if i < len(cols):
                value = cols[i].get_text(strip=True).replace('%', '').replace(',', '.')
                try:
                    row_data[header] = float(value) if '.' in value else int(value)
                except ValueError:
                    row_data[header] = value

        if row_data.get(headers[0]) == 'Toplam':
            toplam = row_data
        else:
            result.append(row_data)

    return {
        'il_dagilimi': result,
        'toplam': toplam
    }
