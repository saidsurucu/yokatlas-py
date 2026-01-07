"""
Configuration management using pydantic settings.
"""

from typing import Dict, Any, List
from pydantic import Field, HttpUrl, field_validator
from pydantic_settings import BaseSettings


class YOKATLASSettings(BaseSettings):
    """YOKATLAS API configuration settings"""

    # API endpoints
    base_url: HttpUrl = Field("https://yokatlas.yok.gov.tr", description="Base API URL")
    search_endpoint: str = Field(
        "/server_side/server_processing-atlas2016-TS-t4.php",
        description="Search endpoint",
    )

    # HTTP settings
    timeout: int = Field(30, ge=1, le=300, description="Request timeout in seconds")
    verify_ssl: bool = Field(False, description="SSL certificate verification")
    max_retries: int = Field(3, ge=0, le=10, description="Maximum retry attempts")

    # Default search parameters
    default_length: int = Field(
        50, ge=1, le=500, description="Default results per page"
    )
    default_puan_turu: str = Field("say", description="Default puan türü")

    # Supported years
    supported_years: List[int] = Field(
        [2022, 2023, 2024, 2025], description="Supported years"
    )
    current_year: int = Field(2025, description="Current/default year")

    # Headers
    user_agent: str = Field(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15",
        description="User agent string",
    )

    # Validation settings
    enable_validation: bool = Field(True, description="Enable pydantic validation")
    strict_mode: bool = Field(False, description="Strict validation mode")

    # Cache settings (for future use)
    cache_enabled: bool = Field(False, description="Enable response caching")
    cache_ttl: int = Field(3600, ge=0, description="Cache TTL in seconds")

    # Rate limiting (for future use)
    rate_limit_enabled: bool = Field(False, description="Enable rate limiting")
    requests_per_minute: int = Field(60, ge=1, description="Requests per minute limit")

    model_config = {
        "env_prefix": "YOKATLAS_",
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }

    @field_validator("supported_years")
    @classmethod
    def validate_supported_years(cls, v):
        if not all(isinstance(year, int) and 2020 <= year <= 2030 for year in v):
            raise ValueError("All years must be integers between 2020 and 2030")
        return sorted(v)

    @field_validator("current_year")
    @classmethod
    def validate_current_year(cls, v, info):
        # In Pydantic v2, we need to access other values differently
        # This validation will be done at model level if needed
        return v

    def get_headers(self) -> Dict[str, str]:
        """Get default HTTP headers"""
        return {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": self.user_agent,
        }

    def get_full_search_url(self) -> str:
        """Get complete search URL"""
        return f"{self.base_url}{self.search_endpoint}"

    def is_year_supported(self, year: int) -> bool:
        """Check if year is supported"""
        return year in self.supported_years


# Global settings instance
settings = YOKATLASSettings()
