import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_yerlesen_tercih_istatistikleri(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/onlisans-dynamic/3040.php?y={program_id}" if year != 2023 else f"/content/onlisans-dynamic/3040.php?y={program_id}"
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

    if len(tables) < 3:
        return {"error": "Required tables not found in the HTML content"}

    result = {
        'genel_istatistikler': {},
        'tercih_sira_dagilimi': []
    }

    # İlk tablo: Genel istatistikler
    rows = tables[0].find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            if len(cols) == 3:
                value = [value, cols[2].get_text(strip=True)]
            result['genel_istatistikler'][key] = value

    # İkinci ve üçüncü tablo: Tercih sıra dağılımı
    for table in tables[1:3]:
        headers = [header.get_text(strip=True) for header in table.find_all('th')]
        rows = table.find_all('tr')[1:]  # Skip the header row
        for row in rows:
            cols = row.find_all('td')
            row_data = {}
            for i, header in enumerate(headers):
                if i < len(cols):
                    value = cols[i].get_text(strip=True).replace('%', '').replace(',', '.')
                    try:
                        row_data[header] = int(value)
                    except ValueError:
                        row_data[header] = value
            if 'Tercih Sırası' in row_data and 'Yerleşen Sayısı' in row_data:
                result['tercih_sira_dagilimi'].append(row_data)

    return result
