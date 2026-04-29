"""yokatlas-py — Python client for the YÖK Atlas tercih kılavuzu JSON API."""

from __future__ import annotations

from .client import (
    AsyncYokAtlasClient,
    YokAtlasClient,
    get_program,
    list_cities,
    list_program_groups,
    list_universities,
    search_programs,
)
from .config import Settings, settings
from .exceptions import (
    APIError,
    LookupError,
    NotFoundError,
    RateLimitError,
    YokAtlasError,
)
from .models import (
    City,
    Program,
    ProgramGroup,
    PuanTuru,
    SearchFilters,
    SearchPage,
    University,
    YearlyStats,
)

__version__ = "1.0.0"

__all__ = [
    # Clients
    "AsyncYokAtlasClient",
    "YokAtlasClient",
    # Convenience
    "get_program",
    "list_cities",
    "list_program_groups",
    "list_universities",
    "search_programs",
    # Models
    "City",
    "Program",
    "ProgramGroup",
    "PuanTuru",
    "SearchFilters",
    "SearchPage",
    "University",
    "YearlyStats",
    # Configuration
    "Settings",
    "settings",
    # Exceptions
    "APIError",
    "LookupError",
    "NotFoundError",
    "RateLimitError",
    "YokAtlasError",
    # Version
    "__version__",
]
