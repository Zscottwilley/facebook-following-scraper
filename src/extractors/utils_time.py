from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from typing import Optional

_RELATIVE_MINUTES_PATTERN = re.compile(
    r"(?P<value>\d+)\s*(min|mins|minute|minutes)\b",
    re.IGNORECASE,
)
_RELATIVE_HOURS_PATTERN = re.compile(
    r"(?P<value>\d+)\s*(h|hr|hrs|hour|hours)\b",
    re.IGNORECASE,
)
_RELATIVE_DAYS_PATTERN = re.compile(
    r"(?P<value>\d+)\s*(d|day|days)\b",
    re.IGNORECASE,
)

def _ensure_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

def parse_relative_time(text: str, now: Optional[datetime] = None) -> datetime:
    """
    Parse a Facebook-like relative timestamp into an absolute UTC datetime.

    Supported examples:
        - "Just now"
        - "5 mins"
        - "2 hours ago"
        - "1 d"
        - "Yesterday at 14:30"

    If parsing fails, returns the current time (UTC).
    """
    if now is None:
        now = datetime.now(timezone.utc)
    else:
        now = _ensure_utc(now)

    s = text.strip().lower()

    if s in {"just now", "now"}:
        return now

    if s.startswith("yesterday"):
        # Try to parse "Yesterday at HH:MM"
        m = re.search(r"(\d{1,2}):(\d{2})", s)
        dt = now - timedelta(days=1)
        if m:
            hour = int(m.group(1))
            minute = int(m.group(2))
            dt = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return dt

    m = _RELATIVE_MINUTES_PATTERN.search(s)
    if m:
        minutes = int(m.group("value"))
        return now - timedelta(minutes=minutes)

    m = _RELATIVE_HOURS_PATTERN.search(s)
    if m:
        hours = int(m.group("value"))
        return now - timedelta(hours=hours)

    m = _RELATIVE_DAYS_PATTERN.search(s)
    if m:
        days = int(m.group("value"))
        return now - timedelta(days=days)

    # Fallback: try to parse as ISO-ish string
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d.%m.%Y %H:%M"):
        try:
            dt = datetime.strptime(text, fmt)
            return _ensure_utc(dt)
        except ValueError:
            continue

    # Last resort: return now
    return now

def to_iso_utc(dt: datetime) -> str:
    """
    Convert datetime to ISO 8601 string in UTC.
    """
    return _ensure_utc(dt).isoformat()