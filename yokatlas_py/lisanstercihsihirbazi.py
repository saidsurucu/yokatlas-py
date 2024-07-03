import requests
from urllib.parse import urlencode
from utils import load_column_data, parse_lisans_results
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YOKATLASLisansTercihSihirbazi:
    def __init__(self, params):
        self.column_vars = {
            "yop_kodu": 1, "uni_adi": 2, "program_adi": 4,
            "sehir_adi": 6, "universite_turu": 7, "ucret_burs": 8,
            "ogretim_turu": 9, "doluluk": 14,
        }

        self.defaults = {
            "draw": 1, "start": 0, "length": 100, "search[value]": "",
            "search[regex]": False, "puan_turu": "dil",
            "ust_bs": 0, "alt_bs": 3000000, "yeniler": 1
        }

        self.columns = load_column_data()
        self._set_columns(params)

    def _set_columns(self, params):
        for key in self.column_vars:
            if key in params:
                self.columns[f"columns[{self.column_vars[key]}][search][value]"] = params[key]

        for key, value in self.defaults.items():
            if key not in params:
                self.columns[key] = value
            elif key == "puan_turu":
                self.columns[key] = params[key] if params[key] in ["dil", "ea", "söz", "say"] else value
            elif key == "search":
                self.columns["search[value]"] = params.get(key, "")
                self.columns["search[regex]"] = False
            else:
                self.columns[key] = params[key]

        page = params.get('page', 1)
        self.columns['start'] = (page - 1) * self.columns['length']

    def search(self):
        payload = urlencode(self.columns)
        print("Payload:", payload)  # Print the payload to the console

        response = requests.post(
            "https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t4.php",
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
            verify=False
        )
        print(response.text)
        if response.status_code == 200:
            return parse_lisans_results(response.json())
        else:
            return {"error": f"Failed to fetch data from YOKATLAS API. Status code: {response.status_code}"}
