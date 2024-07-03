import aiohttp
from bs4 import BeautifulSoup
import asyncio

async def fetch_degisim_programi_bilgileri(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}

    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/2040.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/2040.php?y={program_id}"
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
    
    # Check if the table exists
    table = soup.find('table', {'class': 'table table-bordered'})
    
    if table:
        # If the table exists, fetch the data
        rows = table.find_all('tr')
        data = []
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) == 3:
                data.append({
                    'program': cols[0].get_text(strip=True),
                    'giden': int(cols[1].get_text(strip=True)),
                    'gelen': int(cols[2].get_text(strip=True))
                })
        
        result = {
            "has_data": True,
            "degisim_programlari": data
        }
    else:
        # If the table does not exist, look for the info message
        info_div = soup.find('div', string=lambda text: 'Değişim Programı ile' in text if text else False)
        
        if info_div:
            message = info_div.get_text(strip=True)
            # Parse the message
            giden_gelen = message.split('Değişim Programı ile ')[1].split(' öğrenci')[0]
            result = {
                "message": message,
                "giden_gelen": giden_gelen,
                "has_data": False
            }
        else:
            result = {
                "message": "Değişim programı bilgisi bulunamadı veya sayfanın yapısı değişmiş olabilir.",
                "has_data": False
            }
