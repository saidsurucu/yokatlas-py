import httpx
from urllib.parse import urlencode
from typing import Any, Optional, Union
from .utils import load_column_data, parse_onlisans_results, format_array_parameter
from .models import SearchParams, ProgramInfo
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class YOKATLASOnlisansTercihSihirbazi:
    """YOKATLAS Önlisans Tercih Sihirbazı - Search interface for associate degree programs."""

    def __init__(self, params: dict[str, Any]) -> None:
        """
        Initialize search client with parameters.

        Args:
            params: Search parameters dictionary
        """
        self.params = params

        # Load base column structure from JSON
        self.columns: dict[str, str] = load_column_data()

        # Set default values and ordering
        self._set_defaults()

        # Apply user parameters
        self._apply_params(params)

    def _set_defaults(self) -> None:
        """Set default values for search parameters."""
        defaults: dict[str, Union[str, int]] = {
            "draw": 2,  # Önlisans still uses draw=2 (different from lisans which uses 4)
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
            # Updated to use array format (empty arrays)
            "universite": "[]",
            "program": "[]",
            "sehir": "[]",
            "universite_turu": "[]",
            "ucret": "[]",
            "ogretim_turu": "[]",
            # Updated ordering: default sort column changed from 30 to 32
            "order[0][column]": "32",
            "order[0][dir]": "desc",
            "order[1][column]": "33",
            "order[1][dir]": "asc",
            "order[2][column]": "34",
            "order[2][dir]": "asc",
        }

        # Update columns with defaults
        for key, value in defaults.items():
            self.columns[key] = str(value)

    def _apply_params(self, params: dict[str, Any]) -> None:
        """Apply user parameters to search configuration with new array format."""
        # Parameters that need array formatting
        array_params = {
            "universite": "universite",
            "program": "program",
            "sehir": "sehir",
            "universite_turu": "universite_turu",
            "ucret": "ucret",
            "ogretim_turu": "ogretim_turu",
        }

        # Parameters that remain as strings
        string_params = {
            "puan_turu": "puan_turu",  # tyt
            "ust_puan": "ust_puan",  # Upper score limit
            "alt_puan": "alt_puan",  # Lower score limit
            "length": "length",  # Results per page
            "start": "start",  # Start index for pagination
            "page": None,  # Will be converted to start
        }

        # Apply array parameters
        for user_key, api_key in array_params.items():
            if user_key in params and params[user_key]:
                formatted_value = format_array_parameter(params[user_key])
                self.columns[api_key] = formatted_value

        # Apply string parameters
        for user_key, api_key in string_params.items():
            if user_key in params:
                if user_key == "page":
                    # Convert page to start index
                    page = int(params[user_key])
                    length = int(params.get("length", 50))
                    self.columns["start"] = str((page - 1) * length)
                elif api_key:
                    self.columns[api_key] = str(params[user_key])

    def search(self) -> list[dict[str, Any]]:
        """
        Perform search for önlisans programs.

        Returns:
            List of program dictionaries or error information
        """
        # Prepare the request
        payload = urlencode(
            self.columns, safe="[]%"
        )  # Keep array brackets and percent signs

        headers = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
        }

        url = "https://yokatlas.yok.gov.tr/server_side/server_processing-atlas2016-TS-t3.php"

        try:
            response = httpx.post(
                url,
                data=payload,
                headers=headers,
                verify=False,
                timeout=30,
            )

            if response.status_code == 200:
                try:
                    # Try to parse as JSON directly
                    json_data = response.json()
                    return parse_onlisans_results(json_data)
                except Exception as json_error:
                    # If JSON parsing fails, try to extract JSON from mixed HTML/PHP response
                    import re

                    json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
                    if json_match:
                        try:
                            data = json.loads(json_match.group(0))
                            return parse_onlisans_results(data)
                        except Exception as e:
                            return {
                                "error": f"Failed to parse extracted JSON: {str(e)}",
                                "raw_response": response.text[:500],
                            }
                    return {
                        "error": "No valid JSON found in response",
                        "raw_response": response.text[:500],
                    }
            else:
                return {
                    "error": f"HTTP {response.status_code}: {response.text[:200]}",
                    "full_response": response.text,
                }

        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
