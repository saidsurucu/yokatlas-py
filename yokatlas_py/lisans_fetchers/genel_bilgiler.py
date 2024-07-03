import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_genel_bilgiler(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1000_1.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/1000_1.php?y={program_id}"
    url = f"{base_url}{url_suffix}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            if response.status != 200:
                return {"error": "Failed to fetch data from YOKATLAS"}

            html_content = await response.text()

    def parse_html_to_json(html_content):
        soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
        tables = soup.find_all('table', {'class': 'table table-bordered'})

        details = {}

        if len(tables) > 0:
            rows = tables[0].find_all('tr')
            program_info = {}
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace('*', '')
                    value = cols[1].get_text(strip=True).replace('*', '')
                    program_info[key] = value
            details['program_info'] = program_info
        
        if len(tables) > 1:
            rows = tables[1].find_all('tr')
            kontenjan_info = {}
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace('*', '')
                    value = cols[1].get_text(strip=True).replace('*', '')
                    kontenjan_info[key] = value
            details['kontenjan_info'] = kontenjan_info
        
        if len(tables) > 2:
            rows = tables[2].find_all('tr')
            puan_info = {}
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True).replace('*', '')
                    value = cols[1].get_text(strip=True).replace('*', '')
                    puan_info[key] = value
            details['puan_info'] = puan_info

        return details

    json_data = parse_html_to_json(html_content)
    return json_data
