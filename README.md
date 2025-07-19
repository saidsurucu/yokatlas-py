
# YOKATLAS-py

A Python wrapper for YOKATLAS API.


## Installation | Kurulum

You can install the package using pip:

Paketi pip kullanarak yükleyebilirsiniz:

```sh
pip install yokatlas-py
```

## How to | Kullanım

### University Program Search | Üniversite Program Arama

The search functionality supports filtering by various criteria:

Arama fonksiyonu çeşitli kriterlere göre filtreleme destekler:

**Available Parameters | Kullanılabilir Parametreler:**
- `puan_turu`: Score type | Puan türü (`say`, `ea`, `söz`, `dil` for lisans; `tyt` for önlisans)
- `program`: Program name search | Program adı arama
- `universite`: University name search | Üniversite adı arama  
- `sehir`: City filter | Şehir filtresi
- `universite_turu`: University type | Üniversite türü (`Devlet`, `Vakıf`)
- `ucret`: Fee type | Ücret türü (`Burslu`, `Ücretli`) 
- `ogretim_turu`: Education type | Öğretim türü (`Örgün`, `İkinci Öğretim`)
- `length`: Results per page | Sayfa başına sonuç (default: 50)
- `page`: Page number | Sayfa numarası (default: 1)


```python
from yokatlas_py.lisansatlasi import YOKATLASLisansAtlasi
from yokatlas_py.lisanstercihsihirbazi import YOKATLASLisansTercihSihirbazi
from yokatlas_py.onlisansatlasi import YOKATLASOnlisansAtlasi
from yokatlas_py.onlisanstercihsihirbazi import YOKATLASOnlisansTercihSihirbazi
import asyncio



async def example_yokatlas_onlisansatlasi():
    onlisans_atlasi = YOKATLASOnlisansAtlasi({'program_id': '203550463', 'year': 2024})
    result = await onlisans_atlasi.fetch_all_details()
    print("YOKATLAS Onlisans Atlasi Result:", result)

asyncio.run(example_yokatlas_onlisansatlasi())


async def example_yokatlas_lisansatlasi():
    lisans_atlasi = YOKATLASLisansAtlasi({'program_id': '104111719', 'year': 2024})
    result = await lisans_atlasi.fetch_all_details()
    print("YOKATLAS lisans Atlasi Result:", result)

asyncio.run(example_yokatlas_lisansatlasi())

def example_yokatlas_lisanstercihsihirbazi():
    # Search for programs at state universities in Ankara
    params = {
        'puan_turu': 'say',          # Score type: say, ea, söz, dil
        'sehir': 'ANKARA',           # Filter by city
        'universite_turu': 'Devlet', # State universities only
        'length': 5                  # Results per page
    }
    lisans_tercih = YOKATLASLisansTercihSihirbazi(params)
    result = lisans_tercih.search()
    print("YOKATLAS Lisans Tercih Sihirbazi Result:", result)

example_yokatlas_lisanstercihsihirbazi()


def example_yokatlas_onlisanstercihsihirbazi():
    # Search for programs in Istanbul
    params = {
        'puan_turu': 'tyt',         # Score type for associate degrees
        'sehir': 'İSTANBUL',        # City filter
        'universite_turu': 'Devlet', # State universities
        'length': 10                # Results per page
    }
    onlisans_tercih = YOKATLASOnlisansTercihSihirbazi(params)
    result = onlisans_tercih.search()
    print("YOKATLAS Onlisans Tercih Sihirbazi Result:", result)

example_yokatlas_onlisanstercihsihirbazi()
```


## License | Lisans

This project is licensed under the MIT License - see the LICENSE file for details.

Bu proje MIT Lisansı ile lisanslanmıştır - detaylar için LICENSE dosyasına bakınız.
