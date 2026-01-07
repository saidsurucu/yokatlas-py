"""
Pytest configuration and shared fixtures.

This module provides fixtures used across all test modules.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from tests.fixtures.html_responses import (
    SINGLE_TABLE_HTML,
    TABLE_WITH_TOTALS_HTML,
    MULTI_TABLE_HTML,
    EMPTY_TABLE_HTML,
    PLACEHOLDER_VALUES_HTML,
    KONTENJAN_YERLESME_HTML,
    SEARCH_API_RESPONSE,
)


# -----------------------------------------------------------------------------
# HTTP Client Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def mock_httpx_response():
    """Create a mock httpx Response object."""

    def _create_response(
        content: str = SINGLE_TABLE_HTML,
        status_code: int = 200,
    ) -> MagicMock:
        response = MagicMock(spec=httpx.Response)
        response.status_code = status_code
        response.text = content
        response.raise_for_status = MagicMock()
        if status_code >= 400:
            response.raise_for_status.side_effect = httpx.HTTPStatusError(
                message=f"HTTP {status_code}",
                request=MagicMock(),
                response=response,
            )
        return response

    return _create_response


@pytest.fixture
def mock_async_client(mock_httpx_response):
    """Create a mock AsyncClient for testing fetchers."""

    def _create_client(response_html: str = SINGLE_TABLE_HTML, status_code: int = 200):
        mock_client = AsyncMock(spec=httpx.AsyncClient)
        mock_response = mock_httpx_response(response_html, status_code)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client.is_closed = False
        return mock_client

    return _create_client


@pytest.fixture
def patch_yokatlas_client(mock_async_client):
    """Patch YOKATLASClient.get_client to return mock client."""

    def _patch(response_html: str = SINGLE_TABLE_HTML, status_code: int = 200):
        client = mock_async_client(response_html, status_code)
        return patch(
            "yokatlas_py.http_client.YOKATLASClient.get_client",
            return_value=client,
        )

    return _patch


# -----------------------------------------------------------------------------
# HTML Response Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def single_table_html():
    """Standard single table HTML response."""
    return SINGLE_TABLE_HTML


@pytest.fixture
def table_with_totals_html():
    """Table with totals row HTML response."""
    return TABLE_WITH_TOTALS_HTML


@pytest.fixture
def multi_table_html():
    """Multiple tables HTML response."""
    return MULTI_TABLE_HTML


@pytest.fixture
def empty_table_html():
    """Empty table HTML response."""
    return EMPTY_TABLE_HTML


@pytest.fixture
def placeholder_values_html():
    """HTML with placeholder values (---)."""
    return PLACEHOLDER_VALUES_HTML


@pytest.fixture
def kontenjan_yerlesme_html():
    """Kontenjan yerlesme table HTML."""
    return KONTENJAN_YERLESME_HTML


# -----------------------------------------------------------------------------
# Search API Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def search_api_response():
    """Mock search API JSON response."""
    return SEARCH_API_RESPONSE.copy()


@pytest.fixture
def mock_search_response(mock_httpx_response):
    """Create mock response for search API."""
    import json

    response = mock_httpx_response(json.dumps(SEARCH_API_RESPONSE))
    response.json = MagicMock(return_value=SEARCH_API_RESPONSE)
    return response


# -----------------------------------------------------------------------------
# Test Data Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def sample_program_id():
    """Sample valid program ID."""
    return "123456789"


@pytest.fixture
def sample_year():
    """Sample valid year."""
    return 2024


@pytest.fixture
def sample_params():
    """Sample search parameters."""
    return {
        "puan_turu": "say",
        "ust_bs": 10000,
        "length": 10,
    }


@pytest.fixture
def sample_atlas_params(sample_program_id, sample_year):
    """Sample atlas parameters."""
    return {
        "program_id": sample_program_id,
        "year": sample_year,
    }


# -----------------------------------------------------------------------------
# Instance Fixtures
# -----------------------------------------------------------------------------


@pytest.fixture
def lisans_tercih_instance(sample_params):
    """Create YOKATLASLisansTercihSihirbazi instance."""
    from yokatlas_py import YOKATLASLisansTercihSihirbazi

    return YOKATLASLisansTercihSihirbazi(sample_params)


@pytest.fixture
def onlisans_tercih_instance(sample_params):
    """Create YOKATLASOnlisansTercihSihirbazi instance."""
    from yokatlas_py import YOKATLASOnlisansTercihSihirbazi

    return YOKATLASOnlisansTercihSihirbazi(sample_params)


@pytest.fixture
def lisans_atlas_instance(sample_atlas_params):
    """Create YOKATLASLisansAtlasi instance."""
    from yokatlas_py import YOKATLASLisansAtlasi

    return YOKATLASLisansAtlasi(sample_atlas_params)


@pytest.fixture
def onlisans_atlas_instance(sample_atlas_params):
    """Create YOKATLASOnlisansAtlasi instance."""
    from yokatlas_py import YOKATLASOnlisansAtlasi

    return YOKATLASOnlisansAtlasi(sample_atlas_params)


# -----------------------------------------------------------------------------
# Pytest Markers Configuration
# -----------------------------------------------------------------------------


def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests (fast, mocked)")
    config.addinivalue_line(
        "markers", "integration: Integration tests (may require network)"
    )
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "real_api: Tests against real YOKATLAS API")
