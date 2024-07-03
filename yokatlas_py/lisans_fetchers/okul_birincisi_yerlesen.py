import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_okul_birincisi_yerlesen(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1030c.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/1030c.php?y={program_id}"
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

    if len(tables) < 2:
        return {"error": "Required tables not found in the HTML content"}

    # First table: Yerleşen sayıları
    yerlesen_sayilari = {}
    rows = tables[0].find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            yerlesen_sayilari[key] = int(value) if value.isdigit() else 0

    # Second table: Okul birincisi detayları
    okul_birincisi_detay = []
    rows = tables[1].find_all('tr')
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) == 2:
            okul_birincisi_detay.append({
                'Kontenjan Türü': cols[0].get_text(strip=True),
                'Geldiği Lise': cols[1].get_text(strip=True)
            })

    return {
        'yerlesen_sayilari': yerlesen_sayilari,
        'okul_birincisi_detay': okul_birincisi_detay
    }
