"""Wall-clock time helpers for naive MySQL DATETIME columns."""
from datetime import datetime
from zoneinfo import ZoneInfo

_CN = ZoneInfo("Asia/Shanghai")


def shanghai_now() -> datetime:
    """Return current Asia/Shanghai time as a naive datetime.

    Stored values match China local wall clock when read from SQL tools or API
    without timezone conversion. (Previously ``datetime.utcnow`` stored UTC,
    which often looked like early-morning hours when misread as local time.)

    Returns:
        datetime: Now in Asia/Shanghai, tzinfo stripped for DATETIME storage.

    """
    return datetime.now(_CN).replace(tzinfo=None)
