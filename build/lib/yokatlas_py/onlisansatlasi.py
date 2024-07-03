import asyncio
from onlisans_fetchers.genel_bilgiler import fetch_genel_bilgiler
from onlisans_fetchers.kontenjan_yerlesme import fetch_kontenjan_yerlesme
from onlisans_fetchers.cinsiyet_dagilimi import fetch_cinsiyet_dagilimi
from onlisans_fetchers.sehir_ve_cografi_bolge_dagilimi import fetch_sehir_ve_cografi_bolge_dagilimi
from onlisans_fetchers.yerlesen_il_dagilimi import fetch_yerlesen_il_dagilimi
from onlisans_fetchers.ogrenim_durumu import fetch_ogrenim_durumu
from onlisans_fetchers.mezuniyet_yili_dagilimi import fetch_mezuniyet_yili_dagilimi
from onlisans_fetchers.lise_alani_dagilimi import fetch_lise_alani_dagilimi
from onlisans_fetchers.lise_grubu_ve_tipi_dagilimi import fetch_lise_grubu_ve_tipi_dagilimi
from onlisans_fetchers.lise_bazinda_yerlesen_dagilimi import fetch_lise_bazinda_yerlesen_dagilimi
from onlisans_fetchers.okul_birincisi_yerlesen import fetch_okul_birincisi_yerlesen
from onlisans_fetchers.taban_puan_ve_basari_sirasi_istatistikleri import fetch_taban_puan_ve_basari_sirasi_istatistikleri
from onlisans_fetchers.yerlesen_son_kisi_bilgileri import fetch_yerlesen_son_kisi_bilgileri
from onlisans_fetchers.yerlesen_ortalama_netler import fetch_yerlesen_ortalama_netler
from onlisans_fetchers.tercih_istatistikleri import fetch_tercih_istatistikleri
from onlisans_fetchers.yerlesen_tercih_istatistikleri import fetch_yerlesen_tercih_istatistikleri
from onlisans_fetchers.tercih_kullanma_oranlari import fetch_tercih_kullanma_oranlari
from onlisans_fetchers.tercih_edilen_universite_turleri import fetch_tercih_edilen_universite_turleri
from onlisans_fetchers.tercih_edilen_universiteler import fetch_tercih_edilen_universiteler
from onlisans_fetchers.tercih_edilen_iller import fetch_tercih_edilen_iller
from onlisans_fetchers.tercih_edilen_program_turleri import fetch_tercih_edilen_program_turleri
from onlisans_fetchers.tercih_edilen_programlar import fetch_tercih_edilen_programlar
from onlisans_fetchers.akademisyen_sayilari import fetch_akademisyen_sayilari
from onlisans_fetchers.kayitli_ogrenci_cinsiyet_dagilimi import fetch_kayitli_ogrenci_cinsiyet_dagilimi
from onlisans_fetchers.mezuniyet_yili_cinsiyet_dagilimi import fetch_mezuniyet_yili_cinsiyet_dagilimi
from onlisans_fetchers.degisim_programi_bilgileri import fetch_degisim_programi_bilgileri
from onlisans_fetchers.yatay_gecis_bilgileri import fetch_yatay_gecis_bilgileri

