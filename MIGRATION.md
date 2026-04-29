# v0.x → v0.6.0 Migration Rehberi

## Neden v0.6.0?

YÖK Atlas (`https://yokatlas.yok.gov.tr`) 2025 sonunda tamamen React tabanlı bir SPA'ya geçti. Eski PHP HTML endpoint'leri (`/lisans/{yil}/{kod}.php`, `/onlisans/{yil}/{kod}.php`, `/lisans-tercih-sihirbazi.php`, `/server_side/server_processing-atlas2016-TS-t4.php` vb.) artık tek bir boş SPA shell'i döndürüyor — yani v0.x kütüphanesindeki tüm dört ana sınıf ve 60+ HTML fetcher modülü çalışmıyor.

v0.6.0 yeni resmi JSON API'ye karşı sıfırdan yazıldı (`/api/tercih-kilavuz/*`).

## Hızlı eşleme

| v0.x | v0.6.0 |
|---|---|
| `YOKATLASLisansAtlasi(params).fetch_all_details()` | `YokAtlasClient().get_program(kilavuz_kodu)` |
| `YOKATLASOnlisansAtlasi(params).fetch_all_details()` | `YokAtlasClient().get_program(kilavuz_kodu)` |
| `YOKATLASLisansTercihSihirbazi(params).search()` | `YokAtlasClient().search(SearchFilters(...))` |
| `YOKATLASOnlisansTercihSihirbazi(params).search()` | `YokAtlasClient().search(SearchFilters(birim_turu_id=47, ...))` |
| `search_lisans_programs({...})` | `search_programs({...})` (tek fonksiyon, lisans+önlisans) |
| `search_onlisans_programs({...})` | `search_programs({"birim_turu_id": 47, ...})` |
| `search_programs({...})` | `search_programs({...})` |

## Ana kırılan değişiklikler

### 1. `year` parametresi kalktı

v0.x'te yıl bazlı endpoint vardı (lisans 2021–2024, önlisans 2023–2024). v0.6.0'da **her sonuçta 4 yıllık veri zaten gelir** — `current` (en güncel) + `history` (3 önceki yıl).

```python
# v0.x
atlas = YOKATLASLisansAtlasi({"yop_kodu": "...", "year": 2024})

# v0.6.0
prog = client.get_program(102210277)
for stats in prog.all_years:
    print(stats.year, stats.min_puan, stats.basari_sirasi)
# → 2025, 2024, 2023, 2022
```

### 2. Lisans/Önlisans ayrımı kalktı

Tek arama endpoint'i her ikisini de döner. Önlisans'a sadece için filtre verin:

```python
client.search(SearchFilters(birim_turu_id=47))  # 47 = ÖNLİSANS
```

### 3. Atlas detay sınıflarının ~25 alt-kategorisi kaldırıldı

Yeni API bunları **sunmuyor**, alternatif yok:

- `cinsiyet_dagilimi`
- `lise_alani_dagilimi`, `lise_grubu_ve_tipi_dagilimi`, `lise_bazinda_yerlesen_dagilimi`
- `yerlesen_il_dagilimi`, `sehir_ve_cografi_bolge_dagilimi`
- `tercih_edilen_universiteler`, `tercih_edilen_iller`, `tercih_edilen_programlar`, `tercih_edilen_universite_turleri`, `tercih_edilen_program_turleri`, `tercih_istatistikleri`, `yerlesen_tercih_istatistikleri`, `tercih_kullanma_oranlari`
- `mezuniyet_yili_dagilimi`, `mezuniyet_yili_cinsiyet_dagilimi`
- `kayitli_ogrenci_cinsiyet_dagilimi`, `okul_birincisi_yerlesen`
- `degisim_programi_bilgileri`, `yatay_gecis_bilgileri`
- `yerlesen_son_kisi_bilgileri`, `yerlesen_ortalama_netler`, `yerlesen_puan_bilgileri`, `yerlesen_basari_siralari`
- `taban_puan_ve_basari_sirasi_istatistikleri` (sadece `current.min_puan` + `current.basari_sirasi` ve 3 yıllık `history` mevcut)

v0.6.0 sadece resmi JSON API'nin sunduğu 61 alanı döner: kontenjan/yerleşen/akademik kadro/KPSS/taban puan/başarı sırası — her biri 4 yıl için.

### 4. Form verisi sabit dosyaları silindi

