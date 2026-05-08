"""Aggregate metrics for Monitoring & Evaluation (national weekly reports)."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from django.db.models import Count, IntegerField, Q, Sum
from django.db.models.functions import Coalesce
from django.utils import timezone

from ..models import Province, RiderWeeklyReport, UserProfile
from ..selectors import monday_of_local_today, sunday_of_week


def parse_weeks_param(raw: str | None, *, default: int = 12, max_weeks: int = 52) -> int:
    if not raw or not str(raw).strip():
        return default
    try:
        n = int(str(raw).strip())
    except ValueError:
        return default
    return max(1, min(max_weeks, n))


def _window_bounds(*, weeks: int) -> tuple:
    """
    Rolling Monday..Monday window for M&E exports and charts.

    The window **ends on the previous calendar week's Monday** (the most recently
    completed reporting week), not the current week, so tables align with data that
    is typically still being entered for the week in progress.
    """
    end_monday = monday_of_local_today() - timedelta(days=7)
    start_monday = end_monday - timedelta(weeks=weeks - 1)
    return start_monday, end_monday


def _province_rows(qs) -> list[dict[str, Any]]:
    rows = list(
        qs.annotate(
            pid=Coalesce(
                "rider__rider_profile__district__province_id",
                "rider__rider_profile__province_id",
                output_field=IntegerField(),
            )
        )
        .values("pid")
        .annotate(cnt=Count("id"))
        .order_by("-cnt")
    )
    ids = [r["pid"] for r in rows if r["pid"] is not None]
    names = Province.objects.in_bulk(ids) if ids else {}
    out: list[dict[str, Any]] = []
    for r in rows:
        pid = r["pid"]
        if pid is None:
            name = "Unknown"
        else:
            p = names.get(pid)
            name = p.name if p else f"Province #{pid}"
        out.append({"province_id": pid, "name": name, "count": r["cnt"]})
    return out


def _top_n_with_other(rows: list[dict[str, Any]], n: int = 15) -> tuple[list[dict[str, Any]], int]:
    if len(rows) <= n:
        return rows, 0
    top = rows[:n]
    other = sum(r["count"] for r in rows[n:])
    return top, other


def build_me_metrics(*, weeks: int) -> dict[str, Any]:
    """
    National aggregates for ME. All-time summary cards; ``weeks`` scopes the
    period section and weekly trend chart (Monday weeks). The period ends on the
    **previous** completed week (see ``_window_bounds``).
    """
    base = RiderWeeklyReport.objects.all()
    st = RiderWeeklyReport.Status

    all_agg = base.aggregate(
        total_reports=Count("id"),
        samples_total=Sum("samples_collected"),
        n_draft=Count("id", filter=Q(status=st.DRAFT)),
        n_submitted=Count("id", filter=Q(status=st.SUBMITTED)),
        n_under_review=Count("id", filter=Q(status=st.UNDER_REVIEW)),
        n_approved=Count("id", filter=Q(status=st.APPROVED)),
        n_rejected=Count("id", filter=Q(status=st.REJECTED)),
        distinct_riders=Count(
            "rider_id",
            distinct=True,
            filter=Q(rider__profile__role=UserProfile.Role.RIDER),
        ),
        distinct_drivers=Count(
            "rider_id",
            distinct=True,
            filter=Q(rider__profile__role=UserProfile.Role.DRIVER),
        ),
    )

    start_monday, end_monday = _window_bounds(weeks=weeks)
    window = base.filter(week_start__gte=start_monday, week_start__lte=end_monday)

    win_agg = window.aggregate(
        reports=Count("id"),
        samples=Sum("samples_collected"),
        rider_reports=Count("id", filter=Q(rider__profile__role=UserProfile.Role.RIDER)),
        driver_reports=Count("id", filter=Q(rider__profile__role=UserProfile.Role.DRIVER)),
        distinct_riders=Count(
            "rider_id",
            distinct=True,
            filter=Q(rider__profile__role=UserProfile.Role.RIDER),
        ),
        distinct_drivers=Count(
            "rider_id",
            distinct=True,
            filter=Q(rider__profile__role=UserProfile.Role.DRIVER),
        ),
    )

    by_week = {
        row["week_start"]: row
        for row in window.values("week_start")
        .annotate(report_count=Count("id"), samples_week=Sum("samples_collected"))
        .order_by("week_start")
    }

    labels: list[str] = []
    report_counts: list[int] = []
    sample_counts: list[int] = []
    d = start_monday
    while d <= end_monday:
        labels.append(d.isoformat())
        row = by_week.get(d)
        if row:
            report_counts.append(int(row["report_count"] or 0))
            sample_counts.append(int(row["samples_week"] or 0))
        else:
            report_counts.append(0)
            sample_counts.append(0)
        d += timedelta(days=7)

    prov_all = _province_rows(base)
    prov_top, prov_other = _top_n_with_other(prov_all, 15)
    prov_win = _province_rows(window)
    prov_win_top, prov_win_other = _top_n_with_other(prov_win, 15)

    return {
        "weeks": weeks,
        "window_start": start_monday,
        "window_end": end_monday,
        "window_range_label": (
            f"{start_monday.strftime('%d %b %Y')} – "
            f"{sunday_of_week(end_monday).strftime('%d %b %Y')}"
        ),
        "all_time": {
            "total_reports": all_agg["total_reports"] or 0,
            "samples_total": int(all_agg["samples_total"] or 0),
            "by_status": [
                {"key": "draft", "label": "Draft", "count": all_agg["n_draft"] or 0},
                {"key": "submitted", "label": "Submitted", "count": all_agg["n_submitted"] or 0},
                {"key": "under_review", "label": "Under review", "count": all_agg["n_under_review"] or 0},
                {"key": "approved", "label": "Approved", "count": all_agg["n_approved"] or 0},
                {"key": "rejected", "label": "Rejected", "count": all_agg["n_rejected"] or 0},
            ],
            "distinct_riders": all_agg["distinct_riders"] or 0,
            "distinct_drivers": all_agg["distinct_drivers"] or 0,
        },
        "window": {
            "reports": win_agg["reports"] or 0,
            "samples": int(win_agg["samples"] or 0),
            "rider_reports": win_agg["rider_reports"] or 0,
            "driver_reports": win_agg["driver_reports"] or 0,
            "distinct_riders": win_agg["distinct_riders"] or 0,
            "distinct_drivers": win_agg["distinct_drivers"] or 0,
        },
        "province_top": prov_top,
        "province_other_count": prov_other,
        "province_window_top": prov_win_top,
        "province_window_other_count": prov_win_other,
        "chart": {
            "labels": labels,
            "reports": report_counts,
            "samples": sample_counts,
            "weeks": weeks,
        },
        "generated_at": timezone.now(),
    }
