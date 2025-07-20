# YOKATLAS Lisans (Bachelor's) Search Functionality Analysis

## Overview

I tested the lisans (bachelor's) search functionality in the yokatlas-py library to understand how it works, what data it returns, and what the response structure looks like.

## Search Functions Available

### 1. `search_lisans_programs(params: dict)`
- Enhanced wrapper function with fuzzy matching and parameter normalization
- Accepts parameters as a dictionary
- Supports common variations like `"university"`, `"uni"`, `"program"`, `"score_type"` etc.
- Returns a list of program dictionaries

### 2. `YOKATLASLisansTercihSihirbazi` class
- Direct API interface class
- Requires exact parameter names as used by the API
- More control over search parameters

## Data Structure Returned

Each search result contains the following fields:

```json
{
  "yop_kodu": "102210277",                    // Program code (unique identifier)
  "uni_adi": "BOĞAZİÇİ ÜNİVERSİTESİ",        // University name
  "fakulte": "Mühendislik Fakültesi",         // Faculty name
  "program_adi": "Bilgisayar Mühendisliği",   // Program name
  "program_detay": "(İngilizce) (4 Yıllık)",  // Program details (language, duration)
  "sehir_adi": "İSTANBUL",                    // City
  "universite_turu": "Devlet",                // University type (Devlet/Vakıf)
  "ucret_burs": "Ücretsiz",                   // Fee status (Ücretsiz/Burslu/Ücretli)
  "ogretim_turu": "Örgün",                    // Education type (Örgün/Uzaktan)
  "kontenjan": {                              // Quotas by year
    "2024": "105+3+0+0+0",
    "2023": "100+3+0+0+0",
    "2022": "90+3",
    "2021": "90+3"
  },
  "yerlesen": {                               // Placed students by year
    "2024": "108(105+3+0+0+0)",
    "2023": "103",
    "2022": "93",
    "2021": "93"
  },
  "tbs": {                                    // Success rank by year
    "2024": "1008",
    "2023": "775",
    "2022": "315",
    "2021": "327"
  },
  "taban": {                                  // Base scores by year
    "2024": "539.31607",
    "2023": "544.50335",
    "2022": "547.16431",
    "2021": "521.30695"
  }
}
```

## Test Results Summary

### Working Search Examples

1. **University Search**:
   ```python
   search_lisans_programs({"university": "boğaziçi"})  # 22 programs
   search_lisans_programs({"university": "odtu"})      # 50 programs
   search_lisans_programs({"university": "istanbul teknik"})  # 50 programs
   ```

2. **Program Search**:
   ```python
   search_lisans_programs({"program": "bilgisayar"})  # 78 programs
   search_lisans_programs({"program": "bilgisayar mühendisliği"})  # 55 programs
   ```

3. **Score Type Search**:
   ```python
   search_lisans_programs({"score_type": "say"})  # 50 programs (default limit)
   search_lisans_programs({"score_type": "ea"})   # 50 programs
   ```

### University Name Normalization

The search function has excellent fuzzy matching for university names:

- `"odtu"`, `"odtü"`, `"orta doğu"`, `"metu"` → All find "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"
- `"boğaziçi"` → Finds "BOĞAZİÇİ ÜNİVERSİTESİ"  
- `"istanbul teknik"` → Finds "İSTANBUL TEKNİK ÜNİVERSİTESİ"

### Score Types Available

All score types return results:
- **SAY** (Science/Math): Engineering, medicine, science programs
- **EA** (Equal Weight): Economics, business, social sciences
- **SÖZ** (Verbal): Language, literature, communication programs  
- **DİL** (Language): Foreign language and translation programs

### Top Universities by Computer Engineering Scores (2024)

1. KOÇ ÜNİVERSİTESİ - 550.88113
2. İHSAN DOĞRAMACI BİLKENT ÜNİVERSİTESİ - 547.38649
3. ORTA DOĞU TEKNİK ÜNİVERSİTESİ - 539.85314
4. BOĞAZİÇİ ÜNİVERSİTESİ - 539.31607
5. İSTANBUL TEKNİK ÜNİVERSİTESİ - 536.3077

## Issues Found

### Searches Returning Zero Results

Some searches that should logically return results don't work:

1. **Combined University + Program**: 
   ```python
   search_lisans_programs({"university": "odtu", "program": "mühendislik"})  # 0 results
   ```
   - ODTU alone: 50 programs ✓
   - "mühendislik" alone: 40 programs ✓
   - Combined: 0 results ✗

2. **Score Type + Program Combinations**:
   ```python
   search_lisans_programs({"score_type": "ea", "program": "matematik"})  # 0 results
   ```
   - "matematik" alone: 130 programs ✓
   - EA score type alone: 50 programs ✓
   - Combined: 0 results ✗

3. **Missing Programs**:
   ```python
   search_lisans_programs({"program": "türk dili"})     # 0 results
   search_lisans_programs({"program": "ingilizce"})     # 0 results
   ```

### Possible Causes

1. **API Limitations**: The YOKATLAS API may not support certain parameter combinations
2. **Exact Matching**: Program names might need exact matches rather than partial matches
3. **Program Name Variations**: Some programs might have different official names

## Comparison: Lisans vs Önlisans

Both lisans and önlisans programs return identical field structures:

- **Common fields**: All 13 fields are identical
- **Differences**: Only in the actual data content (different programs, universities, scores)
- **Score types**: Önlisans typically uses "TYT" while lisans uses SAY/EA/SÖZ/DİL

## Recommendations

1. **Use broad searches**: Search by university OR program separately, then filter results
2. **Program name expansion**: The library includes good program name expansion (e.g., "bilgisayar" → "Bilgisayar Mühendisliği")
3. **Exact names**: For specific searches, use exact program names from the results
4. **Error handling**: Add checks for empty results and suggest alternative searches

## Usage Examples

```python
from yokatlas_py import search_lisans_programs

# Find all programs at Boğaziçi
bogazici_programs = search_lisans_programs({"university": "boğaziçi"})

# Find all computer engineering programs
cs_programs = search_lisans_programs({"program": "bilgisayar mühendisliği"})

# Find science programs
science_programs = search_lisans_programs({"score_type": "say"})

# Sort by score
sorted_programs = sorted(cs_programs, 
                        key=lambda x: float(x['taban']['2024']) if x['taban'].get('2024', '0').replace('.', '').isdigit() else 0, 
                        reverse=True)
```