`form_data.py` ve `onlisans_form_data.py` (üniversite/program ID listeleri) silindi. Bu listeler artık **runtime'da** `/api/tercih-kilavuz/universiteler` ve `/api/tercih-kilavuz/universite-programlar` endpoint'lerinden çekilip 1 saat boyunca cache'lenir.

### 5. Akıllı arama parametre adları

Artık `SearchFilters` modelinde tek tip bir alan yapısı var:

```python
# v0.x
search_lisans_programs({
    "puan_turu": "say",
    "universite": "boğaziçi",
    "program": "bilgisayar",
})

# v0.6.0
client.search(SearchFilters(
    puan_turu="SAY",       # büyük harf — "SAY"/"SÖZ"/"EA"/"DİL"/"TYT"
    universite="boğaziçi", # akıllı (fuzzy) — opsiyonel
    program="bilgisayar",
))
```

Akıllı (string) ve ID alanları aynı anda verilemez:

```python
SearchFilters(universite="boğaziçi", universite_id=[173500])  # ValueError
```

### 6. HTTP istemci

- `httpx` kalıyor; `urllib3` ve `beautifulsoup4` bağımlılıkları **kaldırıldı**.
- `verify_ssl` artık **default `True`**. (v0.x hardcoded `False` kullanıyordu.) Geçici geri-uyumluluk: `YOKATLAS_VERIFY_SSL=false` env var.

### 7. Python sürümü

- **Minimum Python ≥ 3.10**. (v0.x ≥3.9'du.)

## Önce ve sonra örnekleri

### Örnek 1 — Üniversite + program araması

```python
# v0.x
from yokatlas_py import search_lisans_programs

results = search_lisans_programs({
    "puan_turu": "say",
    "universite": "boğaziçi",
    "program": "bilgisayar",
}, smart_search=True)
for r in results:
    print(r["universite"], r["program"], r["taban"])

# v0.6.0
from yokatlas_py import YokAtlasClient, SearchFilters

with YokAtlasClient() as client:
    page = client.search(SearchFilters(
        puan_turu="SAY",
        universite="boğaziçi",
        program="bilgisayar",
    ))
    for prog in page.content:
        print(prog.universite_adi, prog.birim_adi, prog.current.min_puan)
```

### Örnek 2 — Tek programın detayı

```python
# v0.x
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

atlas = YOKATLASLisansAtlasi({"yop_kodu": "102210277", "year": 2024})
detail = asyncio.run(atlas.fetch_all_details())
# detail["girdi_gostergeleri"]["genel_bilgiler"]...
# detail["surec_ve_cikti_gostergeleri"]["cinsiyet_dagilimi"]  # ARTIK YOK

# v0.6.0
from yokatlas_py import YokAtlasClient

with YokAtlasClient() as client:
    prog = client.get_program(102210277)
    if prog:
        print(prog.universite_adi, prog.birim_adi)
        print("Mevcut yıl:", prog.current.min_puan, prog.current.basari_sirasi)
        for stats in prog.history:
            print(stats.year, stats.min_puan, stats.basari_sirasi)
```

### Örnek 3 — Async kullanım

```python
# v0.x
import asyncio
from yokatlas_py import YOKATLASOnlisansAtlasi
async def f():
    atlas = YOKATLASOnlisansAtlasi({"yop_kodu": "...", "year": 2024})
    return await atlas.fetch_all_details()
asyncio.run(f())

# v0.6.0
import asyncio
from yokatlas_py import AsyncYokAtlasClient, SearchFilters
async def f():
    async with AsyncYokAtlasClient() as client:
        page = await client.search(SearchFilters(birim_turu_id=47))
        return page.content
asyncio.run(f())
```

## Migration kontrol listesi

- [ ] `YOKATLASLisansAtlasi`, `YOKATLASOnlisansAtlasi`, `YOKATLASLisansTercihSihirbazi`, `YOKATLASOnlisansTercihSihirbazi` → `YokAtlasClient` veya `AsyncYokAtlasClient`
- [ ] `search_lisans_programs` / `search_onlisans_programs` → tek `search_programs` (gerekirse `birim_turu_id` filtresi)
- [ ] `year` parametresi kullanan tüm yerler → `prog.current` / `prog.history` üzerinden 4 yıl
- [ ] Atlas detay alt-kategorilerine bağımlı kod → mevcut `Program` alanlarına geçiş veya kaldırma
- [ ] `puan_turu` → büyük harfli ENUM (`SAY`/`SÖZ`/`EA`/`DİL`/`TYT`)
- [ ] Python 3.10+ ortam kontrolü
