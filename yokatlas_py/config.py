"""Configuration for the YÖK Atlas client (pydantic-settings)."""

from __future__ import annotations

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration. All fields can be overridden via ``YOKATLAS_*`` env vars."""

    model_config = SettingsConfigDict(
        env_prefix="YOKATLAS_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    base_url: HttpUrl = Field(
        default=HttpUrl("https://yokatlas.yok.gov.tr"),
        description="Base URL for the YÖK Atlas JSON API.",
    )
    timeout: float = Field(default=30.0, gt=0, le=300, description="HTTP timeout in seconds.")
    verify_ssl: bool = Field(default=True, description="Verify TLS certificates.")
    max_retries: int = Field(default=3, ge=0, le=10, description="HTTP transport retries.")
    user_agent: str = Field(
        default="yokatlas-py/0.6",
        description="User-Agent header.",
    )
    lookup_cache_ttl: int = Field(
        default=3600,
        ge=0,
        description="TTL (seconds) for the in-process universities/programs/cities cache.",
    )

    def headers(self) -> dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }


settings = Settings()
