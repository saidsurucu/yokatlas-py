"""
Base class for all YOKATLAS fetcher modules.

This module provides the abstract base class that eliminates code duplication
across 58 fetcher modules (30 lisans + 28 onlisans).

Common functionality abstracted:
- Year validation
- URL construction
- HTTP requests with error handling
- HTML parsing utilities
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from bs4 import BeautifulSoup
import httpx

from .http_client import YOKATLASClient
from .config import settings


class BaseFetcher(ABC):
    """
    Abstract base class for YOKATLAS data fetchers.

    Subclasses must define:
        ENDPOINT: str - PHP endpoint (e.g., "1010.php")
        PROGRAM_TYPE: str - "lisans" or "onlisans"
        RESULT_KEY: str - Key for the result dictionary (e.g., "cinsiyet_dagilimi")

    Subclasses must implement:
        parse(html_content: str) -> dict[str, Any]

    Usage:
        class CinsiyetDagilimiLisansFetcher(BaseFetcher):
            ENDPOINT = "1010.php"
            PROGRAM_TYPE = "lisans"
            RESULT_KEY = "cinsiyet_dagilimi"

            def parse(self, html_content: str) -> dict[str, Any]:
                # Custom parsing logic
                ...

        # Usage:
        fetcher = CinsiyetDagilimiLisansFetcher("123456789", 2024)
        result = await fetcher.fetch()
    """

    # Subclasses must define these
    ENDPOINT: str
    PROGRAM_TYPE: str
    RESULT_KEY: str

    def __init__(self, program_id: str, year: int):
        """
        Initialize fetcher with program ID and year.

        Args:
            program_id: YÖK program kodu (9 digit string)
            year: Year (2022-2025)
        """
        self.program_id = program_id
        self.year = year

    async def fetch(self) -> dict[str, Any]:
        """
        Main fetch method with validation and error handling.

        Returns:
            dict with fetched data or {"error": "message"} on failure
        """
        # Validate year
        validation_error = self._validate_year()
        if validation_error:
            return validation_error

        # Build URL
        url = YOKATLASClient.build_url(
            self.PROGRAM_TYPE,
            self.ENDPOINT,
            self.program_id,
            self.year,
        )

        # Fetch HTML
        try:
            client = await YOKATLASClient.get_client()
            response = await client.get(url)
            response.raise_for_status()
            html_content = response.text
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP {e.response.status_code}: Failed to fetch data from YOKATLAS"}
        except httpx.RequestError as e:
            return {"error": f"Failed to fetch data from YOKATLAS: {str(e)}"}

        # Parse HTML
        try:
            return self.parse(html_content)
        except Exception as e:
            return {"error": f"Failed to parse HTML: {str(e)}"}

    def _validate_year(self) -> Optional[dict[str, str]]:
        """
        Validate year against supported years.

        Returns:
            Error dict if invalid, None if valid
        """
        if self.year not in settings.supported_years:
            return {
                "error": f"Invalid year. Only {settings.supported_years} are supported."
            }
        return None

    @abstractmethod
    def parse(self, html_content: str) -> dict[str, Any]:
        """
        Parse HTML content to extract structured data.

        Must be implemented by subclasses.

        Args:
            html_content: Raw HTML string from YOKATLAS

        Returns:
            Dictionary with parsed data
        """
        ...

    # -------------------------------------------------------------------------
    # Shared Parsing Utilities
    # -------------------------------------------------------------------------

    @staticmethod
    def clean_html(html_content: str) -> str:
        """
        Clean HTML content by replacing common placeholder values.

        Args:
            html_content: Raw HTML string

        Returns:
            Cleaned HTML string
        """
        return html_content.replace("---", "0")

    @staticmethod
    def create_soup(html_content: str, clean: bool = True) -> BeautifulSoup:
        """
        Create BeautifulSoup object from HTML content.

        Args:
            html_content: Raw HTML string
            clean: Whether to clean placeholder values first

        Returns:
            BeautifulSoup object
        """
        if clean:
            html_content = BaseFetcher.clean_html(html_content)
        return BeautifulSoup(html_content, "html.parser")

    @staticmethod
    def find_table(
        soup: BeautifulSoup,
        class_name: str = "table table-bordered",
    ) -> Optional[Any]:
        """
        Find a table in the HTML.

        Args:
            soup: BeautifulSoup object
            class_name: CSS class name for the table

        Returns:
            Table element or None
        """
        return soup.find("table", {"class": class_name})

    @staticmethod
    def find_all_tables(
        soup: BeautifulSoup,
        class_name: str = "table table-bordered",
    ) -> list[Any]:
        """
        Find all tables in the HTML.

        Args:
            soup: BeautifulSoup object
            class_name: CSS class name for the tables

        Returns:
            List of table elements
        """
        return soup.find_all("table", {"class": class_name})

    @staticmethod
    def parse_single_table(
        soup: BeautifulSoup,
        result_key: str,
        first_col_header: str = "Type",
        table_class: str = "table table-bordered",
    ) -> dict[str, Any]:
        """
        Parse a single table with headers and rows.

        Standard table format:
            | Type  | 2024 | 2023 | 2022 |
            |-------|------|------|------|
            | Erkek | 50   | 45   | 40   |
            | Kadin | 30   | 35   | 32   |

        Args:
            soup: BeautifulSoup object
            result_key: Key for the result dictionary
            first_col_header: Name for the first column (row type)
            table_class: CSS class for the table

        Returns:
            Dictionary with parsed data
        """
        table = soup.find("table", {"class": table_class})
        if not table:
            return {result_key: []}

        # Extract headers
        headers = [
            header.get_text(strip=True)
            for header in table.find_all("th")[1:]  # Skip first header
        ]

        # Extract rows
        data = []
        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if not cols:
                    continue

                row_data = {
                    first_col_header: cols[0].get_text(strip=True).replace("*", "")
                }

                for i, header in enumerate(headers):
                    if i + 1 < len(cols):
                        value = cols[i + 1].get_text(strip=True).replace("*", "")
                        row_data[header] = value
                    else:
                        row_data[header] = None

                data.append(row_data)

        return {result_key: data}

    @staticmethod
    def parse_table_with_totals(
        soup: BeautifulSoup,
        result_key: str,
        first_col_header: str = "Type",
        table_class: str = "table table-bordered",
    ) -> dict[str, Any]:
        """
        Parse a table that has a totals row.

        Standard table format with totals:
            | Durum | 2024 | 2023 |
            |-------|------|------|
            | Type1 | 50   | 45   |
            | Type2 | 30   | 35   |
            | TOPLAM| 80   | 80   |

        Args:
            soup: BeautifulSoup object
            result_key: Key for the main data
            first_col_header: Name for the first column
            table_class: CSS class for the table

        Returns:
            Dictionary with parsed data and totals
        """
        table = soup.find("table", {"class": table_class})
        if not table:
            return {result_key: [], "toplam": {}}

        # Extract headers
        headers = [
            header.get_text(strip=True)
            for header in table.find_all("th")[1:]
        ]

        # Extract rows
        data = []
        totals = {}

        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if not cols:
                    continue

                first_col = cols[0].get_text(strip=True).replace("*", "")
                row_data = {first_col_header: first_col}

                for i, header in enumerate(headers):
                    if i + 1 < len(cols):
                        value = cols[i + 1].get_text(strip=True).replace("*", "")
                        row_data[header] = value
                    else:
                        row_data[header] = None

                # Check if this is the totals row
                if first_col.upper() in ("TOPLAM", "GENEL TOPLAM", "TOTAL"):
                    totals = row_data
                else:
                    data.append(row_data)

        return {result_key: data, "toplam": totals}

    @staticmethod
    def parse_numeric(value: str, default: Any = None) -> Any:
        """
        Parse a string value as numeric (int or float).

        Args:
            value: String value to parse
            default: Default value if parsing fails

        Returns:
            Parsed numeric value or default
        """
        if not value or value == "0" or value == "---":
            return default

        # Clean the value
        cleaned = value.replace(".", "").replace(",", ".").replace("%", "").strip()

        try:
            if "." in cleaned:
                return float(cleaned)
            return int(cleaned)
        except (ValueError, TypeError):
            return default
