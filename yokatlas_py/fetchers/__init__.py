"""
Refactored fetchers using BaseFetcher pattern.

This module contains the new class-based fetchers that eliminate
code duplication by inheriting from BaseFetcher.

Each fetcher file contains:
- A base class (e.g., CinsiyetDagilimiBaseFetcher) with common parsing logic
- Lisans-specific subclass (e.g., CinsiyetDagilimiLisansFetcher)
- Onlisans-specific subclass (e.g., CinsiyetDagilimiOnlisansFetcher)

The old function-based fetchers in lisans_fetchers/ and onlisans_fetchers/
are maintained as wrappers for backward compatibility.
"""

from .cinsiyet_dagilimi import (
    CinsiyetDagilimiBaseFetcher,
    CinsiyetDagilimiLisansFetcher,
    CinsiyetDagilimiOnlisansFetcher,
)
from .kontenjan_yerlesme import (
    KontenjanYerlesmeBaseFetcher,
    KontenjanYerlesmeLisansFetcher,
    KontenjanYerlesmeOnlisansFetcher,
)
from .ogrenim_durumu import (
    OgrenimDurumuBaseFetcher,
    OgrenimDurumuLisansFetcher,
    OgrenimDurumuOnlisansFetcher,
)
from .tercih_edilen_iller import (
    TercihEdilenIllerBaseFetcher,
    TercihEdilenIllerLisansFetcher,
    TercihEdilenIllerOnlisansFetcher,
)
from .mezuniyet_yili_dagilimi import (
    MezuniyetYiliDagilimiBaseFetcher,
    MezuniyetYiliDagilimiLisansFetcher,
    MezuniyetYiliDagilimiOnlisansFetcher,
)
from .lise_alani_dagilimi import (
    LiseAlaniDagilimiBaseFetcher,
    LiseAlaniDagilimiLisansFetcher,
    LiseAlaniDagilimiOnlisansFetcher,
)
from .okul_birincisi_yerlesen import (
    OkulBirincisiYerlesenBaseFetcher,
    OkulBirincisiYerlesenLisansFetcher,
    OkulBirincisiYerlesenOnlisansFetcher,
)
from .yerlesen_tercih_istatistikleri import (
    YerlesenTercihIstatistikleriBaseFetcher,
    YerlesenTercihIstatistikleriLisansFetcher,
    YerlesenTercihIstatistikleriOnlisansFetcher,
)
from .yerlesen_son_kisi_bilgileri import (
    YerlesenSonKisiBilgileriBaseFetcher,
    YerlesenSonKisiBilgileriLisansFetcher,
    YerlesenSonKisiBilgileriOnlisansFetcher,
)
from .tercih_kullanma_oranlari import (
    TercihKullanmaOranlariBaseFetcher,
    TercihKullanmaOranlariLisansFetcher,
    TercihKullanmaOranlariOnlisansFetcher,
)
from .yerlesen_il_dagilimi import (
    YerlesenIlDagilimiBaseFetcher,
    YerlesenIlDagilimiLisansFetcher,
    YerlesenIlDagilimiOnlisansFetcher,
)
from .yerlesen_ortalama_netler import (
    YerlesenOrtalamaNetlerBaseFetcher,
    YerlesenOrtalamaNetlerLisansFetcher,
    YerlesenOrtalamaNetlerOnlisansFetcher,
)
from .kayitli_ogrenci_cinsiyet_dagilimi import (
    KayitliOgrenciCinsiyetDagilimiBaseFetcher,
    KayitliOgrenciCinsiyetDagilimiLisansFetcher,
    KayitliOgrenciCinsiyetDagilimiOnlisansFetcher,
)
from .mezuniyet_yili_cinsiyet_dagilimi import (
    MezuniyetYiliCinsiyetDagilimiBaseFetcher,
    MezuniyetYiliCinsiyetDagilimiLisansFetcher,
    MezuniyetYiliCinsiyetDagilimiOnlisansFetcher,
)
from .akademisyen_sayilari import (
    AkademisyenSayilariBaseFetcher,
    AkademisyenSayilariLisansFetcher,
    AkademisyenSayilariOnlisansFetcher,
)
from .degisim_programi_bilgileri import (
    DegisimProgramiBilgileriBaseFetcher,
    DegisimProgramiBilgileriLisansFetcher,
    DegisimProgramiBilgileriOnlisansFetcher,
)
from .yatay_gecis_bilgileri import (
    YatayGecisBilgileriBaseFetcher,
    YatayGecisBilgileriLisansFetcher,
    YatayGecisBilgileriOnlisansFetcher,
)
from .genel_bilgiler import (
    GenelBilgilerBaseFetcher,
    GenelBilgilerLisansFetcher,
    GenelBilgilerOnlisansFetcher,
)
from .tercih_istatistikleri import (
    TercihIstatistikleriBaseFetcher,
    TercihIstatistikleriLisansFetcher,
    TercihIstatistikleriOnlisansFetcher,
)
from .lise_grubu_ve_tipi_dagilimi import (
    LiseGrubuVeTipiDagilimiBaseFetcher,
    LiseGrubuVeTipiDagilimiLisansFetcher,
    LiseGrubuVeTipiDagilimiOnlisansFetcher,
)
from .lise_bazinda_yerlesen_dagilimi import (
    LiseBazindaYerlesenDagilimiBaseFetcher,
    LiseBazindaYerlesenDagilimiLisansFetcher,
    LiseBazindaYerlesenDagilimiOnlisansFetcher,
)
from .sehir_ve_cografi_bolge_dagilimi import (
    SehirVeCografiBolgeDagilimiBaseFetcher,
    SehirVeCografiBolgeDagilimiLisansFetcher,
    SehirVeCografiBolgeDagilimiOnlisansFetcher,
)
from .tercih_edilen_programlar import (
    TercihEdilenProgramlarBaseFetcher,
    TercihEdilenProgramlarLisansFetcher,
    TercihEdilenProgramlarOnlisansFetcher,
)
from .tercih_edilen_universiteler import (
    TercihEdilenUniversitelerBaseFetcher,
    TercihEdilenUniversitelerLisansFetcher,
    TercihEdilenUniversitelerOnlisansFetcher,
)
from .tercih_edilen_program_turleri import (
    TercihEdilenProgramTurleriBaseFetcher,
    TercihEdilenProgramTurleriLisansFetcher,
    TercihEdilenProgramTurleriOnlisansFetcher,
)
from .tercih_edilen_universite_turleri import (
    TercihEdilenUniversiteTurleriBaseFetcher,
    TercihEdilenUniversiteTurleriLisansFetcher,
    TercihEdilenUniversiteTurleriOnlisansFetcher,
)
from .taban_puan_ve_basari_sirasi_istatistikleri import (
    TabanPuanVeBasariSirasiIstatistikleriBaseFetcher,
    TabanPuanVeBasariSirasiIstatistikleriLisansFetcher,
    TabanPuanVeBasariSirasiIstatistikleriOnlisansFetcher,
)
from .yerlesen_basari_siralari import (
    YerlesenBasariSiralariBaseFetcher,
    YerlesenBasariSiralariLisansFetcher,
)
from .yerlesen_puan_bilgileri import (
    YerlesenPuanBilgileriBaseFetcher,
    YerlesenPuanBilgileriLisansFetcher,
)

