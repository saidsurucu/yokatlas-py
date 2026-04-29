"""Serialization helpers (snake_case ↔ camelCase) for the YÖK Atlas API."""

from __future__ import annotations


def to_camel(snake: str) -> str:
    """Convert ``snake_case`` to ``camelCase``.

    Trailing/leading underscores are preserved (Pydantic uses them for private
    attributes). Numbers and existing camelCase tokens pass through unchanged.
    """
    parts = snake.split("_")
    if len(parts) == 1:
        return snake
    head, *tail = parts
    return head + "".join(word[:1].upper() + word[1:] for word in tail if word)
