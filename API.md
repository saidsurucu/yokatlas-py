# YOKATLAS-py API Dokümantasyonu

Tam API referansı.

## İçindekiler

- [Akıllı Arama Fonksiyonları](#akıllı-arama-fonksiyonları)
- [Arama Sınıfları](#arama-sınıfları)
- [Atlas Sınıfları](#atlas-sınıfları)
- [Fetcher Sınıfları](#fetcher-sınıfları)
- [HTTP Client](#http-client)
- [Arama Yardımcıları](#arama-yardımcıları)
- [Pydantic Modelleri](#pydantic-modelleri)
- [Form Verileri](#form-verileri)

---

## Akıllı Arama Fonksiyonları

### `search_lisans_programs(params, smart_search=True)`

Bulanık eşleştirme ile lisans programı arama.

```python
from yokatlas_py import search_lisans_programs

results = search_lisans_programs({
    "uni_adi": "boğaziçi",       # "BOĞAZİÇİ ÜNİVERSİTESİ" bulur
    "program_adi": "bilgisayar", # Tüm bilgisayar programlarını bulur
    "puan_turu": "say",
    "sehir": "istanbul"
})
```

**Parametreler:**
| Parametre | Alternatifler | Açıklama |
|-----------|---------------|----------|
| `uni_adi` | `university`, `uni` | Üniversite adı (bulanık) |
| `program_adi` | `bolum`, `department` | Program adı (kısmi) |
| `puan_turu` | `score_type` | `say`, `ea`, `söz`, `dil` |
| `sehir` | `city`, `il` | Şehir |
| `universite_turu` | `uni_type` | `Devlet`, `Vakıf`, `KKTC` |
| `length` | - | Sayfa başına sonuç (varsayılan: 50) |

---

### `search_onlisans_programs(params, smart_search=True)`

Önlisans programı arama.

```python
from yokatlas_py import search_onlisans_programs

results = search_onlisans_programs({
    "uni_adi": "anadolu",
    "program_adi": "turizm",
    "puan_turu": "tyt"
})
```

---

### `search_programs(params, program_type=None)`

Her iki program türünde arama.

```python
from yokatlas_py import search_programs

all_results = search_programs({"uni_adi": "ankara"})
print(f"Lisans: {len(all_results['lisans'])}")
print(f"Önlisans: {len(all_results['onlisans'])}")
```

---

## Arama Sınıfları

### `YOKATLASLisansTercihSihirbazi(params)`

Direkt YOKATLAS API erişimi.

```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi

search = YOKATLASLisansTercihSihirbazi({
    "puan_turu": "say",
    "universite": "BOĞAZİÇİ ÜNİVERSİTESİ",  # Tam isim gerekli
    "length": 10
})
results = search.search()
```

### `YOKATLASOnlisansTercihSihirbazi(params)`

```python
from yokatlas_py import YOKATLASOnlisansTercihSihirbazi

search = YOKATLASOnlisansTercihSihirbazi({
    "puan_turu": "tyt",
    "universite": "ANADOLU ÜNİVERSİTESİ",
    "length": 20
})
results = search.search()
```

---

## Atlas Sınıfları

### `YOKATLASLisansAtlasi(params)`

Program detaylarını getir.

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

async def get_details():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    return await atlas.fetch_all_details()

data = asyncio.run(get_details())
```

**Dönen Veri Anahtarları (12):**

| Anahtar | Açıklama |
|---------|----------|
| `genel_bilgiler` | Program, kontenjan, puan bilgileri |
| `cinsiyet_dagilimi` | Cinsiyet dağılımı |
| `cografi_bolge_dagilimi` | Coğrafi bölge dağılımı |
| `lise_grubu_dagilimi` | Lise grubu dağılımı |
| `lise_bazinda_yerlesen` | Lise bazında yerleşen |
| `tercih_istatistikleri` | Tercih istatistikleri |
| `tercih_edilen_programlar` | Tercih edilen programlar |
| `tercih_edilen_universiteler` | Tercih edilen üniversiteler |
| `tercih_edilen_program_turleri` | Tercih edilen program türleri |
| `tercih_edilen_universite_turleri` | Tercih edilen üniversite türleri |
| `taban_puan_basari_sirasi` | Taban puan ve başarı sırası |
| `yerlesen_puan_bilgileri` | Yerleşen puan bilgileri |

**Örnek Çıktı:**
```python
{
  "genel_bilgiler": {
    "program_info": {
      "ÖSYM Program Kodu": "103910743",
      "Üniversite": "FIRAT ÜNİVERSİTESİ",
      "Puan Türü": "SAY"
    },
    "kontenjan_info": {
      "Genel Kontenjan": "53",
      "Toplam Yerleşen": "60"
    },
    "puan_info": {
      "0,12 Katsayı ile Yerleşen Son Kişinin Puanı": "329,82598"
    }
  }
}
```

### `YOKATLASOnlisansAtlasi(params)`

Önlisans için aynı yapı (10 veri tipi).

```python
from yokatlas_py import YOKATLASOnlisansAtlasi

async def get_onlisans():
    atlas = YOKATLASOnlisansAtlasi({
        'program_id': '105590209',
        'year': 2024
    })
    return await atlas.fetch_all_details()
```

---

## Fetcher Sınıfları

v0.5.4'te eklenen class-based fetcher sistemi.

### BaseFetcher

Tüm fetcher'ların temel sınıfı.

```python
from yokatlas_py.base_fetcher import BaseFetcher

class CustomFetcher(BaseFetcher):
    ENDPOINT = "1010.php"
    PROGRAM_TYPE = "lisans"
    RESULT_KEY = "custom_data"

    def parse(self, html: str) -> dict:
        # HTML parse logic
        pass
```

### Hazır Fetcher'lar

```python
from yokatlas_py.fetchers import (
    # Lisans
    GenelBilgilerLisansFetcher,
    CinsiyetDagilimiLisansFetcher,
    TercihIstatistikleriLisansFetcher,
    # ... 12 fetcher

    # Önlisans
    GenelBilgilerOnlisansFetcher,
    CinsiyetDagilimiOnlisansFetcher,
    # ... 10 fetcher
)

# Kullanım
async def fetch_gender():
    fetcher = CinsiyetDagilimiLisansFetcher('103910743', 2024)
    return await fetcher.fetch()
```

**Tüm Fetcher'lar:**

| Fetcher | Lisans | Önlisans |
|---------|--------|----------|
| GenelBilgiler | ✅ | ✅ |
| CinsiyetDagilimi | ✅ | ✅ |
| TercihIstatistikleri | ✅ | ✅ |
| LiseGrubuVeTipiDagilimi | ✅ | ✅ |
| LiseBazindaYerlesenDagilimi | ✅ | ✅ |
| SehirVeCografiBolgeDagilimi | ✅ | ✅ |
| TercihEdilenProgramlar | ✅ | ✅ |
| TercihEdilenUniversiteler | ✅ | ✅ |
| TercihEdilenProgramTurleri | ✅ | ✅ |
| TercihEdilenUniversiteTurleri | ✅ | ✅ |
| TabanPuanVeBasariSirasiIstatistikleri | ✅ | ✅ |
| YerlesenBasariSiralari | ✅ | ❌ |
| YerlesenPuanBilgileri | ✅ | ❌ |

---

## HTTP Client

Singleton HTTP client with connection pooling.

```python
from yokatlas_py.http_client import YOKATLASClient

# URL oluştur
url = YOKATLASClient.build_url(
    program_type="lisans",
    endpoint="1000_1.php",
    program_id="103910743",
    year=2024
)
# https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_1.php?y=103910743

# Client kullan
async def fetch():
    client = await YOKATLASClient.get_client()
    response = await client.get(url)
    return response.text

# Cleanup
await YOKATLASClient.close()
```

**Özellikler:**
- Connection pooling (max 100 bağlantı)
- `X-Requested-With: XMLHttpRequest` header
- `follow_redirects=True`
- 30 saniye timeout

---

## Arama Yardımcıları

### `find_best_university_match(name, program_type)`

```python
from yokatlas_py.search_utils import find_best_university_match

match = find_best_university_match("odtu", "lisans")
# "ORTA DOĞU TEKNİK ÜNİVERSİTESİ"

match = find_best_university_match("boun", "lisans")
# "BOĞAZİÇİ ÜNİVERSİTESİ"
```

### `expand_program_name(name, program_type)`

```python
from yokatlas_py.search_utils import expand_program_name

programs = expand_program_name("bilgisayar", "lisans")
# ["Bilgisayar Mühendisliği", "Bilgisayar Bilimleri", ...]
```

### `normalize_search_params(params, program_type)`

```python
from yokatlas_py.search_utils import normalize_search_params

normalized = normalize_search_params({
    "uni": "boğaziçi",
    "bolum": "bilgisayar"
}, "lisans")
# {"universite": "BOĞAZİÇİ ÜNİVERSİTESİ", "program": "bilgisayar"}
```

---

## Pydantic Modelleri

### SearchParams

```python
from yokatlas_py.models import SearchParams

params = SearchParams(
    puan_turu="say",
    universite="Boğaziçi Üniversitesi",
    length=10
)
```

### ProgramInfo

```python
from yokatlas_py.models import ProgramInfo

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
```

---

## Form Verileri

### Lisans

```python
from yokatlas_py.form_data import UNIVERSITIES, PROGRAMS

print(f"Üniversite: {len(UNIVERSITIES)}")  # 235
print(f"Program: {len(PROGRAMS)}")          # 200+
```

### Önlisans

```python
from yokatlas_py.onlisans_form_data import ONLISANS_UNIVERSITIES, ONLISANS_PROGRAMS

print(f"Üniversite: {len(ONLISANS_UNIVERSITIES)}")  # 176
print(f"Program: {len(ONLISANS_PROGRAMS)}")          # 250+
```

---

## Hata Yönetimi

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

async def safe_fetch():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    result = await atlas.fetch_all_details()

    for key, value in result.items():
        if isinstance(value, dict) and 'error' in value:
            print(f"❌ {key}: {value['error']}")
        else:
            print(f"✅ {key}")

asyncio.run(safe_fetch())
```

**Sık Hatalar:**

| Hata | Sebep |
|------|-------|
| `HTTP 418` | Rate limiting |
| `HTTP 404` | Geçersiz program ID |
| `Required tables not found` | Veri yok |

---

## Desteklenen Yıllar

| Tür | Yıllar |
|-----|--------|
| Lisans | 2021, 2022, 2023, 2024 |
| Önlisans | 2023, 2024 |
