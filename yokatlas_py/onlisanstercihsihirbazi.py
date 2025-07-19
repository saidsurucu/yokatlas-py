import requests
from urllib.parse import urlencode
from .utils import load_column_data, parse_onlisans_results
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class YOKATLASOnlisansTercihSihirbazi:
    def __init__(self, params):
        self.params = params
        
        # Load base column structure from JSON
        self.columns = load_column_data()
        
        # Set default values and ordering
        self._set_defaults()
        
        # Apply user parameters
        self._apply_params(params)

    def _set_defaults(self):
        # Default values for main parameters
        defaults = {
            "draw": 2,
            "start": 0,
            "length": 50,
            "search[value]": "",
            "search[regex]": "false",
            "puan_turu": "tyt",
            "ust_puan": "",
            "alt_puan": "",
            "tip": "TYT",
            "yeniler": "1",
            "kilavuz_kodu": "",
            "universite": "",
            "program": "", 
            "sehir": "",
            "universite_turu": "",
            "ucret": "",
            "ogretim_turu": "",
            # Default ordering by taban puan (column 30 = descending)
            "order[0][column]": "30",
            "order[0][dir]": "desc",
            "order[1][column]": "33",
            "order[1][dir]": "asc", 
            "order[2][column]": "34",
            "order[2][dir]": "asc"
        }
        
        # Update columns with defaults
        for key, value in defaults.items():
            self.columns[key] = value

    def _apply_params(self, params):
        # Map user-friendly parameters to API parameters
        param_mapping = {
            "puan_turu": "puan_turu",  # tyt
            "universite": "universite",
            "program": "program",
            "sehir": "sehir", 
            "universite_turu": "universite_turu",  # Devlet, Vakıf
            "ucret": "ucret",  # Burslu, Ücretli
            "ogretim_turu": "ogretim_turu",  # Örgün, İkinci Öğretim
            "ust_puan": "ust_puan",  # Upper score limit
            "alt_puan": "alt_puan",  # Lower score limit
            "length": "length",  # Results per page
            "start": "start",   # Start index for pagination
            "page": None        # Will be converted to start
        }
        
        # Apply user parameters
        for user_key, api_key in param_mapping.items():
            if user_key in params:
                if user_key == "page":
                    # Convert page to start index
                    page = int(params[user_key])
                    length = int(params.get("length", 50))
                    self.columns["start"] = (page - 1) * length
                elif api_key:
                    self.columns[api_key] = params[user_key]

    def search(self):
        # Prepare the request
        payload = urlencode(self.columns)
        
        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15"
        }

        try:
            response = requests.post(
                "https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t3.php",
                data=payload,
                headers=headers,
                verify=False,
                timeout=30
            )

            if response.status_code == 200:
                try:
                    # Try to parse as JSON directly
                    json_data = response.json()
                    return parse_onlisans_results(json_data)
                except:
                    # If JSON parsing fails, try to extract JSON from mixed HTML/PHP response
                    import re
                    import json
                    json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(0))
                            return parse_onlisans_results(data)
                        except Exception as e:
                            return {"error": f"Failed to parse extracted JSON: {str(e)}"}
                    return {"error": "No valid JSON found in response"}
            else:
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
                
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}
