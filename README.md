# YOKATLAS-py

YOKATLAS API için modern, tip güvenli Python kütüphanesi.

[![PyPI version](https://badge.fury.io/py/yokatlas-py.svg)](https://badge.fury.io/py/yokatlas-py)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/yokatlas-py)](https://pepy.tech/project/yokatlas-py)

> **[English Version](README_EN.md)**

---

## İçindekiler

- [Kurulum](#kurulum)
- [Hızlı Başlangıç](#hızlı-başlangıç)
- [Desteklenen Veriler](#desteklenen-veriler)
- [Arama API](#arama-api)
- [Atlas API](#atlas-api)
- [Hata Yönetimi](#hata-yönetimi)
- [Hız Sınırları](#hız-sınırları)
- [Test](#test)
- [Katkıda Bulunma](#katkıda-bulunma)
- [Lisans](#lisans)

---

## Kurulum

**Gereksinimler:** Python 3.9+

```bash
# pip ile
pip install yokatlas-py

# uv ile (önerilen)
uv add yokatlas-py
```

---

## Hızlı Başlangıç

```python
from yokatlas_py import search_lisans_programs, YOKATLASLisansAtlasi
import asyncio

# 1. Program arama (senkron)
results = search_lisans_programs({
    "uni_adi": "boğaziçi",       # Bulanık eşleştirme!
    "program_adi": "bilgisayar"
})
print(f"{len(results)} program bulundu")

# 2. Detaylı program verisi (asenkron)
async def detay_getir():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    return await atlas.fetch_all_details()

detaylar = asyncio.run(detay_getir())
print(detaylar['genel_bilgiler'])
```

---

## Desteklenen Veriler

### Desteklenen Yıllar

| Program Türü | Yıllar |
|--------------|--------|
| Lisans | 2021, 2022, 2023, 2024 |
| Önlisans | 2023, 2024 |

### Lisans Veri Tipleri (12)

| Anahtar | Açıklama |
|---------|----------|
| `genel_bilgiler` | Genel bilgi, kontenjan, puan bilgileri |
| `cinsiyet_dagilimi` | Cinsiyet dağılımı |
| `cografi_bolge_dagilimi` | Coğrafi bölge dağılımı |
| `lise_grubu_dagilimi` | Lise grubu dağılımı |
| `lise_bazinda_yerlesen` | Lise bazında yerleşen sayıları |
| `tercih_istatistikleri` | Tercih istatistikleri |
| `tercih_edilen_programlar` | Tercih edilen diğer programlar |
| `tercih_edilen_universiteler` | Tercih edilen üniversiteler |
| `tercih_edilen_program_turleri` | Tercih edilen program türleri |
| `tercih_edilen_universite_turleri` | Tercih edilen üniversite türleri |
| `taban_puan_basari_sirasi` | Taban puan ve başarı sırası istatistikleri |
| `yerlesen_puan_bilgileri` | Yerleşenlerin puan bilgileri |

### Önlisans Veri Tipleri (10)

Lisans ile aynı, sadece `yerlesen_basari_siralari` ve `yerlesen_puan_bilgileri` lisansa özeldir.

---

## Arama API

### Akıllı Arama (Bulanık Eşleştirme)

```python
from yokatlas_py import search_lisans_programs, search_onlisans_programs, search_programs

# Bulanık üniversite eşleştirme - hepsi "BOĞAZİÇİ ÜNİVERSİTESİ"ni bulur
search_lisans_programs({"uni_adi": "boğaziçi"})
search_lisans_programs({"uni_adi": "bogazici"})  # Türkçe karakter olmadan
search_lisans_programs({"uni_adi": "boun"})      # Kısaltma

# Desteklenen kısaltmalar:
# "odtü", "odtu", "metu" → ORTA DOĞU TEKNİK ÜNİVERSİTESİ
# "itü", "itu" → İSTANBUL TEKNİK ÜNİVERSİTESİ
# "hacettepe" → HACETTEPE ÜNİVERSİTESİ

# Kısmi program adı eşleştirme
results = search_lisans_programs({"program_adi": "bilgisayar"})
# Bulur: Bilgisayar Mühendisliği, Bilgisayar Bilimleri, vb.

# Hem lisans hem önlisans arama
tum_sonuclar = search_programs({"uni_adi": "anadolu"})
print(f"Lisans: {len(tum_sonuclar['lisans'])}")
print(f"Önlisans: {len(tum_sonuclar['onlisans'])}")
```

### Geleneksel Arama

```python
from yokatlas_py import YOKATLASLisansTercihSihirbazi, YOKATLASOnlisansTercihSihirbazi

# Lisans arama
lisans_arama = YOKATLASLisansTercihSihirbazi({
    'puan_turu': 'say',          # say, ea, söz, dil
    'sehir': 'ANKARA',
    'universite_turu': 'Devlet',
    'ust_bs': 50000,             # Maksimum başarı sırası
    'length': 10
})
sonuclar = lisans_arama.search()

# Önlisans arama
onlisans_arama = YOKATLASOnlisansTercihSihirbazi({
    'puan_turu': 'tyt',
    'sehir': 'İSTANBUL',
    'length': 10
})
sonuclar = onlisans_arama.search()
```

---

## Atlas API

### Tüm Program Detaylarını Getirme

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi, YOKATLASOnlisansAtlasi

async def program_verisi_getir():
    # Lisans
    lisans = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024
    })
    veri = await lisans.fetch_all_details()
    return veri

sonuc = asyncio.run(program_verisi_getir())
```

### Örnek Çıktı

```python
# sonuc['genel_bilgiler']
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

### Sadece Belirli Verileri Getirme

```python
async def belirli_veri_getir():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '103910743',
        'year': 2024,
        'keys': ['genel_bilgiler', 'cinsiyet_dagilimi']  # Sadece bunlar
    })
    return await atlas.fetch_all_details()
```

---

## Hata Yönetimi

```python
import asyncio
from yokatlas_py import YOKATLASLisansAtlasi

async def guvenli_getir():
    atlas = YOKATLASLisansAtlasi({
        'program_id': '999999999',  # Geçersiz ID
        'year': 2024
    })
    sonuc = await atlas.fetch_all_details()

    # Her veri tipi için hata kontrolü
    for anahtar, deger in sonuc.items():
        if isinstance(deger, dict) and 'error' in deger:
            print(f"❌ {anahtar}: {deger['error']}")
        else:
            print(f"✅ {anahtar}: OK")

asyncio.run(guvenli_getir())
```

### Sık Karşılaşılan Hatalar

| Hata | Sebep | Çözüm |
|------|-------|-------|
| `HTTP 418` | Hız sınırı | Bekleyip tekrar deneyin |
| `HTTP 404` | Geçersiz program ID veya yıl | program_id'yi doğrulayın |
| `Required tables not found` | Bu program için veri yok | Normal - bazı programlarda belirli veriler olmayabilir |

---

## Hız Sınırları

YOKATLAS API'nin hız sınırları vardır. Öneriler:

- İstekler arası gecikme ekleyin: `await asyncio.sleep(0.5)`
- Bağlantı havuzu kullanın (`YOKATLASClient` ile otomatik)
- Sonuçları mümkünse önbelleğe alın
- Aynı endpoint'e paralel isteklerden kaçının

```python
import asyncio

async def birden_fazla_program_getir(program_idleri):
    sonuclar = {}
    for pid in program_idleri:
        atlas = YOKATLASLisansAtlasi({'program_id': pid, 'year': 2024})
        sonuclar[pid] = await atlas.fetch_all_details()
        await asyncio.sleep(0.5)  # Hız sınırı gecikmesi
    return sonuclar
```

---

## Test

```bash
# Unit testleri çalıştır
uv run pytest tests/ -v

# Coverage ile çalıştır
uv run pytest tests/ --cov=yokatlas_py

# Gerçek API testi (internet gerektirir)
uv run python -c "
from yokatlas_py import search_lisans_programs
sonuclar = search_lisans_programs({'uni_adi': 'boğaziçi', 'length': 3})
print(f'{len(sonuclar)} program bulundu')
"
```

---

## Katkıda Bulunma

Katkılarınızı bekliyoruz!

1. Repository'yi fork edin
2. Feature branch oluşturun: `git checkout -b feature/harika-ozellik`
3. Değişikliklerinizi yapın
4. Testleri çalıştırın: `uv run pytest tests/`
5. Commit edin: `git commit -m 'Harika özellik eklendi'`
6. Push edin: `git push origin feature/harika-ozellik`
7. Pull Request açın

---

## Lisans

MIT Lisansı - detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## Bağlantılar

- [PyPI Paketi](https://pypi.org/project/yokatlas-py/)
- [YOKATLAS Resmi](https://yokatlas.yok.gov.tr/)
- [Hata Bildirimi](https://github.com/your-username/yokatlas-py/issues)
