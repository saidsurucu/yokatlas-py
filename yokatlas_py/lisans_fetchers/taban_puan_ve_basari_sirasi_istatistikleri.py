import aiohttp
from bs4 import BeautifulSoup, Comment
import asyncio

async def fetch_taban_puan_ve_basari_sirasi_istatistikleri(program_id, year):
    if year not in [2021, 2022, 2023]:
        return {"error": "Invalid year. Only 2021, 2022, and 2023 are supported."}
    
    base_url = "https://yokatlas.yok.gov.tr"
    url_suffix = f"/{year}/content/lisans-dynamic/1000_3.php?y={program_id}" if year != 2023 else f"/content/lisans-dynamic/1000_3.php?y={program_id}"
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
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        comments = soup.find_all(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            uncommented = BeautifulSoup(comment.string, 'html.parser')
            comment.insert_after(uncommented)
        
        tables = soup.find_all('table', {'class': 'table table-bordered'})
        
        if len(tables) < 2:
            return {"error": "Required tables not found in the HTML content"}
        
        result = {
            'son_kisi_puan_bilgileri': [],
            'son_kisi_basari_sirasi_bilgileri': []
        }
        
        def parse_table(table, table_name):
            headers = ['Kontenjan Türü', 'Kontenjan', 'Yerleşen Sayısı', '0,12 Katsayı ile', '0,12 + 0,06 Katsayı ile']
            
            data = []
            rows = table.find_all('tr')
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                
                if len(cols) >= 4:
                    entry = {}
                    for header, col in zip(headers, cols + [None] * (5 - len(cols))):
                        text = col.get_text(strip=True) if col else None
                        entry[header] = text if text and text != '---' else None
                    if entry['Kontenjan Türü'] and entry['Kontenjan Türü'] not in ['Kontenjan Türü', '', 'Kontenjan']:
                        if entry['Kontenjan Türü'] == 'YKS Kontenjanı':
                            entry['Kontenjan Türü'] = 'Genel Kontenjan'
                        if entry['Kontenjan Türü'] != 'Sınavsız Geçiş Kontenjanı':
                            data.append(entry)
            
            return data
        
        result['son_kisi_puan_bilgileri'] = parse_table(tables[0], "son_kisi_puan_bilgileri")
        result['son_kisi_basari_sirasi_bilgileri'] = parse_table(tables[1], "son_kisi_basari_sirasi_bilgileri")
        
        return result
    except Exception as e:
        return {"error": f"Failed to process HTML: {str(e)}"}