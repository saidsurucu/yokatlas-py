"""HTTP transport layer for the YÖK Atlas JSON API.

Provides a thin wrapper around ``httpx`` with retries, JSON serialization,
and unified error handling for both sync and async use.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from .config import Settings, settings as default_settings
from .exceptions import APIError, NotFoundError, RateLimitError


def _build_limits() -> httpx.Limits:
    return httpx.Limits(max_connections=100, max_keepalive_connections=20)


def _raise_for_response(response: httpx.Response) -> None:
    if response.is_success:
        return
    body: str | None
    try:
        body = response.text
    except Exception:  # pragma: no cover
        body = None
    msg = f"YÖK Atlas API error {response.status_code} for {response.request.url}"
    if response.status_code == 404:
        raise NotFoundError(msg, status_code=response.status_code, body=body)
    if response.status_code in (418, 429):
        raise RateLimitError(msg, status_code=response.status_code, body=body)
    raise APIError(msg, status_code=response.status_code, body=body)


def _decode_json(response: httpx.Response) -> Any:
    try:
        return response.json()
    except json.JSONDecodeError as exc:
        raise APIError(
            f"Failed to decode JSON from {response.request.url}: {exc}",
            status_code=response.status_code,
            body=response.text[:500] if response.text else None,
        ) from exc


class HttpClient:
    """Synchronous JSON HTTP client over :class:`httpx.Client`."""

    def __init__(self, *, settings: Settings | None = None, client: httpx.Client | None = None) -> None:
        self.settings = settings or default_settings
        if client is None:
            transport = httpx.HTTPTransport(retries=self.settings.max_retries, verify=self.settings.verify_ssl)
            client = httpx.Client(
                base_url=str(self.settings.base_url).rstrip("/"),
                timeout=self.settings.timeout,
                headers=self.settings.headers(),
                limits=_build_limits(),
                transport=transport,
                follow_redirects=True,
            )
            self._owns_client = True
        else:
            self._owns_client = False
        self._client = client

    @property
    def client(self) -> httpx.Client:
        return self._client

    def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        response = self._client.get(path, params=params)
        _raise_for_response(response)
        return _decode_json(response)

    def post_json(self, path: str, *, json_body: dict[str, Any]) -> Any:
        response = self._client.post(path, json=json_body)
        _raise_for_response(response)
        return _decode_json(response)

    def close(self) -> None:
        if self._owns_client and not self._client.is_closed:
            self._client.close()

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncHttpClient:
    """Asynchronous JSON HTTP client over :class:`httpx.AsyncClient`."""

    def __init__(self, *, settings: Settings | None = None, client: httpx.AsyncClient | None = None) -> None:
        self.settings = settings or default_settings
        if client is None:
            transport = httpx.AsyncHTTPTransport(retries=self.settings.max_retries, verify=self.settings.verify_ssl)
            client = httpx.AsyncClient(
                base_url=str(self.settings.base_url).rstrip("/"),
                timeout=self.settings.timeout,
                headers=self.settings.headers(),
                limits=_build_limits(),
                transport=transport,
                follow_redirects=True,
            )
            self._owns_client = True
        else:
            self._owns_client = False
        self._client = client

    @property
    def client(self) -> httpx.AsyncClient:
        return self._client

    async def get_json(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        response = await self._client.get(path, params=params)
        _raise_for_response(response)
        return _decode_json(response)

    async def post_json(self, path: str, *, json_body: dict[str, Any]) -> Any:
        response = await self._client.post(path, json=json_body)
        _raise_for_response(response)
        return _decode_json(response)

    async def aclose(self) -> None:
        if self._owns_client and not self._client.is_closed:
            await self._client.aclose()

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.aclose()


__all__ = ["AsyncHttpClient", "HttpClient"]
