
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

## How to | Kullanım

### Quick Start with Type Safety | Tip Güvenli Hızlı Başlangıç

```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi
from yokatlas_py.models import SearchParams, ProgramInfo

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

## Migration from v0.3.x | v0.3.x'den Geçiş

### Breaking Changes | Değişiklikler

- **Python 3.9+ Required**: Updated from 3.8+ to 3.9+
- **New Dependencies**: Added pydantic and typing-extensions
- **Type Hints**: All functions now have type annotations

### Migration Steps | Geçiş Adımları

1. **Update Python version to 3.9+**
   ```bash
   # Check your Python version
   python --version
   ```

2. **Update the package**
   ```bash
   pip install --upgrade yokatlas-py
   ```

3. **Optional: Use new type-safe features**
   ```python
   # Old way (still works)
   params = {"puan_turu": "say", "length": 10}
   
   # New way (with validation)
   from yokatlas_py.models import SearchParams
   params = SearchParams(puan_turu="say", length=10)
   ```

## License | Lisans

This project is licensed under the MIT License - see the LICENSE file for details.

Bu proje MIT Lisansı ile lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.
