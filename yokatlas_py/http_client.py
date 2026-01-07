"""
Shared HTTP client with connection pooling for YOKATLAS API requests.

This module provides a centralized HTTP client configuration to:
- Avoid creating new connections for each fetcher
- Maintain consistent timeout, SSL, and header settings
- Provide URL building utilities with proper year handling
"""

from typing import Optional, ClassVar
import httpx
from contextlib import asynccontextmanager


class YOKATLASClient:
    """
    Singleton-style HTTP client for YOKATLAS API requests.

    Provides connection pooling and consistent configuration across all fetchers.

    Usage:
        client = await YOKATLASClient.get_client()
        response = await client.get(url)

        # Or using context manager for automatic cleanup:
        async with YOKATLASClient.session() as client:
            response = await client.get(url)
    """

    # Class-level client instance
    _client: ClassVar[Optional[httpx.AsyncClient]] = None

    # Configuration constants
    BASE_URL: ClassVar[str] = "https://yokatlas.yok.gov.tr"
    TIMEOUT: ClassVar[int] = 30
    VERIFY_SSL: ClassVar[bool] = False

    DEFAULT_HEADERS: ClassVar[dict[str, str]] = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
        "Accept": "text/html, */*; q=0.01",
        "Accept-Language": "tr-TR,tr;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
    }

    @classmethod
    async def get_client(cls) -> httpx.AsyncClient:
        """
        Get or create the shared client instance.

        Returns:
            httpx.AsyncClient: The shared HTTP client instance
        """
        if cls._client is None or cls._client.is_closed:
            cls._client = httpx.AsyncClient(
                verify=cls.VERIFY_SSL,
                timeout=httpx.Timeout(cls.TIMEOUT),
                headers=cls.DEFAULT_HEADERS,
                follow_redirects=True,
                limits=httpx.Limits(
                    max_connections=100,
                    max_keepalive_connections=20,
                ),
            )
        return cls._client

    @classmethod
    async def close(cls) -> None:
        """Close the client connection and release resources."""
        if cls._client is not None and not cls._client.is_closed:
            await cls._client.aclose()
            cls._client = None

    @classmethod
    @asynccontextmanager
    async def session(cls):
        """
        Context manager for HTTP client usage.

        Note: Does NOT close the client on exit to allow connection reuse.
        Use close() explicitly when shutting down the application.

        Usage:
            async with YOKATLASClient.session() as client:
                response = await client.get(url)
        """
        client = await cls.get_client()
        try:
            yield client
        except Exception:
            raise

    @classmethod
    def build_url(
        cls,
        program_type: str,
        endpoint: str,
        program_id: str,
        year: int,
    ) -> str:
        """
        Build URL with proper year handling.

        YOKATLAS has a special case: 2024 URLs don't include the year in path.

        Args:
            program_type: "lisans" or "onlisans"
            endpoint: PHP endpoint (e.g., "1010.php", "2050.php")
            program_id: YÖK program kodu (9 digit string)
            year: Year (2022-2025)

        Returns:
            Complete URL string

        Examples:
            >>> YOKATLASClient.build_url("lisans", "1010.php", "123456789", 2024)
            'https://yokatlas.yok.gov.tr/content/lisans-dynamic/1010.php?y=123456789'

            >>> YOKATLASClient.build_url("lisans", "1010.php", "123456789", 2023)
            'https://yokatlas.yok.gov.tr/2023/content/lisans-dynamic/1010.php?y=123456789'
        """
        # Map program type to URL path segment
        path_segment = f"{program_type}-dynamic"

        # 2024 is the "current" year without year prefix in URL
        if year == 2024:
            url_path = f"/content/{path_segment}/{endpoint}?y={program_id}"
        else:
            url_path = f"/{year}/content/{path_segment}/{endpoint}?y={program_id}"

        return f"{cls.BASE_URL}{url_path}"

    @classmethod
    def build_search_url(cls, program_type: str) -> str:
        """
        Build search endpoint URL.

        Args:
            program_type: "lisans" or "onlisans"

        Returns:
            Search endpoint URL
        """
        if program_type == "lisans":
            endpoint = "server_processing-atlas2016-TS-t4.php"
        else:
            endpoint = "server_processing-atlas2016-MTS-t4.php"

        return f"{cls.BASE_URL}/server_side/{endpoint}"
