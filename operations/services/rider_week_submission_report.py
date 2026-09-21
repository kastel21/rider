"""Weekly rider submission and PC-review coverage by province.

A rider has **submitted** for a Monday week when they have at least one
``RiderWeeklyReport`` for that ``week_start`` whose status is past draft
(submitted, under review, approved, or rejected) — the same statuses PC
queues treat as submitted for review.

**Trips** are ``RiderTripEntry`` rows on that rider's reports for the week.

**Need to submit** is the active rider roster in the province (each rider is
expected to file a weekly report).

A **PC review** is a completed coordinator review: ``complete_review`` sets
``reviewed_at`` and status approved or rejected.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Any

from django.db.models import Count, Max, Q

from ..models import RiderWeeklyReport, UserProfile
from ..selectors import (
    get_provinces_queryset,
    get_riders_queryset,
    sunday_of_week,
    week_range_label,
)

SUBMITTED_STATUSES = (
    RiderWeeklyReport.Status.SUBMITTED,
    RiderWeeklyReport.Status.UNDER_REVIEW,
    RiderWeeklyReport.Status.APPROVED,
    RiderWeeklyReport.Status.REJECTED,
)

UNASSIGNED_PROVINCE = "—"


def parse_province_id_from_request(request, user) -> int | None:
    raw = (request.GET.get("province") or "").strip()
    if not raw:
        return None
    try:
        pid = int(raw)
    except ValueError:
        return None
    if not get_provinces_queryset(user).filter(pk=pid).exists():
        return None
    return pid


def _rider_display_name(user) -> str:
    name = (user.get_full_name() or "").strip()
    return name or user.username


def _province_for_profile(profile) -> tuple[int | None, str]:
    district = getattr(profile, "district", None)
    if district is not None:
        prov = getattr(district, "province", None)
        if prov is not None:
            return prov.pk, prov.name
    prov = getattr(profile, "province", None)
    if prov is not None:
        return prov.pk, prov.name
    return None, UNASSIGNED_PROVINCE


def _sort_rider_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(rows, key=lambda r: (-int(r["trip_count"]), r["rider_name"].lower(), r["rider_id"]))


def build_rider_week_submission_report(
    *,
    user,
    week_start: date,
    province_id: int | None = None,
) -> dict[str, Any]:
    riders_qs = (
        get_riders_queryset(user, province_id=province_id)
        .filter(user__is_active=True, user__profile__role=UserProfile.Role.RIDER)
        .select_related(
            "user",
            "user__profile",
            "district",
            "district__province",
            "province",
        )
    )
    profiles = list(riders_qs)
    rider_ids = [p.user_id for p in profiles]

    week_reports = (
        RiderWeeklyReport.objects.filter(rider_id__in=rider_ids, week_start=week_start)
        .values("rider_id")
        .annotate(
            trip_count=Count("trip_entries"),
            submitted_reports=Count(
                "id", distinct=True, filter=Q(status__in=SUBMITTED_STATUSES)
            ),
            reviewed_reports=Count(
                "id", distinct=True, filter=Q(reviewed_at__isnull=False)
            ),
            latest_submitted_at=Max("submitted_at"),
        )
    )
    by_rider: dict[int, dict[str, Any]] = {row["rider_id"]: row for row in week_reports}

    status_rows = RiderWeeklyReport.objects.filter(
        rider_id__in=rider_ids, week_start=week_start
    ).values_list("rider_id", "status")
    statuses_by_rider: dict[int, set[str]] = defaultdict(set)
    for rider_id, status in status_rows:
        statuses_by_rider[rider_id].add(status)

    grouped: dict[tuple[int | None, str], dict[str, Any]] = {}
    for profile in profiles:
        pid, pname = _province_for_profile(profile)
        key = (pid, pname)
        bucket = grouped.get(key)
        if bucket is None:
            bucket = {
                "province_id": pid,
                "province_name": pname,
                "submitted_riders": [],
                "not_submitted_riders": [],
            }
            grouped[key] = bucket

        agg = by_rider.get(profile.user_id, {})
        trip_count = int(agg.get("trip_count") or 0)
        submitted = int(agg.get("submitted_reports") or 0) > 0
        pc_reviewed = int(agg.get("reviewed_reports") or 0) > 0
        status_set = statuses_by_rider.get(profile.user_id, set())
        if submitted:
            labels = [
                RiderWeeklyReport.Status(s).label
                for s in status_set
                if s in SUBMITTED_STATUSES
            ]
            status_display = labels[0] if len(set(labels)) == 1 else ("Mixed" if labels else "Submitted")
        elif status_set:
            status_display = "Draft"
        else:
            status_display = "Not submitted"

        row = {
            "rider_id": profile.user_id,
            "rider_name": _rider_display_name(profile.user),
            "district_name": profile.district.name if profile.district_id else UNASSIGNED_PROVINCE,
            "trip_count": trip_count,
            "submitted": submitted,
            "pc_reviewed": pc_reviewed,
            "status_display": status_display,
            "submitted_at": agg.get("latest_submitted_at"),
        }
        if submitted:
            bucket["submitted_riders"].append(row)
        else:
            bucket["not_submitted_riders"].append(row)

    provinces: list[dict[str, Any]] = []
    for (_pid, pname), bucket in sorted(
        grouped.items(),
        key=lambda item: (item[0][1] == UNASSIGNED_PROVINCE, item[0][1].lower()),
    ):
        submitted_riders = _sort_rider_rows(bucket["submitted_riders"])
        not_submitted_riders = _sort_rider_rows(bucket["not_submitted_riders"])
        rider_count = len(submitted_riders) + len(not_submitted_riders)
        submitted_count = len(submitted_riders)
        pc_reviewed_count = sum(
            1 for r in submitted_riders + not_submitted_riders if r["pc_reviewed"]
        )
        submitted_pending_review = sum(
            1 for r in submitted_riders if not r["pc_reviewed"]
        )
        bucket.update(
            {
                "rider_count": rider_count,
                "submitted_count": submitted_count,
                "not_submitted_count": rider_count - submitted_count,
                "pc_reviewed_count": pc_reviewed_count,
                "needs_to_submit": rider_count,
                "submitted_pending_review": submitted_pending_review,
                "submitted_riders": submitted_riders,
                "not_submitted_riders": not_submitted_riders,
            }
        )
        provinces.append(bucket)

    rider_count = sum(p["rider_count"] for p in provinces)
    submitted_count = sum(p["submitted_count"] for p in provinces)
    pc_reviewed_count = sum(p["pc_reviewed_count"] for p in provinces)
    return {
        "week_start": week_start,
        "week_end": sunday_of_week(week_start),
        "week_range_label": week_range_label(week_start),
        "province_id": province_id,
        "provinces": provinces,
        "totals": {
            "rider_count": rider_count,
            "submitted_count": submitted_count,
            "not_submitted_count": rider_count - submitted_count,
            "pc_reviewed_count": pc_reviewed_count,
            "needs_to_submit": rider_count,
            "submitted_pending_review": sum(p["submitted_pending_review"] for p in provinces),
        },
    }


def _pct(part: int, whole: int) -> str:
    if whole <= 0:
        return ""
    return f"{round(100.0 * part / whole, 1)}"


def province_summary_csv_rows(data: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    headers = [
        "Province",
        "Riders",
        "Submitted",
        "Not submitted",
        "Submitted %",
        "PC reviewed",
        "Need to submit",
        "PC reviewed vs need to submit %",
        "Submitted awaiting PC review",
    ]
    rows: list[list[str]] = []
    for p in data["provinces"]:
        rows.append(
            [
                p["province_name"],
                str(p["rider_count"]),
                str(p["submitted_count"]),
                str(p["not_submitted_count"]),
                _pct(p["submitted_count"], p["rider_count"]),
                str(p["pc_reviewed_count"]),
                str(p["needs_to_submit"]),
                _pct(p["pc_reviewed_count"], p["needs_to_submit"]),
                str(p["submitted_pending_review"]),
            ]
        )
    t = data["totals"]
    rows.append(
        [
            "Total",
            str(t["rider_count"]),
            str(t["submitted_count"]),
            str(t["not_submitted_count"]),
            _pct(t["submitted_count"], t["rider_count"]),
            str(t["pc_reviewed_count"]),
            str(t["needs_to_submit"]),
            _pct(t["pc_reviewed_count"], t["needs_to_submit"]),
            str(t["submitted_pending_review"]),
        ]
    )
    return headers, rows


def rider_detail_csv_rows(data: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    headers = ["Province", "Submission", "Rider", "District", "Trips", "Status", "PC reviewed"]
    rows: list[list[str]] = []
    for p in data["provinces"]:
        for r in p["submitted_riders"]:
            rows.append(
                [
                    p["province_name"],
                    "Submitted",
                    r["rider_name"],
                    r["district_name"],
                    str(r["trip_count"]),
                    r["status_display"],
                    "Yes" if r["pc_reviewed"] else "No",
                ]
            )
        for r in p["not_submitted_riders"]:
            rows.append(
                [
                    p["province_name"],
                    "Not submitted",
                    r["rider_name"],
                    r["district_name"],
                    str(r["trip_count"]),
                    r["status_display"],
                    "Yes" if r["pc_reviewed"] else "No",
                ]
            )
    return headers, rows


def pc_review_csv_rows(data: dict[str, Any]) -> tuple[list[str], list[list[str]]]:
    headers = [
        "Province",
        "PC reviewed",
        "Need to submit",
        "Submitted",
        "Not submitted",
        "Submitted awaiting PC review",
        "PC reviewed vs need to submit %",
    ]
    rows: list[list[str]] = []
    for p in data["provinces"]:
        rows.append(
            [
                p["province_name"],
                str(p["pc_reviewed_count"]),
                str(p["needs_to_submit"]),
                str(p["submitted_count"]),
                str(p["not_submitted_count"]),
                str(p["submitted_pending_review"]),
                _pct(p["pc_reviewed_count"], p["needs_to_submit"]),
            ]
        )
    t = data["totals"]
    rows.append(
        [
            "Total",
            str(t["pc_reviewed_count"]),
            str(t["needs_to_submit"]),
            str(t["submitted_count"]),
            str(t["not_submitted_count"]),
            str(t["submitted_pending_review"]),
            _pct(t["pc_reviewed_count"], t["needs_to_submit"]),
        ]
    )
    return headers, rows