__all__ = [
    # Cinsiyet Dagilimi
    "CinsiyetDagilimiBaseFetcher",
    "CinsiyetDagilimiLisansFetcher",
    "CinsiyetDagilimiOnlisansFetcher",
    # Kontenjan Yerlesme
    "KontenjanYerlesmeBaseFetcher",
    "KontenjanYerlesmeLisansFetcher",
    "KontenjanYerlesmeOnlisansFetcher",
    # Ogrenim Durumu
    "OgrenimDurumuBaseFetcher",
    "OgrenimDurumuLisansFetcher",
    "OgrenimDurumuOnlisansFetcher",
    # Tercih Edilen Iller
    "TercihEdilenIllerBaseFetcher",
    "TercihEdilenIllerLisansFetcher",
    "TercihEdilenIllerOnlisansFetcher",
    # Mezuniyet Yili Dagilimi
    "MezuniyetYiliDagilimiBaseFetcher",
    "MezuniyetYiliDagilimiLisansFetcher",
    "MezuniyetYiliDagilimiOnlisansFetcher",
    # Lise Alani Dagilimi
    "LiseAlaniDagilimiBaseFetcher",
    "LiseAlaniDagilimiLisansFetcher",
    "LiseAlaniDagilimiOnlisansFetcher",
    # Okul Birincisi Yerlesen
    "OkulBirincisiYerlesenBaseFetcher",
    "OkulBirincisiYerlesenLisansFetcher",
    "OkulBirincisiYerlesenOnlisansFetcher",
    # Yerlesen Tercih Istatistikleri
    "YerlesenTercihIstatistikleriBaseFetcher",
    "YerlesenTercihIstatistikleriLisansFetcher",
    "YerlesenTercihIstatistikleriOnlisansFetcher",
    # Yerlesen Son Kisi Bilgileri
    "YerlesenSonKisiBilgileriBaseFetcher",
    "YerlesenSonKisiBilgileriLisansFetcher",
    "YerlesenSonKisiBilgileriOnlisansFetcher",
    # Tercih Kullanma Oranlari
    "TercihKullanmaOranlariBaseFetcher",
    "TercihKullanmaOranlariLisansFetcher",
    "TercihKullanmaOranlariOnlisansFetcher",
    # Yerlesen Il Dagilimi
    "YerlesenIlDagilimiBaseFetcher",
    "YerlesenIlDagilimiLisansFetcher",
    "YerlesenIlDagilimiOnlisansFetcher",
    # Yerlesen Ortalama Netler
    "YerlesenOrtalamaNetlerBaseFetcher",
    "YerlesenOrtalamaNetlerLisansFetcher",
    "YerlesenOrtalamaNetlerOnlisansFetcher",
    # Kayitli Ogrenci Cinsiyet Dagilimi
    "KayitliOgrenciCinsiyetDagilimiBaseFetcher",
    "KayitliOgrenciCinsiyetDagilimiLisansFetcher",
    "KayitliOgrenciCinsiyetDagilimiOnlisansFetcher",
    # Mezuniyet Yili Cinsiyet Dagilimi
    "MezuniyetYiliCinsiyetDagilimiBaseFetcher",
    "MezuniyetYiliCinsiyetDagilimiLisansFetcher",
    "MezuniyetYiliCinsiyetDagilimiOnlisansFetcher",
    # Akademisyen Sayilari
    "AkademisyenSayilariBaseFetcher",
    "AkademisyenSayilariLisansFetcher",
    "AkademisyenSayilariOnlisansFetcher",
    # Degisim Programi Bilgileri
    "DegisimProgramiBilgileriBaseFetcher",
    "DegisimProgramiBilgileriLisansFetcher",
    "DegisimProgramiBilgileriOnlisansFetcher",
    # Yatay Gecis Bilgileri
    "YatayGecisBilgileriBaseFetcher",
    "YatayGecisBilgileriLisansFetcher",
    "YatayGecisBilgileriOnlisansFetcher",
    # Genel Bilgiler
    "GenelBilgilerBaseFetcher",
    "GenelBilgilerLisansFetcher",
    "GenelBilgilerOnlisansFetcher",
    # Tercih Istatistikleri
    "TercihIstatistikleriBaseFetcher",
    "TercihIstatistikleriLisansFetcher",
    "TercihIstatistikleriOnlisansFetcher",
    # Lise Grubu ve Tipi Dagilimi
    "LiseGrubuVeTipiDagilimiBaseFetcher",
    "LiseGrubuVeTipiDagilimiLisansFetcher",
    "LiseGrubuVeTipiDagilimiOnlisansFetcher",
    # Lise Bazinda Yerlesen Dagilimi
    "LiseBazindaYerlesenDagilimiBaseFetcher",
    "LiseBazindaYerlesenDagilimiLisansFetcher",
    "LiseBazindaYerlesenDagilimiOnlisansFetcher",
    # Sehir ve Cografi Bolge Dagilimi
    "SehirVeCografiBolgeDagilimiBaseFetcher",
    "SehirVeCografiBolgeDagilimiLisansFetcher",
    "SehirVeCografiBolgeDagilimiOnlisansFetcher",
    # Tercih Edilen Programlar
    "TercihEdilenProgramlarBaseFetcher",
    "TercihEdilenProgramlarLisansFetcher",
    "TercihEdilenProgramlarOnlisansFetcher",
    # Tercih Edilen Universiteler
    "TercihEdilenUniversitelerBaseFetcher",
    "TercihEdilenUniversitelerLisansFetcher",
    "TercihEdilenUniversitelerOnlisansFetcher",
    # Tercih Edilen Program Turleri
    "TercihEdilenProgramTurleriBaseFetcher",
    "TercihEdilenProgramTurleriLisansFetcher",
    "TercihEdilenProgramTurleriOnlisansFetcher",
    # Tercih Edilen Universite Turleri
    "TercihEdilenUniversiteTurleriBaseFetcher",
    "TercihEdilenUniversiteTurleriLisansFetcher",
    "TercihEdilenUniversiteTurleriOnlisansFetcher",
    # Taban Puan ve Basari Sirasi Istatistikleri
    "TabanPuanVeBasariSirasiIstatistikleriBaseFetcher",
    "TabanPuanVeBasariSirasiIstatistikleriLisansFetcher",
    "TabanPuanVeBasariSirasiIstatistikleriOnlisansFetcher",
    # Yerlesen Basari Siralari (Lisans only)
    "YerlesenBasariSiralariBaseFetcher",
    "YerlesenBasariSiralariLisansFetcher",
    # Yerlesen Puan Bilgileri (Lisans only)
    "YerlesenPuanBilgileriBaseFetcher",
    "YerlesenPuanBilgileriLisansFetcher",
]
