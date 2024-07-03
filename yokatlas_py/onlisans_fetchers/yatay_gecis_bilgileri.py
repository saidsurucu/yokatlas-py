import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_yatay_gecis_bilgileri(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/onlisans-dynamic/2060.php?y={program_id}" if year != 2023 else f"/content/onlisans-dynamic/2060.php?y={program_id}"
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

    result = {
        "gelen_ogrenci": {},
        "giden_ogrenci": {}
    }

    for table in tables:
        header = table.find('th', colspan="3")
        if header:
            header_text = header.get_text(strip=True)
            key = "gelen_ogrenci" if "Gelen" in header_text else "giden_ogrenci" if "Giden" in header_text else None
            if key:
                rows = table.find_all('tr')
                if len(rows) > 2:  # Skip the first two header rows
                    cols = rows[2].find_all('td')  # Data row is the third row (index 2)
                    if len(cols) == 2:
                        result[key] = {
                            "2022": 0 if cols[0].get_text(strip=True) == "---" else int(cols[0].get_text(strip=True)),
                            "2023": 0 if cols[1].get_text(strip=True) == "---" else int(cols[1].get_text(strip=True))
                        }

    return result
