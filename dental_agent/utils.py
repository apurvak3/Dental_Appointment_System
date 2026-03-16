from __future__ import annotations

from collections.abc import Iterable


def _normalize_content(content) -> str:
    if isinstance(content, str):
        text = content.strip()
        return text or " "

    if isinstance(content, Iterable):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                text = str(item.get("text", "")).strip()
                if text:
                    parts.append(text)
            elif isinstance(item, str):
                text = item.strip()
                if text:
                    parts.append(text)
        if parts:
            return "\n".join(parts)

    return " "


def sanitize_messages(messages: list) -> list:
    """Return copies of messages with non-empty content for model-safe invocation."""
    sanitized = []
    for message in messages:
        content = _normalize_content(getattr(message, "content", " "))
        sanitized.append(message.model_copy(update={"content": content}))
    return sanitized
