# yokatlas-py

YÖK Atlas tercih kılavuzu JSON API'si için modern, tip güvenli Python istemcisi.

[![PyPI version](https://badge.fury.io/py/yokatlas-py.svg)](https://badge.fury.io/py/yokatlas-py)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

[English README](README_EN.md) · [API Referansı](API.md) · [Migration Rehberi](MIGRATION.md)

> ⚠️ **v1.0.0 büyük değişiklik içerir.** YÖK Atlas 2025'te React tabanlı SPA'ya geçti ve eski HTML scraping endpoint'leri kapandı. v1.0.0, yeni JSON API'ye karşı sıfırdan yazıldı. v0.x kullanıcıları için [MIGRATION.md](MIGRATION.md) dosyasına bakın.

## Özellikler

- **Tek istemci**: `YokAtlasClient` (sync) ve `AsyncYokAtlasClient` (async) — aynı arayüz.
- **Tek seferde 4 yıllık veri**: Her program, mevcut yıl + 3 önceki yılın taban puanı, başarı sırası, kontenjan/yerleşen sayıları, akademik kadro bilgileri ile döner.
- **Akıllı arama**: `universite="boğaziçi"`, `program="bilgisayar"`, `il="ankara"` gibi serbest yazımlar fuzzy match ile ID'ye dönüşür (Türkçe karakter normalizasyonu dahil).
- **Pydantic v2 modeller**: Tam tip güvenliği, IDE auto-complete, runtime doğrulama.
- **Sıfır HTML parsing**: Tüm veri JSON, `beautifulsoup4` bağımlılığı yok.

## Kurulum

```bash
pip install yokatlas-py
# veya
uv add yokatlas-py
```

Python ≥3.10 gerekir.

## Hızlı başlangıç

```python
from yokatlas_py import YokAtlasClient, SearchFilters

with YokAtlasClient() as client:
    # Boğaziçi'nde sayısal tüm programlar
    page = client.search(
        SearchFilters(puan_turu="SAY", universite="boğaziçi"),
        size=20,
    )
    print(f"Toplam: {page.total_elements}")

    for prog in page.content:
        print(
            f"{prog.universite_adi} — {prog.birim_adi} | "
            f"{prog.current.min_puan} ({prog.current.basari_sirasi})"
        )

    # Tek bir program (kilavuz kodu ile)
    prog = client.get_program(102210277)
    if prog:
        for stats in prog.all_years:
            print(f"{stats.year}: {stats.min_puan} / {stats.basari_sirasi}")
```

### Async kullanım

```python
import asyncio
from yokatlas_py import AsyncYokAtlasClient, SearchFilters

async def main() -> None:
    async with AsyncYokAtlasClient() as client:
        page = await client.search(SearchFilters(il="ankara", program="tıp"))
        for prog in page.content:
            print(prog.universite_adi, prog.current.min_puan)

asyncio.run(main())
```

### Modül seviyesinde kısayollar

Tek seferlik scriptler için singleton bir istemci üzerinden çalışan kısayollar:

```python
from yokatlas_py import search_programs, get_program, list_universities

page = search_programs({"puan_turu": "EA", "universite": "boğaziçi"}, size=10)
prog = get_program(102210277)
unis = list_universities()  # 221 üniversite
```

## Filtreler

| Alan | Tip | Açıklama |
|---|---|---|
| `puan_turu` | `"SAY" \| "SÖZ" \| "EA" \| "DİL" \| "TYT"` | Puan türü |
| `universite` / `universite_id` | `str \| list[str]` / `list[int]` | Üniversite (akıllı veya ID) |
| `program` / `birim_grup_id` | `str \| list[str]` / `list[int]` | Program grubu |
| `il` / `il_kodu` | `str \| list[str]` / `list[int]` | İl |
| `birim_turu_id` | `int` | 46 = LİSANS, 47 = ÖNLİSANS |
| `universite_turu` | `"DEVLET" \| "VAKIF"` | Üniversite türü |
| `burs_orani_id` | `int` | 0 = Ücretsiz / Burslu |
| `ogrenim_turu_id` | `int` | Örgün/İkinci öğretim |
| `kilavuzKodu` | `int` | Tek programa filtre |
| `min_basari_sirasi` / `max_basari_sirasi` | `int` | Başarı sırası aralığı |

> Akıllı (string) alanlar ile ID alanları aynı anda verilemez — biri seçilir.

## Yapı

Bir `Program` 4 yıllık veri taşır:

```python
prog.current        # YearlyStats: en güncel yıl (2025)
prog.history        # list[YearlyStats]: 3 önceki yıl (2024, 2023, 2022)
prog.all_years      # 4 yılın tümü (yeni → eski)
```

`YearlyStats` alanları: `year, kontenjan, yerlesen, kontenjan_obs, kontenjan_y34, prof, doc, dou, ogr_gor, ar_gor, kpss1, kpss2, min_puan, basari_sirasi`.

## Yapılandırma

`YOKATLAS_*` env var'ları ile veya `Settings` ile:

```python
from yokatlas_py import Settings, YokAtlasClient

settings = Settings(timeout=60.0, lookup_cache_ttl=600)
client = YokAtlasClient(settings=settings)
```

| Env var | Default | Açıklama |
|---|---|---|
| `YOKATLAS_BASE_URL` | `https://yokatlas.yok.gov.tr` | API kökü |
| `YOKATLAS_TIMEOUT` | `30.0` | HTTP timeout (sn) |
| `YOKATLAS_VERIFY_SSL` | `true` | TLS sertifika doğrulaması |
| `YOKATLAS_MAX_RETRIES` | `3` | HTTP retry sayısı |
| `YOKATLAS_LOOKUP_CACHE_TTL` | `3600` | Üniversite/program/il cache TTL (sn) |

## Önemli kısıt

YÖK Atlas yeni API'sinde **alt-kategori detayları kaldırıldı**: cinsiyet/lise alanı/yerleşen il dağılımı, tercih edilen üniversiteler/programlar, akademisyen ünvan dağılımı, yatay geçiş, mezuniyet yılı dağılımı vb. v0.x'te dönen ~25 alt kategori artık API'de yok. v1.0.0 sadece resmî API'nin sunduğunu döner.

## Geliştirme

```bash
uv sync
uv run pytest                # tüm testler (mock)
uv run pytest -m integration # gerçek API (opt-in)
uv run mypy yokatlas_py/
```

## Lisans

MIT
