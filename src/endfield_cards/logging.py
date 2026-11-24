"""Opt-in library logging with centralized credential and URL redaction."""

import logging
import re
from collections.abc import Mapping
from urllib.parse import urlsplit, urlunsplit

_PRIVATE = re.compile(r"token|cred|authorization|cookie|password|secret", re.I)
_URL = re.compile(r"https?://[^\s'\"<>]+")
_SECRET = re.compile(
    r"(?i)((?:[\"']?(?:token|cred|credential|authorization|cookie|password|secret)[\"']?)\s*[=:]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;}]+)"
)
_BEARER = re.compile(r"(?i)\b(Bearer|Basic)\s+[^\s,;\"'}]+")
_COOKIE = re.compile(r"(?im)(\bCookie\s*:\s*)[^\r\n]+")


def _safe_url(match: re.Match[str]) -> str:
    try:
        parts = urlsplit(match.group())
        return urlunsplit((parts.scheme, parts.netloc.rsplit("@", 1)[-1], parts.path, "", ""))
    except ValueError:
        return "[redacted-url]"


def redact(value: object) -> object:
    """Remove private fields and URL queries before logging structured values."""
    if isinstance(value, Mapping):
        return {str(k): "[redacted]" if _PRIVATE.search(str(k)) else redact(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [redact(item) for item in value]
    if isinstance(value, str):
        safe = _URL.sub(_safe_url, value)
        safe = _BEARER.sub(r"\1 [redacted]", safe)
        safe = _COOKIE.sub(r"\1[redacted]", safe)
        return _SECRET.sub(r"\1[redacted]", safe)
    return value


class RedactingFormatter(logging.Formatter):
    """Redact after formatting, including exception text."""

    def format(self, record: logging.LogRecord) -> str:
        return str(redact(super().format(record)))


def configure_logging(level: int = logging.INFO, *, handler: logging.Handler | None = None) -> logging.Logger:
    """Install at most one library-owned handler; never configure the root logger."""
    logger = logging.getLogger("endfield_cards")
    for existing in list(logger.handlers):
        if getattr(existing, "_endfield_cards_owned", False):
            logger.removeHandler(existing)
    target = handler or logging.StreamHandler()
    target.setFormatter(RedactingFormatter("%(levelname)s endfield_cards: %(message)s"))
    target._endfield_cards_owned = True  # type: ignore[attr-defined]
    logger.addHandler(target)
    logger.setLevel(level)
    logger.propagate = False
    return logger
