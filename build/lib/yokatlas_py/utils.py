import json
from bs4 import BeautifulSoup
from urllib.parse import parse_qsl

def load_column_data():
    with open("columnData.json", "r") as file:
        column_data = json.load(file)
        if isinstance(column_data, list) and len(column_data) > 0:
            return dict(parse_qsl(column_data[0]))
    return {}

def extract_text_from_html(html):
    if not html:
        return None
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text(strip=True)

def parse_onlisans_results(data):
    results = []
    for item in data.get('data', []):
        result = parse_onlisans_item(item)
        results.append(result)
    return results

def parse_onlisans_item(item):
    def get_value(index, split_index=None, color=None):
        try:
            value = item[index]
            soup = BeautifulSoup(value, 'html.parser')
            if split_index is not None:
                parts = value.split('<br>')
                if split_index < len(parts):
                    soup = BeautifulSoup(parts[split_index], 'html.parser')
            if color:
                element = soup.find('font', color=color)
                return element.get_text(strip=True) if element else None
            return soup.get_text(strip=True)
        except (IndexError, KeyError):
            return None

    def clean_text(text):
        if text:
            return text.replace('Listeme Ekle', '').strip()
        return text

    def format_tbs(value):
        return value.replace('.', '') if value else None

    def format_taban(value):
        return value.replace(',', '.') if value else None

    return {
        "yop_kodu": clean_text(get_value(1)),
        "uni_adi": clean_text(get_value(2)),
        "fakulte": clean_text(get_value(3)),
        "program_adi": clean_text(get_value(4)),
        "program_detay": clean_text(get_value(5)),
        "sehir_adi": clean_text(get_value(6)),
        "universite_turu": clean_text(get_value(7)),
        "ucret_burs": clean_text(get_value(8)),
        "ogretim_turu": clean_text(get_value(9)),
        "kontenjan": {
            "2023": get_value(10, color='red'),
            "2022": get_value(10, color='blue')
        },
        "yerlesen": {
            "2023": get_value(16, color='red'),
            "2022": get_value(16, color='blue')
        },
        "taban": {
            "2023": format_taban(get_value(21, color='red')),
            "2022": format_taban(get_value(21, color='blue'))
        },
        "tbs": {
            "2023": format_tbs(get_value(22, color='red')),
            "2022": format_tbs(get_value(22, color='blue'))
        }
    }

def parse_lisans_results(data):
    results = []
    for item in data.get('data', []):
        result = parse_lisans_item(item)
        results.append(result)
    return results

def parse_lisans_item(item):
    def safe_extract(index, sub_index=None, color=None):
        try:
            if sub_index is not None:
                content = item[index].split('<br>')[sub_index]
            else:
                content = item[index]
            
            if color:
                soup = BeautifulSoup(content, 'html.parser')
                element = soup.find('font', color=color)
                return element.text.strip() if element else None
            else:
                return extract_text_from_html(content)
        except (IndexError, AttributeError):
            return None

    def safe_replace(value, old, new):
        return value.replace(old, new) if value else None

    return {
        "yop_kodu": safe_extract(1, 0),
        "uni_adi": safe_extract(2, 0),
        "fakulte": safe_extract(2, 1, '#CC0000'),
        "program_adi": safe_extract(4, 0),
        "program_detay": safe_extract(4, 1, '#CC0000'),
        "sehir_adi": safe_extract(6) if len(item) > 6 else None,
        "universite_turu": safe_extract(7) if len(item) > 7 else None,
        "ucret_burs": safe_extract(8) if len(item) > 8 else None,
        "ogretim_turu": safe_extract(9) if len(item) > 9 else None,
        "kontenjan": {
            "2023": safe_extract(10, 1, 'red'),
            "2022": safe_extract(10, 2, 'purple'),
            "2021": safe_extract(10, 3, 'blue'),
            "2020": safe_extract(10, 4, 'green')
        },
        "yerlesen": {
            "2023": safe_extract(15, 1, 'red'),
            "2022": safe_extract(15, 2, 'purple'),
            "2021": safe_extract(15, 3, 'blue'),
            "2020": safe_extract(15, 4, 'green')
        },
        "tbs": {
            "2023": safe_replace(safe_extract(19, 1, 'red'), '.', ''),
            "2022": safe_replace(safe_extract(19, 2, 'purple'), '.', ''),
            "2021": safe_replace(safe_extract(19, 3, 'blue'), '.', ''),
            "2020": safe_replace(safe_extract(19, 4, 'green'), '.', '')
        },
        "taban": {
            "2023": safe_replace(safe_extract(27, 1, 'red'), ',', '.'),
            "2022": safe_replace(safe_extract(27, 2, 'purple'), ',', '.'),
            "2021": safe_replace(safe_extract(27, 3, 'blue'), ',', '.'),
            "2020": safe_replace(safe_extract(27, 4, 'green'), ',', '.')
        }
    }
