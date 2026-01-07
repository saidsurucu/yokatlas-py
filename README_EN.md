# YOKATLAS-py

A modern, type-safe Python wrapper for YOKATLAS API with async support.

[![PyPI version](https://badge.fury.io/py/yokatlas-py.svg)](https://badge.fury.io/py/yokatlas-py)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/yokatlas-py)](https://pepy.tech/project/yokatlas-py)

> **[Türkçe Versiyon](README.md)**

---

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Supported Data](#supported-data)
- [Search API](#search-api)
- [Atlas API](#atlas-api)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Installation

**Requirements:** Python 3.9+

```bash
# With pip
pip install yokatlas-py

# With uv (recommended)
uv add yokatlas-py
```

---

## Quick Start

```python
from yokatlas_py import search_lisans_programs, YOKATLASLisansAtlasi
import asyncio

# 1. Search for programs (sync)
results = search_lisans_programs({
    "uni_adi": "boğaziçi",       # Fuzzy matching!
    "program_adi": "bilgisayar"
})
print(f"Found {len(results)} programs")

# 2. Get detailed program data (async)
async def get_details():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    return await atlas.fetch_all_details()

details = asyncio.run(get_details())
print(details['genel_bilgiler'])
```

---

## Supported Data

### Supported Years

| Program Type | Years |
|--------------|-------|
| Lisans (Bachelor's) | 2021, 2022, 2023, 2024 |
| Önlisans (Associate) | 2023, 2024 |

### Lisans Data Types (12)

| Key | Description |
|-----|-------------|
| `genel_bilgiler` | General info, quotas, score info |
| `cinsiyet_dagilimi` | Gender distribution |
| `cografi_bolge_dagilimi` | Geographic region distribution |
| `lise_grubu_dagilimi` | High school group distribution |
| `lise_bazinda_yerlesen` | Placement by high school |
| `tercih_istatistikleri` | Preference statistics |
| `tercih_edilen_programlar` | Preferred other programs |
| `tercih_edilen_universiteler` | Preferred universities |
| `tercih_edilen_program_turleri` | Preferred program types |
| `tercih_edilen_universite_turleri` | Preferred university types |
| `taban_puan_basari_sirasi` | Base score and ranking statistics |
| `yerlesen_puan_bilgileri` | Placed student score info |

### Önlisans Data Types (10)

Same as Lisans, except `yerlesen_basari_siralari` and `yerlesen_puan_bilgileri` are Lisans-only.

---

## Search API

### Smart Search (Fuzzy Matching)

```python
from yokatlas_py import search_lisans_programs, search_onlisans_programs, search_programs

# Fuzzy university matching - all find "BOĞAZİÇİ ÜNİVERSİTESİ"
search_lisans_programs({"uni_adi": "boğaziçi"})
search_lisans_programs({"uni_adi": "bogazici"})  # Without Turkish chars
search_lisans_programs({"uni_adi": "boun"})      # Abbreviation

# Supported abbreviations:
# "odtü", "odtu", "metu" → ORTA DOĞU TEKNİK ÜNİVERSİTESİ
# "itü", "itu" → İSTANBUL TEKNİK ÜNİVERSİTESİ
# "hacettepe" → HACETTEPE ÜNİVERSİTESİ

# Partial program name matching
results = search_lisans_programs({"program_adi": "bilgisayar"})
# Finds: Bilgisayar Mühendisliği, Bilgisayar Bilimleri, etc.

# Search both lisans and önlisans
all_results = search_programs({"uni_adi": "anadolu"})
print(f"Lisans: {len(all_results['lisans'])}")
print(f"Önlisans: {len(all_results['onlisans'])}")
```

### Traditional Search

```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi, YOKATLASOnlisansTercihSihirbazi

# Lisans search
lisans_search = YOKATLASLisansTercihSihirbazi({
    'puan_turu': 'say',          # say, ea, söz, dil
    'sehir': 'ANKARA',
    'universite_turu': 'Devlet',
    'ust_bs': 50000,             # Max ranking
    'length': 10
})
results = lisans_search.search()

# Önlisans search
onlisans_search = YOKATLASOnlisansTercihSihirbazi({
    'puan_turu': 'tyt',
    'sehir': 'İSTANBUL',
    'length': 10
})
results = onlisans_search.search()
```

---

## Atlas API

### Get All Program Details

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi

async def fetch_program_data():
    # Lisans
    lisans = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    data = await lisans.fetch_all_details()
    return data

result = asyncio.run(fetch_program_data())
```

### Example Output

```python
# result['genel_bilgiler']
{
  "program_info": {
    "ÖSYM Program Kodu": "103910743",
    "Üniversite Türü": "Devlet",
    "Üniversite": "FIRAT ÜNİVERSİTESİ",
    "Fakülte / Yüksekokul": "Teknoloji Fakültesi",
    "Puan Türü": "SAY",
    "Burs Türü": "Ücretsiz"
  },
  "kontenjan_info": {
    "Genel Kontenjan": "53",
    "Toplam Yerleşen": "60",
    "Boş Kalan Kontenjan": "0",
    "İlk Yerleşme Oranı": "100"
  },
  "puan_info": {
    "0,12 Katsayı ile Yerleşen Son Kişinin Puanı": "329,82598",
    "0,12 Katsayı ile Yerleşen Son Kişinin Başarı Sırası": "218.206"
  }
}
```

### Fetch Specific Data Only

```python
async def fetch_specific():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024,
        'keys': ['genel_bilgiler', 'cinsiyet_dagilimi']  # Only these
    })
    return await atlas.fetch_all_details()
```

---

## Error Handling

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

async def safe_fetch():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '999999999',  # Invalid ID
        'year': 2024
    })
    result = await atlas.fetch_all_details()

    # Check for errors in each data type
    for key, value in result.items():
        if isinstance(value, dict) and 'error' in value:
            print(f"❌ {key}: {value['error']}")
        else:
            print(f"✅ {key}: OK")

asyncio.run(safe_fetch())
```

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `HTTP 418` | Rate limiting | Wait and retry |
| `HTTP 404` | Invalid program ID or year | Verify program_id exists |
| `Required tables not found` | No data for this program | Normal - some programs lack certain data |

---

## Rate Limiting

YOKATLAS API has rate limits. Recommendations:

- Add delays between requests: `await asyncio.sleep(0.5)`
- Use connection pooling (automatic with `YOKATLASClient`)
- Cache results when possible
- Avoid parallel requests to the same endpoint

```python
import asyncio

async def fetch_multiple_programs(program_ids):
    results = {}
    for pid in program_ids:
        atlas = YOKATLASLisansAtlasi({'program_id': pid, 'year': 2024})
        results[pid] = await atlas.fetch_all_details()
        await asyncio.sleep(0.5)  # Rate limit delay
    return results
```

---

## Testing

```bash
# Run unit tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=yokatlas_py

# Run real API test (requires internet)
uv run python -c "
from yokatlas_py import search_lisans_programs
results = search_lisans_programs({'uni_adi': 'boğaziçi', 'length': 3})
print(f'Found {len(results)} programs')
"
```

---

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `uv run pytest tests/`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Links

- [PyPI Package](https://pypi.org/project/yokatlas-py/)
- [YOKATLAS Official](https://yokatlas.yok.gov.tr/)
- [Issue Tracker](https://github.com/your-username/yokatlas-py/issues)
