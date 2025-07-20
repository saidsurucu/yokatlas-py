# YOKATLAS-py API Documentation

Complete API reference for yokatlas-py library with smart search capabilities.

## Table of Contents

- [Smart Search Functions](#smart-search-functions)
- [Core Search Classes](#core-search-classes)
- [Atlas Classes](#atlas-classes)
- [Search Utilities](#search-utilities)
- [Pydantic Models](#pydantic-models)
- [Form Data](#form-data)
- [Error Handling](#error-handling)

---

## Smart Search Functions

### `search_lisans_programs(params, smart_search=True)`

Enhanced search for lisans (bachelor's) programs with fuzzy matching and intelligent parameter normalization.

**Parameters:**
- `params` (`dict[str, Any]`): Search parameters
- `smart_search` (`bool`, optional): Enable smart features. Default: `True`

**Returns:**
- `list[dict[str, Any]]`: List of matching programs

**Example:**
```python
from yokatlas_py import search_lisans_programs

# Smart search with fuzzy matching
results = search_lisans_programs({
    "uni_adi": "boğaziçi",      # Fuzzy matches to "BOĞAZİÇİ ÜNİVERSİTESİ"
    "program_adi": "bilgisayar", # Finds all computer programs
    "puan_turu": "say",
    "sehir": "istanbul"
})

print(f"Found {len(results)} programs")
```

**Supported Parameters:**
- `uni_adi` / `university` / `uni`: University name (supports fuzzy matching)
- `program_adi` / `bolum` / `department`: Program name (supports partial matching)
- `puan_turu` / `score_type`: Score type (`"say"`, `"ea"`, `"söz"`, `"dil"`)
- `sehir` / `city` / `il`: City name
- `universite_turu` / `uni_type`: University type (`"Devlet"`, `"Vakıf"`, `"KKTC"`, `"Yurt Dışı"`)
- `ucret` / `fee`: Fee type (`"Ücretsiz"`, `"Ücretli"`, `"Burslu"`, etc.)
- `ogretim_turu` / `education_type`: Education type (`"Örgün"`, `"İkinci"`, `"Açıköğretim"`, `"Uzaktan"`)
- `length`: Results per page (default: 50)
- `page`: Page number for pagination

---

### `search_onlisans_programs(params, smart_search=True)`

Enhanced search for önlisans (associate degree) programs with fuzzy matching.

**Parameters:**
- `params` (`dict[str, Any]`): Search parameters
- `smart_search` (`bool`, optional): Enable smart features. Default: `True`

**Returns:**
- `list[dict[str, Any]]`: List of matching programs

**Example:**
```python
from yokatlas_py import search_onlisans_programs

# Smart search for associate programs
results = search_onlisans_programs({
    "uni_adi": "anadolu",       # Fuzzy matches to "ANADOLU ÜNİVERSİTESİ"
    "program_adi": "turizm",    # Finds all tourism programs
    "sehir": "eskişehir"
})

for program in results:
    print(f"{program['uni_adi']} - {program['program_adi']}")
```

**Note:** Önlisans programs use `"tyt"` score type instead of lisans score types.

---

### `search_programs(params, program_type=None, smart_search=True)`

Universal search function for both lisans and önlisans programs.

**Parameters:**
- `params` (`dict[str, Any]`): Search parameters
- `program_type` (`str`, optional): `"lisans"`, `"onlisans"`, or `None` for both
- `smart_search` (`bool`, optional): Enable smart features. Default: `True`

**Returns:**
- `dict[str, list[dict[str, Any]]]`: Dictionary with `"lisans"` and/or `"onlisans"` keys

**Example:**
```python
from yokatlas_py import search_programs

# Search both program types
all_results = search_programs({
    "uni_adi": "ankara",
    "program_adi": "bilgisayar"
})

print(f"Lisans programs: {len(all_results['lisans'])}")
print(f"Önlisans programs: {len(all_results['onlisans'])}")

# Search only specific type
lisans_only = search_programs({
    "uni_adi": "odtu",
    "program_adi": "mühendislik"
}, program_type="lisans")
```

---

## Core Search Classes

### `YOKATLASLisansTercihSihirbazi(params)`

Direct interface to YOKATLAS lisans search API.

**Parameters:**
- `params` (`dict[str, Any]`): Raw search parameters

**Methods:**

#### `search() -> list[dict[str, Any]]`
Perform search and return results.

**Example:**
```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi

# Direct API usage
search = YOKATLASLisansTercihSihirbazi({
    "puan_turu": "say",
    "universite": "BOĞAZİÇİ ÜNİVERSİTESİ",  # Exact name required
    "program": "Bilgisayar Mühendisliği",    # Exact name required
    "length": 10
})

results = search.search()
```

**Required Exact Parameter Names:**
- `universite`: Full university name
- `program`: Exact program name
- `puan_turu`: Score type
- `sehir`: City name (uppercase)
- `universite_turu`: University type
- `ucret`: Fee type
- `ogretim_turu`: Education type

---

### `YOKATLASOnlisansTercihSihirbazi(params)`

Direct interface to YOKATLAS önlisans search API.

**Parameters:**
- `params` (`dict[str, Any]`): Raw search parameters

**Methods:**

#### `search() -> list[dict[str, Any]]`
Perform search and return results.

**Example:**
```python
from yokatlas_py import YOKATLASOnlisansTercihSihirbazi

# Direct önlisans search
search = YOKATLASOnlisansTercihSihirbazi({
    "universite": "ANADOLU ÜNİVERSİTESİ",
    "program": "Bilgisayar Programcılığı",
    "length": 20
})

results = search.search()
```

---

## Atlas Classes

### `YOKATLASLisansAtlasi(params)`

Fetch detailed information for a specific lisans program.

**Parameters:**
- `params` (`dict[str, Any]`): Atlas parameters containing `program_id` and `year`

**Methods:**

#### `async fetch_all_details() -> dict[str, Any]`
Fetch comprehensive program data from all available sources.

**Example:**
```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

async def get_program_details():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '104111719',  # Program YOP code
        'year': 2024
    })
    
    details = await atlas.fetch_all_details()
    
    print(f"Program: {details.get('program_name', 'N/A')}")
    print(f"University: {details.get('university_name', 'N/A')}")
    print(f"Faculty: {details.get('faculty_name', 'N/A')}")
    
    # Access specific data categories
    if 'gender_data' in details:
        print(f"Gender distribution: {details['gender_data']}")
    
    if 'score_data' in details:
        print(f"Score statistics: {details['score_data']}")

# Run async function
asyncio.run(get_program_details())
```

**Available Data Categories:**
- `gender_data`: Gender distribution statistics
- `score_data`: Score and ranking information
- `city_data`: Geographic distribution
- `high_school_data`: High school type statistics
- `quota_data`: Quota and placement information
- And 25+ more data categories

---

### `YOKATLASOnlisansAtlasi(params)`

Fetch detailed information for a specific önlisans program.

**Parameters:**
- `params` (`dict[str, Any]`): Atlas parameters containing `program_id` and `year`

**Methods:**

#### `async fetch_all_details() -> dict[str, Any]`
Fetch comprehensive program data from all available sources.

**Example:**
```python
import asyncio
from yokatlas_py import YOKATLASOnlisansAtlasi

async def get_onlisans_details():
    atlas = YOKATLASOnlisansAtlasi({
        'program_id': '203550463',  # Önlisans program YOP code
        'year': 2024
    })
    
    details = await atlas.fetch_all_details()
    return details

# Usage
details = asyncio.run(get_onlisans_details())
```

---

## Search Utilities

### `find_best_university_match(name, program_type="lisans")`

Find the best matching university name using fuzzy matching.

**Parameters:**
- `name` (`str`): University name (partial or abbreviated)
- `program_type` (`str`, optional): `"lisans"` or `"onlisans"`. Default: `"lisans"`

**Returns:**
- `str`: Best matching official university name

**Example:**
```python
from yokatlas_py.search_utils import find_best_university_match

# Fuzzy matching examples
match1 = find_best_university_match("boğaziçi", "lisans")
# Returns: "BOĞAZİÇİ ÜNİVERSİTESİ"

match2 = find_best_university_match("odtu", "lisans") 
# Returns: "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"

match3 = find_best_university_match("itu", "onlisans")
# Returns: "İSTANBUL TEKNİK ÜNİVERSİTESİ"
```

---

### `expand_program_name(name, program_type="lisans")`

Expand a program name to find all related programs.

**Parameters:**
- `name` (`str`): Program name (partial)
- `program_type` (`str`, optional): `"lisans"` or `"onlisans"`. Default: `"lisans"`

**Returns:**
- `list[str]`: List of matching program names

**Example:**
```python
from yokatlas_py.search_utils import expand_program_name

# Find all computer-related programs
programs = expand_program_name("bilgisayar", "lisans")
# Returns: ["Bilgisayar Mühendisliği", "Bilgisayar Bilimleri", ...]

# Find tourism programs in önlisans
tourism_programs = expand_program_name("turizm", "onlisans")
# Returns: ["Turizm ve Otel İşletmeciliği", "Turizm Animasyonu", ...]
```

---

### `normalize_search_params(params, program_type="lisans")`

Normalize and validate search parameters.

**Parameters:**
- `params` (`dict[str, Any]`): Raw search parameters
- `program_type` (`str`, optional): `"lisans"` or `"onlisans"`. Default: `"lisans"`

**Returns:**
- `dict[str, Any]`: Normalized parameters

**Example:**
```python
from yokatlas_py.search_utils import normalize_search_params

# Input with various parameter names
raw_params = {
    "uni": "boğaziçi",           # Gets normalized to "universite"
    "bolum": "bilgisayar",       # Gets normalized to "program"
    "city": "istanbul",          # Gets normalized to "sehir"
    "score_type": "say"          # Gets normalized to "puan_turu"
}

normalized = normalize_search_params(raw_params, "lisans")
# Returns:
# {
#     "universite": "BOĞAZİÇİ ÜNİVERSİTESİ",
#     "program": "bilgisayar",
#     "sehir": "İSTANBUL",
#     "puan_turu": "say"
# }
```

---

## Pydantic Models

### `SearchParams`

Type-safe search parameter validation.

**Fields:**
- `puan_turu` (`str`, optional): Score type
- `universite` (`str`, optional): University name
- `program` (`str`, optional): Program name
- `sehir` (`str`, optional): City name
- `universite_turu` (`str`, optional): University type
- `ucret` (`str`, optional): Fee type
- `ogretim_turu` (`str`, optional): Education type
- `length` (`int`, optional): Results per page
- `start` (`int`, optional): Start index

**Example:**
```python
from yokatlas_py.models import SearchParams
from pydantic import ValidationError

try:
    params = SearchParams(
        puan_turu="say",
        universite="Boğaziçi Üniversitesi",
        length=10,
        start=0
    )
    print(params.model_dump(exclude_none=True))
except ValidationError as e:
    print(f"Validation error: {e}")
```

---

### `ProgramInfo`

University program information with validation.

**Fields:**
- `yop_kodu` (`str`): Program code
- `uni_adi` (`str`): University name
- `fakulte` (`str`): Faculty name
- `program_adi` (`str`): Program name
- `program_detay` (`str`, optional): Program details
- `sehir_adi` (`str`): City name
- `universite_turu` (`str`): University type
- `ucret_burs` (`str`): Fee/scholarship info
- `ogretim_turu` (`str`): Education type
- `kontenjan` (`dict`, optional): Quota information
- `yerlesen` (`dict`, optional): Placement statistics
- `taban` (`dict`, optional): Base scores
- `tbs` (`dict`, optional): Success rankings

**Example:**
```python
from yokatlas_py.models import ProgramInfo

# Validate program data
program = ProgramInfo(
    yop_kodu="104111719",
    uni_adi="BOĞAZİÇİ ÜNİVERSİTESİ",
    fakulte="Mühendislik Fakültesi",
    program_adi="Bilgisayar Mühendisliği",
    sehir_adi="İSTANBUL",
    universite_turu="Devlet",
    ucret_burs="Ücretsiz",
    ogretim_turu="Örgün"
)

print(f"Program: {program.program_adi}")
print(f"University: {program.uni_adi}")
```

---

### `YearlyData`

Year-based statistical data validation.

**Fields:**
- `year` (`int`): Year
- `value` (`str` | `int` | `float`): Data value

**Example:**
```python
from yokatlas_py.models import YearlyData

yearly_score = YearlyData(year=2024, value=456.78)
yearly_quota = YearlyData(year=2024, value="50+2+0+0+0")
```

---

### `ErrorResponse`

Error handling and reporting.

**Fields:**
- `error` (`str`): Error message
- `status_code` (`int`, optional): HTTP status code
- `details` (`dict`, optional): Additional error details

---

## Form Data

### `UNIVERSITIES` (from `form_data.py`)

Complete list of 235 lisans universities.

**Example:**
```python
from yokatlas_py.form_data import UNIVERSITIES

print(f"Total lisans universities: {len(UNIVERSITIES)}")
print("First 5:", UNIVERSITIES[:5])

# Check if university exists
if "BOĞAZİÇİ ÜNİVERSİTESİ" in UNIVERSITIES:
    print("Boğaziçi University found!")
```

---

### `PROGRAMS` (from `form_data.py`)

Complete list of 200+ lisans programs.

**Example:**
```python
from yokatlas_py.form_data import PROGRAMS

# Find computer-related programs
computer_programs = [p for p in PROGRAMS if "bilgisayar" in p.lower()]
print(f"Computer programs: {len(computer_programs)}")
```

---

### `ONLISANS_UNIVERSITIES` (from `onlisans_form_data.py`)

Complete list of 176 önlisans universities.

**Example:**
```python
from yokatlas_py.onlisans_form_data import ONLISANS_UNIVERSITIES

print(f"Total önlisans universities: {len(ONLISANS_UNIVERSITIES)}")
```

---

### `ONLISANS_PROGRAMS` (from `onlisans_form_data.py`)

Complete list of 250+ önlisans programs.

**Example:**
```python
from yokatlas_py.onlisans_form_data import ONLISANS_PROGRAMS

# Find tourism programs
tourism_programs = [p for p in ONLISANS_PROGRAMS if "turizm" in p.lower()]
print(f"Tourism programs: {len(tourism_programs)}")
```

---

## Error Handling

### Common Error Types

1. **HTTP Errors**: Network connectivity issues
2. **Parsing Errors**: Invalid API response format
3. **Validation Errors**: Invalid parameters with pydantic
4. **Empty Results**: No programs match search criteria

### Error Handling Examples

```python
from yokatlas_py import search_lisans_programs
from yokatlas_py.models import SearchParams
from pydantic import ValidationError
import httpx

# Handle validation errors
try:
    params = SearchParams(
        puan_turu="invalid_type",  # Invalid score type
        length=-5                  # Invalid length
    )
except ValidationError as e:
    print(f"Parameter validation failed: {e}")

# Handle search errors
try:
    results = search_lisans_programs({
        "uni_adi": "nonexistent_university",
        "program_adi": "nonexistent_program"
    })
    
    if not results:
        print("No programs found matching your criteria")
    else:
        print(f"Found {len(results)} programs")
        
except httpx.RequestError as e:
    print(f"Network error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Error Response Format

```python
# When API returns an error
{
    "error": "HTTP 500: Internal Server Error",
    "status_code": 500,
    "details": {
        "url": "https://yokatlas.yok.gov.tr/...",
        "method": "POST"
    }
}
```

---

## Performance Tips

1. **Use Smart Search**: Prefer `search_lisans_programs()` over direct class usage
2. **Batch Requests**: Use `search_programs()` for both program types
3. **Limit Results**: Use `length` parameter to control response size
4. **Cache Universities**: Import form data once and reuse for validation
5. **Async for Atlas**: Always use `await` with atlas methods

### Example Performance Optimization

```python
from yokatlas_py import search_programs
from yokatlas_py.form_data import UNIVERSITIES

# Pre-validate university exists
def smart_search(uni_name, program_name):
    # Quick local validation
    if uni_name.upper() not in [u.upper() for u in UNIVERSITIES]:
        print(f"University '{uni_name}' not found in database")
        return []
    
    # Perform search
    return search_programs({
        "uni_adi": uni_name,
        "program_adi": program_name,
        "length": 20  # Limit results for better performance
    })

results = smart_search("boğaziçi", "bilgisayar")
```

---

## Version Compatibility

- **v0.4.2+**: Full smart search features
- **v0.4.1+**: Pydantic models and type safety
- **v0.4.0+**: httpx HTTP client
- **v0.3.x**: Legacy API (still supported)

**Migration from older versions:**
```python
# Old way (v0.3.x)
from yokatlas_py import YOKATLASLisansTercihSihirbazi
search = YOKATLASLisansTercihSihirbazi({"universite": "BOĞAZİÇİ ÜNİVERSİTESİ"})

# New way (v0.4.2+) - Recommended
from yokatlas_py import search_lisans_programs
results = search_lisans_programs({"uni_adi": "boğaziçi"})
```