"""Referred laboratory samples table for M&E (matches national PC referral layout).

Uses the same rolling window as other M&E tables (``me_metrics_service._window_bounds``),
ending on the previous completed Monday week.
"""

from __future__ import annotations

from typing import Any

from django.utils import timezone

from ..models import ReferredSample
from ..selectors import sunday_of_week
from .me_metrics_service import _window_bounds

# (key, label, section) — same shape as other M&E matrices for templates/CSS.
REFERRED_SAMPLES_COLUMNS: tuple[tuple[str, str, str], ...] = (
    ("date", "Date", "basic"),
    ("lab", "Lab", "basic"),
    ("sample_type", "Sample type", "reach"),
    ("test_type", "Test type", "reach"),
    ("total_out", "Total number of samples referred out", "reach"),
    ("lab_referred_to", "Lab Samples Referred to", "service"),
    ("swift", "Swift Consignment Number", "service"),
    ("comments", "Comments", "outcome"),
    ("data_quality", "Data Quality Checks", "neutral"),
)


def _local_date_str(dt) -> str:
    if dt is None:
        return ""
    return timezone.localtime(dt).strftime("%d/%m/%Y")


def _swift_display(rs: ReferredSample) -> str:
    s = (rs.swift_consignment_number or "").strip()
    if not s:
        return ""
    if s.isdigit():
        return str(int(s))
    return s


def build_me_referred_samples_table(*, weeks: int) -> dict[str, Any]:
    start_monday, end_monday = _window_bounds(weeks=weeks)
    end_date = sunday_of_week(end_monday)

    qs = (
        ReferredSample.objects.filter(
            created_at__date__gte=start_monday,
            created_at__date__lte=end_date,
        )
        .select_related(
            "from_facility",
            "from_facility__district",
            "from_facility__district__province",
            "to_facility",
            "to_facility__district",
            "to_facility__district__province",
        )
        .order_by("-created_at", "-id")
    )

    columns = [{"key": k, "label": lbl, "section": sec} for k, lbl, sec in REFERRED_SAMPLES_COLUMNS]
    rows: list[list[dict[str, str]]] = []

    for rs in qs:
        values = {
            "date": _local_date_str(rs.created_at),
            "lab": rs.referring_lab_display(),
            "sample_type": rs.get_sample_type_display(),
            "test_type": rs.get_test_type_display(),
            "total_out": str(rs.total_samples_referred_out),
            "lab_referred_to": rs.referred_to_lab_display(),
            "swift": _swift_display(rs),
            "comments": (rs.comments or "").strip(),
            "data_quality": "",
        }
        rows.append(
            [{"text": values[k], "section": sec} for k, _, sec in REFERRED_SAMPLES_COLUMNS]
        )

    return {
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "window_start": start_monday,
        "window_end": end_monday,
    }
