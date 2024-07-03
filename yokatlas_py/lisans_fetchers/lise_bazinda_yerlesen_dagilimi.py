import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_lise_bazinda_yerlesen_dagilimi(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1060.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/1060.php?y={program_id}"
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
    table = soup.find('table', {'class': 'table table-bordered'})

    if not table:
        return {"error": "Table not found in the HTML content"}

    headers = ['Lise', 'Toplam', "Lise'den Yeni Mezun", 'Önceki Mezun']
    rows = table.find('tbody').find_all('tr') if table.find('tbody') else table.find_all('tr')

    result = []
    toplam = {}

    for row in rows:
        cols = row.find_all(['td', 'th'])
        if len(cols) != 4:  # We expect 4 columns
            continue

        row_data = {}
        for i, header in enumerate(headers):
            value = cols[i].get_text(strip=True).replace('---', '0').replace('%', '').replace(',', '.')
            if i == 0:  # 'Lise' column
                row_data[header] = value
            else:
                try:
                    row_data[header] = int(value)
                except ValueError:
                    row_data[header] = value

        if row_data['Lise'] == 'Toplam':
            toplam = row_data
        else:
            result.append(row_data)

    return {
        'lise_bazinda_yerlesen': result,
        'toplam': toplam
    }
