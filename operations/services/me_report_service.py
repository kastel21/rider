"""Build row/column data for M&E matrices (rider and driver weekly reports in the metrics window)."""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Any

from ..models import RiderWeeklyReport, UserProfile
from .me_driver_report_schema import DRIVER_ME_REPORT_COLUMNS
from .me_metrics_service import _window_bounds
from .me_report_resolvers import _bike_or_car, _full_name, resolve_cell_group
from .me_report_schema import ME_REPORT_COLUMNS, MEReportColumn


def _report_bike_reg_key(report: RiderWeeklyReport) -> str:
    """Normalized bike/vehicle code on the report (grouping key)."""
    return (_bike_or_car(report) or "").strip().upper()


def _me_report_queryset(
    *,
    start_monday: date,
    end_monday: date,
    role: str,
    pc_approved_only: bool = False,
):
    filters = {
        "week_start__gte": start_monday,
        "week_start__lte": end_monday,
        "rider__profile__role": role,
    }
    if pc_approved_only:
        filters["status"] = RiderWeeklyReport.Status.APPROVED
    return (
        RiderWeeklyReport.objects.filter(**filters)
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
        .order_by("week_start", "rider_id", "id")
    )


def _build_me_table(
    *,
    start_monday: date,
    end_monday: date,
    columns: tuple[MEReportColumn, ...],
    role: str,
    pc_approved_only: bool = False,
) -> dict[str, Any]:
    qs = _me_report_queryset(
        start_monday=start_monday,
        end_monday=end_monday,
        role=role,
        pc_approved_only=pc_approved_only,
    )

    by_rider_bike_week: dict[tuple[int, str, date], list[RiderWeeklyReport]] = defaultdict(list)
    for report in qs:
        by_rider_bike_week[
            (report.rider_id, _report_bike_reg_key(report), report.week_start)
        ].append(report)

    columns_ctx = [c.to_context_dict() for c in columns]
    rows: list[list[dict[str, str]]] = []

    sort_keys = sorted(
        by_rider_bike_week.keys(),
        key=lambda k: (
            k[2],
            _full_name(by_rider_bike_week[k][0].rider).lower(),
            k[1],
        ),
    )
    for key in sort_keys:
        group = by_rider_bike_week[key]
        rows.append(
            [
                {
                    "text": resolve_cell_group(group, col.source, vehicle_scoped=True),
                    "section": col.section,
                    "key": col.key,
                }
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


def _build_me_table_weeks(*, weeks: int, columns: tuple[MEReportColumn, ...], role: str) -> dict[str, Any]:
    start_monday, end_monday = _window_bounds(weeks=weeks)
    return _build_me_table(
        start_monday=start_monday,
        end_monday=end_monday,
        columns=columns,
        role=role,
    )


def build_me_report_table(*, weeks: int) -> dict[str, Any]:
    """Rider-role weekly reports: one row per rider and bike reg per Monday week (aggregated)."""
    return _build_me_table_weeks(weeks=weeks, columns=ME_REPORT_COLUMNS, role=UserProfile.Role.RIDER)


def build_driver_me_report_table(*, weeks: int) -> dict[str, Any]:
    """Driver-role weekly reports: one row per driver and vehicle reg per Monday week (aggregated)."""
    return _build_me_table_weeks(
        weeks=weeks,
        columns=DRIVER_ME_REPORT_COLUMNS,
        role=UserProfile.Role.DRIVER,
    )


def build_me_report_table_for_week(
    *,
    week_start: date,
    role: str,
    pc_approved_only: bool = True,
) -> dict[str, Any]:
    """Single calendar week (Monday ``week_start``)."""
    columns = (
        ME_REPORT_COLUMNS
        if role == UserProfile.Role.RIDER
        else DRIVER_ME_REPORT_COLUMNS
    )
    return _build_me_table(
        start_monday=week_start,
        end_monday=week_start,
        columns=columns,
        role=role,
        pc_approved_only=pc_approved_only,
    )
