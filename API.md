# yokatlas-py API Referansı

`yokatlas-py` v1.0.0, YÖK Atlas tercih kılavuzu JSON API'si üzerine ince bir tip-güvenli istemcidir. Bu belge tüm public sınıfları, fonksiyonları ve modelleri kapsar.

## İçindekiler

1. [İstemciler](#istemciler)
2. [Modeller](#modeller)
3. [Filtreler](#filtreler)
4. [İstisnalar](#istisnalar)
5. [Yapılandırma](#yapılandırma)
6. [Modül seviyesinde kısayollar](#modül-seviyesinde-kısayollar)

---

## İstemciler

### `YokAtlasClient` (sync)

```python
from yokatlas_py import YokAtlasClient
```

#### `__init__(*, settings: Settings | None = None, http: HttpClient | None = None)`

Yeni bir istemci oluşturur. `settings` verilmezse default ayarlar (env var override'lı) kullanılır. `http` verilmezse kendi `httpx.Client`'ını yönetir ve `close()`'da kapatır.

#### `search(filters=None, *, page=0, size=20, sort_by="basariSirasi", direction="ASC", smart_search=True) -> SearchPage[Program]`

Arama yapar. `filters` `SearchFilters`, `dict` veya `None` olabilir. Akıllı string alanları (`universite`, `program`, `il`) `smart_search=True` iken çözülür.

#### `get_program(kilavuz_kodu: int | str) -> Program | None`

Tek bir programı ÖSYM kılavuz kodu ile döndürür. Bulunamazsa `None`. `kilavuz_kodu` int'e çevrilemiyorsa `ValueError`.

#### `list_universities() -> list[University]`
#### `list_program_groups() -> list[ProgramGroup]`
#### `list_cities() -> list[City]`

Lookup tablolarını döndürür. İlk çağrıda HTTP yapılır, sonrasında `lookup_cache_ttl` süresi boyunca cache'ten yanıtlanır.

#### `refresh_lookups() -> None`

Cache'i hemen geçersiz kılıp yeniden çeker.

#### `close()` / context manager

```python
with YokAtlasClient() as client:
    ...  # client otomatik kapanır
```

### `AsyncYokAtlasClient` (async)

`YokAtlasClient` ile birebir aynı yüzey. Tüm metotlar `async`. Kapama: `await client.aclose()` veya `async with`.

```python
from yokatlas_py import AsyncYokAtlasClient

async with AsyncYokAtlasClient() as client:
    page = await client.search(...)
    prog = await client.get_program(102210277)
```

Lookup verileri ilk çağrıda **paralel** çekilir (`asyncio.gather`).

---

## Modeller

### `Program`

YÖK Atlas search endpoint'inden dönen tek bir kayıt. Yıllık veriler (kontenjan, kadro, KPSS, taban puan, başarı sırası) `current` ve `history`'ye gruplandı.

| Alan | Tip | Açıklama |
|---|---|---|
| `kilavuz_kodu` | `int` | ÖSYM kılavuz kodu (9 hane) |
| `osym_kilavuz_id` | `int \| None` | ÖSYM iç ID |
| `universite_id` / `universite_adi` | `int / str` | Üniversite |
| `birim_id`, `birim_adi`, `birim_grup_id`, `birim_grup_adi` | — | Program / birim grubu |
| `birim_turu_adi` | `"LISANS" \| "ONLISANS"` | |
| `puan_turu` | `str` | SAY / SÖZ / EA / DİL / TYT |
| `universite_turu` | `"DEVLET" \| "VAKIF"` | |
| `burs_orani_id` / `burs_orani_adi` | `int \| None` / `str \| None` | Burs durumu |
| `ogrenim_turu_id` / `ogrenim_turu_adi` | — | Örgün vb. |
| `ogrenim_dili_id` / `ogrenim_dili_adi` | — | Türkçe / İngilizce vb. |
| `ogrenim_suresi` | `int \| None` | Yıl |
| `il_kodu` / `il_adi`, `ilce_kodu` / `ilce_adi` | — | Programın bulunduğu yer |
| `fymk_id` / `fymk_adi` | — | Fakülte / yüksekokul / meslek yüksekokulu |
| `current` | `YearlyStats` | En güncel yıl (örn. 2025) |
| `history` | `list[YearlyStats]` | 3 önceki yıl, yeni → eski |

**Property**: `prog.all_years -> list[YearlyStats]` — `[current, *history]`.

### `YearlyStats`

| Alan | Tip | Açıklama |
|---|---|---|
| `year` | `int` | İlgili yıl |
| `kontenjan` | `int \| None` | Genel kontenjan |
| `yerlesen` | `int \| None` | Genel kontenjandan yerleşen (raw API: `gkY`) |
| `kontenjan_obs`, `kontenjan_y34` | `int \| None` | OBS / 34 yaş üstü kontenjanı |
| `prof`, `doc`, `dou`, `ogr_gor`, `ar_gor` | `int \| None` | Akademik kadro sayıları |
| `kpss1`, `kpss2` | `float \| None` | KPSS başarı yüzdeleri |
| `min_puan` | `float \| None` | Taban puan |
| `basari_sirasi` | `int \| None` | Başarı sırası |

### `SearchPage[T]`

Spring `Page<T>` ile birebir. Alanlar: `content, total_elements, total_pages, size, number, first, last, number_of_elements, empty, yil`.

### `University`, `ProgramGroup`, `City`

Sırasıyla `(universite_id, universite_adi)`, `(birim_grup_id, birim_grup_adi, puan_turu)`, `(il_kodu, il_adi)`.

---

## Filtreler

### `SearchFilters`

Tüm alanlar opsiyoneldir; verilmeyenler API'a gönderilmez.

| Alan | Tip | Notlar |
|---|---|---|
| `puan_turu` | `"SAY" \| "SÖZ" \| "EA" \| "DİL" \| "TYT" \| None` | `"SOZ"` ve `"DIL"` otomatik normalize edilir |
| `universite_id` | `list[int] \| None` | Doğrudan ID |
| `birim_grup_id` | `list[int] \| None` | Doğrudan ID |
| `il_kodu` | `list[int] \| None` | Doğrudan ID |
| `birim_turu_id` | `int \| None` | 46 = LİSANS, 47 = ÖNLİSANS |
| `universite_turu` | `"DEVLET" \| "VAKIF" \| None` | |
| `burs_orani_id`, `ogrenim_turu_id` | `int \| None` | |
| `kilavuz_kodu` | `int \| None` | Tek programa filtre |
| `min_basari_sirasi`, `max_basari_sirasi` | `int \| None` | Aralık |
| **`universite`** | `str \| list[str] \| None` | Akıllı (fuzzy) — `universite_id` ile birlikte verilemez |
| **`program`** | `str \| list[str] \| None` | Akıllı — `birim_grup_id` ile birlikte verilemez |
| **`il`** | `str \| list[str] \| None` | Akıllı — `il_kodu` ile birlikte verilemez |

`extra="forbid"`: bilinmeyen alanlar `ValueError` üretir.

#### `to_payload() -> dict`

API'ye gönderilen camelCase payload'u üretir (smart alanlar düşer; sadece ID alanları kalır).

---

## İstisnalar

```python
from yokatlas_py import APIError, NotFoundError, RateLimitError, LookupError, YokAtlasError
```

| Sınıf | Tetiklenme |
|---|---|
| `YokAtlasError` | Tüm istisnaların kökü |
| `APIError(status_code, body)` | Beklenmeyen HTTP yanıtı |
| `NotFoundError` | 404 |
| `RateLimitError` | 418 / 429 |
| `LookupError(name, kind, suggestions)` | Smart search bir ismi ID'ye çeviremedi |

---

## Yapılandırma

### `Settings`

```python
from yokatlas_py import Settings
```

| Alan | Default | Env var |
|---|---|---|
| `base_url` | `https://yokatlas.yok.gov.tr` | `YOKATLAS_BASE_URL` |
| `timeout` | `30.0` | `YOKATLAS_TIMEOUT` |
| `verify_ssl` | `true` | `YOKATLAS_VERIFY_SSL` |
| `max_retries` | `3` | `YOKATLAS_MAX_RETRIES` |
| `user_agent` | `yokatlas-py/1.0` | `YOKATLAS_USER_AGENT` |
| `lookup_cache_ttl` | `3600` (sn) | `YOKATLAS_LOOKUP_CACHE_TTL` |

`settings` adında bir process-wide singleton da export edilir.

---

## Modül seviyesinde kısayollar

Tek seferlik scriptler için singleton bir `YokAtlasClient` üzerinden çalışan kısayollar. İstemci `atexit` ile kapatılır.

```python
from yokatlas_py import (
    search_programs, get_program,
    list_universities, list_program_groups, list_cities,
)

page = search_programs({"puan_turu": "SAY"}, size=10)
prog = get_program(102210277)
unis = list_universities()
progs = list_program_groups()
cities = list_cities()
```

> Production'da `with YokAtlasClient() as c: ...` kullanın — bağlantıların net kapanmasını garanti eder.

---

## Endpoint eşlemesi (referans)

Bu kütüphane sadece 4 resmi endpoint'i sarar:

| Endpoint | Metod | Kullanım |
|---|---|---|
| `/api/tercih-kilavuz/search` | POST | `search()`, `get_program()` |
| `/api/tercih-kilavuz/universiteler` | GET | `list_universities()` |
| `/api/tercih-kilavuz/universite-programlar` | GET | `list_program_groups()` |
| `/api/tercih-kilavuz/universite-iller` | GET | `list_cities()` |
