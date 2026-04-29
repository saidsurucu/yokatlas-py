"""yokatlas-py exception hierarchy."""

from __future__ import annotations


class YokAtlasError(Exception):
    """Base exception for all yokatlas-py errors."""


class APIError(YokAtlasError):
    """Raised when the YÖK Atlas API returns an unexpected response."""

    def __init__(self, message: str, *, status_code: int | None = None, body: str | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class NotFoundError(APIError):
    """Raised when a requested resource (e.g., kılavuz kodu) is not found."""


class RateLimitError(APIError):
    """Raised when the API responds with a rate-limit status."""


class LookupError(YokAtlasError):
    """Raised when a smart-search lookup cannot resolve a name to an id."""

    def __init__(self, name: str, *, kind: str, suggestions: list[str] | None = None) -> None:
        msg = f"Could not resolve {kind} '{name}'."
        if suggestions:
            msg += f" Closest matches: {', '.join(suggestions)}"
        super().__init__(msg)
        self.name = name
        self.kind = kind
        self.suggestions = suggestions or []
