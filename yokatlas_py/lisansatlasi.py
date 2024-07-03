import asyncio
from .lisans_fetchers import (
    fetch_genel_bilgiler,
    fetch_kontenjan_yerlesme,
    fetch_cinsiyet_dagilimi,
    fetch_sehir_ve_cografi_bolge_dagilimi,
    fetch_yerlesen_il_dagilimi,
    fetch_ogrenim_durumu,
    fetch_mezuniyet_yili_dagilimi,
    fetch_lise_alani_dagilimi,
    fetch_lise_grubu_ve_tipi_dagilimi,
    fetch_lise_bazinda_yerlesen_dagilimi,
    fetch_okul_birincisi_yerlesen,
    fetch_taban_puan_ve_basari_sirasi_istatistikleri,
    fetch_yerlesen_son_kisi_bilgileri,
    fetch_yerlesen_ortalama_netler,
    fetch_yerlesen_puan_bilgileri,
    fetch_yerlesen_basari_siralari,
    fetch_tercih_istatistikleri,
    fetch_yerlesen_tercih_istatistikleri,
    fetch_tercih_kullanma_oranlari,
    fetch_tercih_edilen_universite_turleri,
    fetch_tercih_edilen_universiteler,
    fetch_tercih_edilen_iller,
    fetch_tercih_edilen_program_turleri,
    fetch_tercih_edilen_programlar,
    fetch_akademisyen_sayilari,
    fetch_kayitli_ogrenci_cinsiyet_dagilimi,
    fetch_mezuniyet_yili_cinsiyet_dagilimi,
    fetch_degisim_programi_bilgileri,
    fetch_yatay_gecis_bilgileri
)


class YOKATLASLisansAtlasi:
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
                'yerlesen_puan_bilgileri': fetch_yerlesen_puan_bilgileri,
                'yerlesen_basari_siralari': fetch_yerlesen_basari_siralari,
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
                'yerlesen_puan_bilgileri': results_dict.get('yerlesen_puan_bilgileri'),
                'yerlesen_basari_siralari': results_dict.get('yerlesen_basari_siralari'),
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
