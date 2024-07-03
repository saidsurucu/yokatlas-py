import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_kontenjan_yerlesme(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/onlisans-dynamic/3000_2.php?y={program_id}" if year != 2023 else f"/content/onlisans-dynamic/3000_2.php?y={program_id}"
    url = f"{base_url}{url_suffix}"

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as response:
                if response.status != 200:
                    return {"error": "Failed to fetch data from YOKATLAS"}

                html_content = await response.text()
        except aiohttp.ClientError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

    def parse_html_to_json(html_content):
        soup = BeautifulSoup(html_content.replace('---','0'), 'html.parser')
        table = soup.find('table', {'class': 'table table-bordered'})
        details = {}

        if table:
            headers = [header.get_text(strip=True) for header in table.find_all('th')]
            headers[0] = 'Tür'  # Change the first header to "Tür"
            rows = table.find('tbody').find_all('tr')
            
            data = []
            for row in rows:
                cols = row.find_all('td')
                row_data = {}
                for i, header in enumerate(headers):
                    row_data[header] = cols[i].get_text(strip=True).replace('*', '') if i < len(cols) else None
                data.append(row_data)
            
            details['kontenjan_yerlesme'] = data

        return details

    json_data = parse_html_to_json(html_content)
    return json_data
