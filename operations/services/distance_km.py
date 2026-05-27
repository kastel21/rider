"""Whole-km rounding for distance travelled (display, export, and form save)."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal
from typing import Any


def round_distance_km(value: Any) -> int:
    if value is None:
        return 0
    d = value if isinstance(value, Decimal) else Decimal(str(value or 0))
    return int(d.to_integral_value(rounding=ROUND_HALF_UP))


def distance_km_str(value: Any) -> str:
    if value is None:
        return ""
    return str(round_distance_km(value))
