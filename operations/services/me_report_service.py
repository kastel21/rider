"""Build row/column data for M&E matrices (rider and driver weekly reports in the metrics window)."""

from __future__ import annotations

from typing import Any

from ..models import RiderWeeklyReport, UserProfile
from .me_driver_report_schema import DRIVER_ME_REPORT_COLUMNS
from .me_metrics_service import _window_bounds
from .me_report_resolvers import resolve_cell
from .me_report_schema import ME_REPORT_COLUMNS, MEReportColumn


def _me_report_queryset(*, start_monday, end_monday, role: str):
    return (
        RiderWeeklyReport.objects.filter(
            week_start__gte=start_monday,
            week_start__lte=end_monday,
            rider__profile__role=role,
        )
        .select_related(
            "rider",
            "rider__profile",
            "bike",
            "car",
            "rider__rider_profile",
            "rider__rider_profile__bike",
            "rider__rider_profile__car",
            "rider__rider_profile__facility",
            "rider__rider_profile__district",
            "rider__rider_profile__district__province",
            "rider__rider_profile__province",
        )
        .prefetch_related("trip_entries")
        .order_by("week_start", "id")
    )


def _build_me_table(*, weeks: int, columns: tuple[MEReportColumn, ...], role: str) -> dict[str, Any]:
    start_monday, end_monday = _window_bounds(weeks=weeks)
    qs = _me_report_queryset(start_monday=start_monday, end_monday=end_monday, role=role)

    columns_ctx = [c.to_context_dict() for c in columns]
    rows: list[list[dict[str, str]]] = []

    for report in qs:
        rows.append(
            [
                {"text": resolve_cell(report, col.source), "section": col.section}
                for col in columns
            ]
        )

    return {
        "columns": columns_ctx,
        "rows": rows,
        "row_count": len(rows),
        "window_start": start_monday,
        "window_end": end_monday,
    }


def build_me_report_table(*, weeks: int) -> dict[str, Any]:
    """Rider-role weekly reports in the window (national rider export columns)."""
    return _build_me_table(weeks=weeks, columns=ME_REPORT_COLUMNS, role=UserProfile.Role.RIDER)


def build_driver_me_report_table(*, weeks: int) -> dict[str, Any]:
    """Driver-role weekly reports in the window (national driver export columns)."""
    return _build_me_table(weeks=weeks, columns=DRIVER_ME_REPORT_COLUMNS, role=UserProfile.Role.DRIVER)
