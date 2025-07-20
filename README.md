
# YOKATLAS-py

A modern, type-safe Python wrapper for YOKATLAS API with pydantic validation.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Type Hints](https://img.shields.io/badge/type%20hints-yes-brightgreen.svg)](https://docs.python.org/3/library/typing.html)
[![Pydantic](https://img.shields.io/badge/pydantic-2.11+-orange.svg)](https://pydantic.dev)


## Installation | Kurulum

**Requirements | Gereksinimler:** Python 3.9+

You can install the package using pip:

Paketi pip kullanarak yükleyebilirsiniz:

```sh
pip install yokatlas-py
```

Or with uv (recommended):

Ya da uv ile (önerilen):

```sh
uv add yokatlas-py
```

## Features | Özellikler

✅ **Type Safe**: Full type hints and pydantic validation  
✅ **Modern Python**: Requires Python 3.9+ with modern syntax  
✅ **Fast HTTP**: Uses httpx for both sync and async operations  
✅ **Validation**: Runtime validation of all API responses  
✅ **IDE Support**: Enhanced autocomplete and error detection  
✅ **Smart Search**: Fuzzy university matching and flexible program name search  
✅ **Complete Data**: All 235 lisans + 176 önlisans universities with 450+ programs  

## How to | Kullanım

### Quick Start with Smart Search | Akıllı Arama ile Hızlı Başlangıç

```python
from yokatlas_py import search_lisans_programs, search_onlisans_programs

# 🎯 Smart fuzzy search - works with partial names and abbreviations
# Akıllı bulanık arama - kısmi isimler ve kısaltmalarla çalışır

# Search for bachelor's programs with fuzzy matching
results = search_lisans_programs({
    "uni_adi": "boğaziçi",      # Finds "BOĞAZİÇİ ÜNİVERSİTESİ"
    "program_adi": "bilgisayar", # Finds all computer-related programs
    "sehir": "istanbul"          # Case-insensitive city matching
})

print(f"📚 Found {len(results)} lisans programs:")
for program in results[:3]:
    print(f"🎓 {program['uni_adi']}")
    print(f"💻 {program['program_adi']}")
    print(f"📍 {program['sehir_adi']}")
    print("---")

# Search for associate programs with abbreviations
onlisans_results = search_onlisans_programs({
    "uni_adi": "anadolu",        # Finds "ANADOLU ÜNİVERSİTESİ"
    "program_adi": "turizm"      # Finds all tourism-related programs
})

print(f"🏫 Found {len(onlisans_results)} önlisans programs:")
for program in onlisans_results[:2]:
    print(f"🎓 {program['uni_adi']}")
    print(f"🏖️ {program['program_adi']}")
    print("---")
```

### Type-Safe Search | Tip Güvenli Arama

```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi
from yokatlas_py.models import SearchParams, ProgramInfo
from pydantic import ValidationError

# Type-safe parameter validation
params = SearchParams(
    puan_turu="say",
    length=10,
    sehir="İstanbul",
    universite_turu="Devlet"
)

# Perform search with validated parameters
search = YOKATLASLisansTercihSihirbazi(params.model_dump(exclude_none=True))
results = search.search()

# Process results with validation
for result in results[:3]:
    try:
        program = ProgramInfo(**result)
        print(f"🎓 {program.uni_adi}")
        print(f"📚 {program.program_adi}")
        print(f"🏛️ {program.fakulte}")
        print(f"📍 {program.sehir_adi}")
        print("---")
    except ValidationError as e:
        print(f"⚠️ Invalid data: {e}")
```

### Traditional Usage | Geleneksel Kullanım

```python
from yokatlas_py import (
    YOKATLASLisansAtlasi,
    YOKATLASLisansTercihSihirbazi,
    YOKATLASOnlisansAtlasi,
    YOKATLASOnlisansTercihSihirbazi
)

# Atlas classes use async methods
async def example_atlas_usage():
    # Lisans (Bachelor's) program details
    lisans_atlasi = YOKATLASLisansAtlasi({'program_id': '104111719', 'year': 2024})
    lisans_result = await lisans_atlasi.fetch_all_details()
    print("YOKATLAS Lisans Atlas Result:", lisans_result)
    
    # Önlisans (Associate) program details  
    onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': '203550463', 'year': 2024})
    onlisans_result = await onlisans_atlasi.fetch_all_details()
    print("YOKATLAS Önlisans Atlas Result:", onlisans_result)

# Search classes use sync methods
def example_search_usage():
    # Search for bachelor's programs
    lisans_params = {
        'puan_turu': 'say',          # Score type: say, ea, söz, dil
        'sehir': 'ANKARA',           # Filter by city
        'universite_turu': 'Devlet', # State universities only
        'length': 5                  # Results per page
    }
    lisans_search = YOKATLASLisansTercihSihirbazi(lisans_params)
    lisans_results = lisans_search.search()
    print("Lisans Search Results:", lisans_results)
    
    # Search for associate programs
    onlisans_params = {
        'puan_turu': 'tyt',         # Score type for associate degrees
        'sehir': 'İSTANBUL',        # City filter
        'universite_turu': 'Devlet', # State universities
        'length': 10                # Results per page
    }
    onlisans_search = YOKATLASOnlisansTercihSihirbazi(onlisans_params)
    onlisans_results = onlisans_search.search()
    print("Önlisans Search Results:", onlisans_results)

# Run examples
example_search_usage()

# For async atlas usage, use asyncio in your environment:
# import asyncio
# asyncio.run(example_atlas_usage())
```

## Pydantic Models | Pydantic Modelleri

The library includes comprehensive pydantic models for type safety and validation:

Kütüphane tip güvenliği ve doğrulama için kapsamlı pydantic modelleri içerir:

### Available Models | Mevcut Modeller

- **SearchParams**: Search parameter validation
- **ProgramInfo**: University program information  
- **YearlyData**: Year-based statistical data
- **ErrorResponse**: Error handling and reporting

### Example with Validation | Doğrulama ile Örnek

```python
from yokatlas_py.models import SearchParams, ProgramInfo
from pydantic import ValidationError

# Invalid search parameters will be caught
try:
    params = SearchParams(
        puan_turu="invalid_type",  # Invalid score type
        length=-5  # Invalid length
    )
except ValidationError as e:
    print(f"Validation error: {e}")

# Valid parameters pass validation
params = SearchParams(
    puan_turu="say",
    sehir="İstanbul", 
    length=10
)
```

## Smart Search Features | Akıllı Arama Özellikleri

### Fuzzy University Matching | Bulanık Üniversite Eşleştirme

The library automatically matches partial and abbreviated university names:

```python
from yokatlas_py import search_lisans_programs

# All of these work and find "BOĞAZİÇİ ÜNİVERSİTESİ"
search_lisans_programs({"uni_adi": "boğaziçi"})
search_lisans_programs({"uni_adi": "bogazici"})  # Without Turkish chars
search_lisans_programs({"uni_adi": "boun"})      # Common abbreviation

# Common university abbreviations supported:
# "odtu"/"metu" → "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"
# "itu" → "İSTANBUL TEKNİK ÜNİVERSİTESİ" 
# "hacettepe" → "HACETTEPE ÜNİVERSİTESİ"
```

### Flexible Program Matching | Esnek Program Eşleştirme

Partial program names automatically find all related programs:

```python
# "bilgisayar" finds all computer-related programs:
# - "Bilgisayar Mühendisliği"
# - "Bilgisayar Bilimleri" 
# - "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği"

results = search_lisans_programs({"program_adi": "bilgisayar"})

# "mühendislik" finds all engineering programs
engineering_programs = search_lisans_programs({"program_adi": "mühendislik"})
```

### Universal Search | Evrensel Arama

Search both lisans and önlisans programs simultaneously:

```python
from yokatlas_py import search_programs

# Search both program types at once
all_results = search_programs({
    "uni_adi": "anadolu",
    "program_adi": "bilgisayar"
})

print(f"Lisans programs: {len(all_results['lisans'])}")
print(f"Önlisans programs: {len(all_results['onlisans'])}")
```

## Migration from v0.3.x | v0.3.x'den Geçiş

### New Features in v0.4.2+ | v0.4.2+'daki Yeni Özellikler

- **Smart Search**: Use `search_lisans_programs()` and `search_onlisans_programs()` for better search experience
- **Fuzzy Matching**: University and program names are matched intelligently
- **Complete Data**: All Turkish universities and programs included

### Migration Steps | Geçiş Adımları

1. **Update the package**
   ```bash
   pip install --upgrade yokatlas-py
   ```

2. **Use new smart search functions (recommended)**
   ```python
   # Old way (still works)
   from yokatlas_py import YOKATLASLisansTercihSihirbazi
   search = YOKATLASLisansTercihSihirbazi({"universite": "BOĞAZİÇİ ÜNİVERSİTESİ"})
   
   # New way (with fuzzy matching)
   from yokatlas_py import search_lisans_programs
   results = search_lisans_programs({"uni_adi": "boğaziçi"})  # Much easier!
   ```

3. **Optional: Use type-safe features**
   ```python
   from yokatlas_py.models import SearchParams
   params = SearchParams(puan_turu="say", length=10)
   ```

## License | Lisans

This project is licensed under the MIT License - see the LICENSE file for details.

Bu proje MIT Lisansı ile lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.
