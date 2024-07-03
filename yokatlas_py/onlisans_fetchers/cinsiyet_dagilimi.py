import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_cinsiyet_dagilimi(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}


    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/onlisans-dynamic/3010.php?y={program_id}" if year != 2023 else f"/content/onlisans-dynamic/3010.php?y={program_id}"
    url = f"{base_url}{url_suffix}"
 
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            if response.status != 200:
                return {"error": "Failed to fetch data from YOKATLAS"}

            html_content = await response.text()

    def parse_html_to_json(html_content):
        soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
        table = soup.find('table', {'class': 'table table-bordered'})
        details = {}

        if table:
            headers = [header.get_text(strip=True) for header in table.find_all('th')[1:]]
            rows = table.find('tbody').find_all('tr')
            
            data = []
            for row in rows:
                cols = row.find_all('td')
                row_data = {}
                row_data['Type'] = cols[0].get_text(strip=True).replace('*', '')
                for i, header in enumerate(headers):
                    if i + 1 < len(cols):
                        row_data[header] = cols[i + 1].get_text(strip=True).replace('*', '')
                    else:
                        row_data[header] = None
                data.append(row_data)
            
            details['cinsiyet_dagilimi'] = data

        return details

    json_data = parse_html_to_json(html_content)
    return json_data
