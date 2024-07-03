
# YOKATLAS-py

A Python wrapper for YOKATLAS API.


## Installation | Kurulum

You can install the package using pip:

Paketi pip kullanarak yükleyebilirsiniz:

```sh
pip install yokatlas-py
```

## Usage | Kullanım

### English

```python
from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi

# Example usage of YOKATLASLisansAtlasi
lisans_atlasi = YOKATLASLisansAtlasi({'program_id': '12345', 'year': 2023})
result = lisans_atlasi.fetch_all_details()

# Example usage of YOKATLASLisansTercihSihirbazi
lisans_tercih = YOKATLASLisansTercihSihirbazi({
    'yop_kodu': '001',
    'uni_adi': 'Example University',
    'program_adi': 'Computer Science',
    'sehir_adi': 'Ankara',
    'universite_turu': 'State',
    'ucret_burs': 'Full Scholarship',
    'ogretim_turu': 'Evening',
    'doluluk': 'Full',
    'puan_turu': 'say',
    'ust_bs': 100000,
    'alt_bs': 10000,
    'page': 1
})
result = lisans_tercih.search()

# Example usage of YOKATLASOnlisansAtlasi
onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': '67890', 'year': 2023})
result = onlisans_atlasi.fetch_all_details()

# Example usage of YOKATLASOnlisansTercihSihirbazi
onlisans_tercih = YOKATLASOnlisansTercihSihirbazi({
    'yop_kodu': '002',
    'uni_adi': 'Example University',
    'program_adi': 'Information Technology',
    'sehir_adi': 'Istanbul',
    'universite_turu': 'Private',
    'ucret_burs': 'Half Scholarship',
    'ogretim_turu': 'Daytime',
    'doluluk': '80%',
    'ust_puan': 400,
    'alt_puan': 150,
    'page': 1
})
result = onlisans_tercih.search()
```

### Türkçe

```python
from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi

# YOKATLASLisansAtlasi'nın örnek kullanımı
lisans_atlasi = YOKATLASLisansAtlasi({'program_id': '12345', 'year': 2023})
sonuc = lisans_atlasi.fetch_all_details()

# YOKATLASLisansTercihSihirbazi'nın örnek kullanımı
lisans_tercih = YOKATLASLisansTercihSihirbazi({
    'yop_kodu': '001',
    'uni_adi': 'Örnek Üniversite',
    'program_adi': 'Bilgisayar Mühendisliği',
    'sehir_adi': 'Ankara',
    'universite_turu': 'Devlet',
    'ucret_burs': 'Tam Burs',
    'ogretim_turu': 'İkinci Öğretim',
    'doluluk': 'Dolu',
    'puan_turu': 'say',
    'ust_bs': 100000,
    'alt_bs': 10000,
    'page': 1
})
sonuc = lisans_tercih.search()

# YOKATLASOnlisansAtlasi'nın örnek kullanımı
onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': '67890', 'year': 2023})
sonuc = onlisans_atlasi.fetch_all_details()

# YOKATLASOnlisansTercihSihirbazi'nın örnek kullanımı
onlisans_tercih = YOKATLASOnlisansTercihSihirbazi({
    'yop_kodu': '002',
    'uni_adi': 'Örnek Üniversite',
    'program_adi': 'Bilgi Teknolojileri',
    'sehir_adi': 'İstanbul',
    'universite_turu': 'Özel',
    'ucret_burs': 'Yarım Burs',
    'ogretim_turu': 'Gündüz',
    'doluluk': '80%',
    'ust_puan': 400,
    'alt_puan': 150,
    'page': 1
})
sonuc = onlisans_tercih.search()
```

## License | Lisans

This project is licensed under the MIT License - see the LICENSE file for details.

Bu proje MIT Lisansı ile lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.
