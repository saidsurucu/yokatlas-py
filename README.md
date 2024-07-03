
# YOKATLAS-py

A Python wrapper for YOKATLAS API.


## Installation | Kurulum

You can install the package using pip:

Paketi pip kullanarak yükleyebilirsiniz:

```sh
pip install yokatlas-py
```

## How to | Kullanım

Ayrıntılı kullanım dokümantasyonu yazılacak.
Detailed documentation wil be added.


```python
from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi
import asyncio



async def example_yokatlas_onlisansatlasi():
    onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': '203550463', 'year': 2023})
    result = await onlisans_atlasi.fetch_all_details()
    print("YOKATLAS Onlisans Atlasi Result:", result)

asyncio.run(example_yokatlas_onlisansatlasi())


async def example_yokatlas_lisansatlasi():
    lisans_atlasi = YOKATLASLisansAtlasi({'program_id': '104111719', 'year': 2023})
    result = await lisans_atlasi.fetch_all_details()
    print("YOKATLAS lisans Atlasi Result:", result)

asyncio.run(example_yokatlas_lisansatlasi())

def example_yokatlas_lisanstercihsihirbazi():
    params = {
        'yop_kodu': '',
        'uni_adi': 'Boğaziçi',
        'program_adi': '',
        'sehir_adi': '',
        'universite_turu': '',
        'ucret_burs': '',
        'ogretim_turu': '',
        'doluluk': '',
        'puan_turu': 'say',
        'ust_bs': 0,
        'alt_bs': 3000000,
        'page': 1
    }
    lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
    result = lisans_tercih.search()
    print("YOKATLAS Lisans Tercih Sihirbazi Result:", result)

example_yokatlas_lisanstercihsihirbazi()


def example_yokatlas_onlisanstercihsihirbazi():
    params = {
        'yop_kodu': '',
        'uni_adi': 'İstanbul',
        'program_adi': '',
        'sehir_adi': '',
        'universite_turu': '',
        'ucret_burs': '',
        'ogretim_turu': '',
        'doluluk': '',
        'ust_puan': 500,
        'alt_puan': 150,
        'page': 1
    }
    onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
    result = onlisans_tercih.search()
    print("YOKATLAS Onlisans Tercih Sihirbazi Result:", result)

example_yokatlas_onlisanstercihsihirbazi()
```


## License | Lisans

This project is licensed under the MIT License - see the LICENSE file for details.

Bu proje MIT Lisansı ile lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.
