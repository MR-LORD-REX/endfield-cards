"""Source-clock formatting without advancing captured game state."""

from datetime import UTC, datetime
from typing import Any
from zoneinfo import ZoneInfo


def source_datetime(value: Any) -> datetime | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        if isinstance(value, datetime):
            result = value
        elif isinstance(value, (int, float)) or str(value).replace(".", "", 1).isdigit():
            if float(value) <= 0:
                return None
            result = datetime.fromtimestamp(float(value), UTC)
        else:
            result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return (result.replace(tzinfo=UTC) if result.tzinfo is None else result).astimezone(UTC)
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def remaining(deadline: datetime | None, now: datetime | None) -> str:
    end, start = source_datetime(deadline), source_datetime(now)
    if end is None or start is None:
        return "Unavailable"
    seconds = int((end - start).total_seconds())
    if seconds <= 0:
        return "Due"
    days, rest = divmod(seconds, 86400)
    hours, rest = divmod(rest, 3600)
    return f"{days}d {hours}h" if days else f"{hours}h {rest // 60:02d}m" if hours else f"{rest // 60}m"


def display_time(value: datetime | None, context: Any) -> str:
    observed = source_datetime(value)
    return (
        observed.astimezone(ZoneInfo(context.display_timezone)).strftime("%d %b %Y · %H:%M %Z")
        if observed is not None
        else "Unavailable"
    )