class YOKATLASOnlisansAtlasi:
    def __init__(self, params, keys='all'):
        self.program_id = params.get('program_id')
        self.year = params.get('year', 2023)
        self.keys = keys

    async def fetch_all_details(self):
        try:
            tasks = []

            # Define the possible fetchers and their corresponding keys
            fetchers = {
                'sehir_ve_cografi_bolge_dagilimi': fetch_sehir_ve_cografi_bolge_dagilimi,
                'genel_bilgiler': fetch_genel_bilgiler,
                'kontenjan_yerlesme': fetch_kontenjan_yerlesme,
                'cinsiyet_dagilimi': fetch_cinsiyet_dagilimi,
                'yerlesen_il_dagilimi': fetch_yerlesen_il_dagilimi,
                'ogrenim_durumu': fetch_ogrenim_durumu,
                'mezuniyet_yili_dagilimi': fetch_mezuniyet_yili_dagilimi,
                'lise_alani_dagilimi': fetch_lise_alani_dagilimi,
                'lise_grubu_ve_tipi_dagilimi': fetch_lise_grubu_ve_tipi_dagilimi,
                'lise_bazinda_yerlesen_dagilimi': fetch_lise_bazinda_yerlesen_dagilimi,
                'okul_birincisi_yerlesen': fetch_okul_birincisi_yerlesen,
                'taban_puan_ve_basari_sirasi_istatistikleri': fetch_taban_puan_ve_basari_sirasi_istatistikleri,
                'yerlesen_son_kisi_bilgileri': fetch_yerlesen_son_kisi_bilgileri,
                'yerlesen_ortalama_netler': fetch_yerlesen_ortalama_netler,
                'tercih_istatistikleri': fetch_tercih_istatistikleri,
                'yerlesen_tercih_istatistikleri': fetch_yerlesen_tercih_istatistikleri,
                'tercih_kullanma_oranlari': fetch_tercih_kullanma_oranlari,
                'tercih_edilen_universite_turleri': fetch_tercih_edilen_universite_turleri,
                'tercih_edilen_universiteler': fetch_tercih_edilen_universiteler,
                'tercih_edilen_iller': fetch_tercih_edilen_iller,
                'tercih_edilen_program_turleri': fetch_tercih_edilen_program_turleri,
                'tercih_edilen_programlar': fetch_tercih_edilen_programlar,
                'akademisyen_sayilari': fetch_akademisyen_sayilari,
                'kayitli_ogrenci_cinsiyet_dagilimi': fetch_kayitli_ogrenci_cinsiyet_dagilimi,
                'mezuniyet_yili_cinsiyet_dagilimi': fetch_mezuniyet_yili_cinsiyet_dagilimi,
                'degisim_programi_bilgileri': fetch_degisim_programi_bilgileri,
                'yatay_gecis_bilgileri': fetch_yatay_gecis_bilgileri
            }

            if self.keys == 'all':
                keys_to_fetch = fetchers.keys()
            else:
                keys_to_fetch = self.keys

            # Create tasks only for the selected keys
            for key in keys_to_fetch:
                if key in fetchers:
                    tasks.append(fetchers[key](self.program_id, self.year))

            results = await asyncio.gather(*tasks)

            # Process results and ensure no hashable type errors
            results_dict = dict(zip(keys_to_fetch, results))

            girdi_gostergeleri = {
                'genel_bilgiler': results_dict.get('genel_bilgiler'),
                'kontenjan_yerlesme': results_dict.get('kontenjan_yerlesme'),
                'cinsiyet_dagilimi': results_dict.get('cinsiyet_dagilimi'),
                'sehir_dagilimi': results_dict.get('sehir_ve_cografi_bolge_dagilimi', {}).get('sehir_dagilimi', []),
                'cografi_bolge_dagilimi': results_dict.get('sehir_ve_cografi_bolge_dagilimi', {}).get('cografi_bolge_dagilimi', []),
                'yerlesen_il_dagilimi': results_dict.get('yerlesen_il_dagilimi', {}).get('il_dagilimi', []),
                'yerlesen_il_toplam': results_dict.get('yerlesen_il_dagilimi', {}).get('toplam', {}),
                'ogrenim_durumu': results_dict.get('ogrenim_durumu', {}).get('ogrenim_durumu', []),
                'ogrenim_durumu_toplam': results_dict.get('ogrenim_durumu', {}).get('toplam', {}),
                'mezuniyet_yili_dagilimi': results_dict.get('mezuniyet_yili_dagilimi', {}).get('mezuniyet_yili_dagilimi', []),
                'mezuniyet_yili_toplam': results_dict.get('mezuniyet_yili_dagilimi', {}).get('toplam', {}),
                'lise_alani_dagilimi': results_dict.get('lise_alani_dagilimi', {}).get('lise_alani_dagilimi', []),
                'lise_alani_toplam': results_dict.get('lise_alani_dagilimi', {}).get('toplam', {}),
                'lise_grubu_ve_tipi_dagilimi': results_dict.get('lise_grubu_ve_tipi_dagilimi'),
                'lise_bazinda_yerlesen_dagilimi': results_dict.get('lise_bazinda_yerlesen_dagilimi'),
                'okul_birincisi_yerlesen': results_dict.get('okul_birincisi_yerlesen'),
                'taban_puan_ve_basari_sirasi_istatistikleri': results_dict.get('taban_puan_ve_basari_sirasi_istatistikleri'),
                'yerlesen_son_kisi_bilgileri': results_dict.get('yerlesen_son_kisi_bilgileri'),
                'yerlesen_ortalama_netler': results_dict.get('yerlesen_ortalama_netler'),
                'tercih_istatistikleri': results_dict.get('tercih_istatistikleri'),
                'yerlesen_tercih_istatistikleri': results_dict.get('yerlesen_tercih_istatistikleri'),
                'tercih_kullanma_oranlari': results_dict.get('tercih_kullanma_oranlari'),
                'tercih_edilen_universite_turleri': results_dict.get('tercih_edilen_universite_turleri'),
                'tercih_edilen_universiteler': results_dict.get('tercih_edilen_universiteler'),
                'tercih_edilen_iller': results_dict.get('tercih_edilen_iller'),
                'tercih_edilen_program_turleri': results_dict.get('tercih_edilen_program_turleri'),
                'tercih_edilen_programlar': results_dict.get('tercih_edilen_programlar')
            }

            surec_ve_cikti_gostergeleri = {
                'akademisyen_sayilari': results_dict.get('akademisyen_sayilari'),
                'kayitli_ogrenci_cinsiyet_dagilimi': results_dict.get('kayitli_ogrenci_cinsiyet_dagilimi'),
                'mezuniyet_yili_cinsiyet_dagilimi': results_dict.get('mezuniyet_yili_cinsiyet_dagilimi'),
                'degisim_programi_bilgileri': results_dict.get('degisim_programi_bilgileri'),
                'yatay_gecis_bilgileri': results_dict.get('yatay_gecis_bilgileri')
            }

            return {
                'girdi_gostergeleri': girdi_gostergeleri,
                'surec_ve_cikti_gostergeleri': surec_ve_cikti_gostergeleri
            }
        except Exception as e:
            return {"error": f"Failed to fetch all details: {str(e)}"}
