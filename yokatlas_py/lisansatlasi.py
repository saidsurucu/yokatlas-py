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
    fetch_yatay_gecis_bilgileri,
)


class YOKATLASLisansAtlasi:
    def __init__(self, params, keys="all"):
        self.program_id = params.get("program_id")
        self.year = params.get("year", 2025)
        self.keys = keys

    async def fetch_all_details(self):
        try:
            tasks = []
            task_keys = []

            # Define the possible fetchers and their corresponding keys
            fetchers = {
                "sehir_ve_cografi_bolge_dagilimi": fetch_sehir_ve_cografi_bolge_dagilimi,
                "genel_bilgiler": fetch_genel_bilgiler,
                "kontenjan_yerlesme": fetch_kontenjan_yerlesme,
                "cinsiyet_dagilimi": fetch_cinsiyet_dagilimi,
                "yerlesen_il_dagilimi": fetch_yerlesen_il_dagilimi,
                "ogrenim_durumu": fetch_ogrenim_durumu,
                "mezuniyet_yili_dagilimi": fetch_mezuniyet_yili_dagilimi,
                "lise_alani_dagilimi": fetch_lise_alani_dagilimi,
                "lise_grubu_ve_tipi_dagilimi": fetch_lise_grubu_ve_tipi_dagilimi,
                "lise_bazinda_yerlesen_dagilimi": fetch_lise_bazinda_yerlesen_dagilimi,
                "okul_birincisi_yerlesen": fetch_okul_birincisi_yerlesen,
                "taban_puan_ve_basari_sirasi_istatistikleri": fetch_taban_puan_ve_basari_sirasi_istatistikleri,
                "yerlesen_son_kisi_bilgileri": fetch_yerlesen_son_kisi_bilgileri,
                "yerlesen_ortalama_netler": fetch_yerlesen_ortalama_netler,
                "yerlesen_puan_bilgileri": fetch_yerlesen_puan_bilgileri,
                "yerlesen_basari_siralari": fetch_yerlesen_basari_siralari,
                "tercih_istatistikleri": fetch_tercih_istatistikleri,
                "yerlesen_tercih_istatistikleri": fetch_yerlesen_tercih_istatistikleri,
                "tercih_kullanma_oranlari": fetch_tercih_kullanma_oranlari,
                "tercih_edilen_universite_turleri": fetch_tercih_edilen_universite_turleri,
                "tercih_edilen_universiteler": fetch_tercih_edilen_universiteler,
                "tercih_edilen_iller": fetch_tercih_edilen_iller,
                "tercih_edilen_program_turleri": fetch_tercih_edilen_program_turleri,
                "tercih_edilen_programlar": fetch_tercih_edilen_programlar,
                "akademisyen_sayilari": fetch_akademisyen_sayilari,
                "kayitli_ogrenci_cinsiyet_dagilimi": fetch_kayitli_ogrenci_cinsiyet_dagilimi,
                "mezuniyet_yili_cinsiyet_dagilimi": fetch_mezuniyet_yili_cinsiyet_dagilimi,
                "degisim_programi_bilgileri": fetch_degisim_programi_bilgileri,
                "yatay_gecis_bilgileri": fetch_yatay_gecis_bilgileri,
            }

            if self.keys == "all":
                keys_to_fetch = fetchers.keys()
            else:
                keys_to_fetch = self.keys

            # Create tasks only for the selected keys
            for key in keys_to_fetch:
                if key in fetchers:
                    tasks.append(fetchers[key](self.program_id, self.year))
                    task_keys.append(key)

            # Use return_exceptions=True to handle individual fetcher failures gracefully
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results and separate successful results from errors
            results_dict = {}
            errors_dict = {}

            for i, (key, result) in enumerate(zip(task_keys, results)):
                if isinstance(result, Exception):
                    # Handle the error case
                    error_msg = str(result)
                    errors_dict[key] = {
                        "error": error_msg,
                        "error_type": type(result).__name__,
                    }
                    results_dict[key] = (
                        None  # Set to None so we can safely check for it
                    )
                else:
                    # Handle successful result
                    results_dict[key] = result

            # Helper function to safely get values with error handling
            def safe_get(key, default=None, nested_key=None):
                if key in errors_dict:
                    return {
                        "error": f"Failed to fetch {key}: {errors_dict[key]['error']}"
                    }

                result = results_dict.get(key, default)
                if result is None:
                    return default

                if nested_key:
                    return (
                        result.get(nested_key, default)
                        if isinstance(result, dict)
                        else default
                    )
                return result

            girdi_gostergeleri = {
                "genel_bilgiler": safe_get("genel_bilgiler"),
                "kontenjan_yerlesme": safe_get("kontenjan_yerlesme"),
                "cinsiyet_dagilimi": safe_get("cinsiyet_dagilimi"),
                "sehir_dagilimi": safe_get(
                    "sehir_ve_cografi_bolge_dagilimi", {}, "sehir_dagilimi"
                )
                or [],
                "cografi_bolge_dagilimi": safe_get(
                    "sehir_ve_cografi_bolge_dagilimi", {}, "cografi_bolge_dagilimi"
                )
                or [],
                "yerlesen_il_dagilimi": safe_get(
                    "yerlesen_il_dagilimi", {}, "il_dagilimi"
                )
                or [],
                "yerlesen_il_toplam": safe_get("yerlesen_il_dagilimi", {}, "toplam")
                or {},
                "ogrenim_durumu": safe_get("ogrenim_durumu", {}, "ogrenim_durumu")
                or [],
                "ogrenim_durumu_toplam": safe_get("ogrenim_durumu", {}, "toplam") or {},
                "mezuniyet_yili_dagilimi": safe_get(
                    "mezuniyet_yili_dagilimi", {}, "mezuniyet_yili_dagilimi"
                )
                or [],
                "mezuniyet_yili_toplam": safe_get(
                    "mezuniyet_yili_dagilimi", {}, "toplam"
                )
                or {},
                "lise_alani_dagilimi": safe_get(
                    "lise_alani_dagilimi", {}, "lise_alani_dagilimi"
                )
                or [],
                "lise_alani_toplam": safe_get("lise_alani_dagilimi", {}, "toplam")
                or {},
                "lise_grubu_ve_tipi_dagilimi": safe_get("lise_grubu_ve_tipi_dagilimi"),
                "lise_bazinda_yerlesen_dagilimi": safe_get(
                    "lise_bazinda_yerlesen_dagilimi"
                ),
                "okul_birincisi_yerlesen": safe_get("okul_birincisi_yerlesen"),
                "taban_puan_ve_basari_sirasi_istatistikleri": safe_get(
                    "taban_puan_ve_basari_sirasi_istatistikleri"
                ),
                "yerlesen_son_kisi_bilgileri": safe_get("yerlesen_son_kisi_bilgileri"),
                "yerlesen_ortalama_netler": safe_get("yerlesen_ortalama_netler"),
                "yerlesen_puan_bilgileri": safe_get("yerlesen_puan_bilgileri"),
                "yerlesen_basari_siralari": safe_get("yerlesen_basari_siralari"),
                "tercih_istatistikleri": safe_get("tercih_istatistikleri"),
                "yerlesen_tercih_istatistikleri": safe_get(
                    "yerlesen_tercih_istatistikleri"
                ),
                "tercih_kullanma_oranlari": safe_get("tercih_kullanma_oranlari"),
                "tercih_edilen_universite_turleri": safe_get(
                    "tercih_edilen_universite_turleri"
                ),
                "tercih_edilen_universiteler": safe_get("tercih_edilen_universiteler"),
                "tercih_edilen_iller": safe_get("tercih_edilen_iller"),
                "tercih_edilen_program_turleri": safe_get(
                    "tercih_edilen_program_turleri"
                ),
                "tercih_edilen_programlar": safe_get("tercih_edilen_programlar"),
            }

            surec_ve_cikti_gostergeleri = {
                "akademisyen_sayilari": safe_get("akademisyen_sayilari"),
                "kayitli_ogrenci_cinsiyet_dagilimi": safe_get(
                    "kayitli_ogrenci_cinsiyet_dagilimi"
                ),
                "mezuniyet_yili_cinsiyet_dagilimi": safe_get(
                    "mezuniyet_yili_cinsiyet_dagilimi"
                ),
                "degisim_programi_bilgileri": safe_get("degisim_programi_bilgileri"),
                "yatay_gecis_bilgileri": safe_get("yatay_gecis_bilgileri"),
            }

            # Build the final result with error information
            result = {
                "girdi_gostergeleri": girdi_gostergeleri,
                "surec_ve_cikti_gostergeleri": surec_ve_cikti_gostergeleri,
            }

            # Add error summary if there were any errors
            if errors_dict:
                result["fetch_errors"] = errors_dict
                result["successful_fetchers"] = len(task_keys) - len(errors_dict)
                result["failed_fetchers"] = len(errors_dict)
                result["total_fetchers"] = len(task_keys)
            else:
                result["successful_fetchers"] = len(task_keys)
                result["failed_fetchers"] = 0
                result["total_fetchers"] = len(task_keys)

            return result

        except Exception as e:
            return {"error": f"Failed to fetch all details: {str(e)}"}
