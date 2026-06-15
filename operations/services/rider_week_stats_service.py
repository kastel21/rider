"""Week-level stats for a rider: specimens, results, rejections, fuel, distance."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model
from django.db.models import Sum

from ..models import RiderTripEntry, RiderWeekFuelSummary, RiderWeeklyReport, SampleRejection
from ..selectors import get_reports_queryset
from .distance_km import round_distance_km

User = get_user_model()

SPECIMEN_TYPE_ROWS: list[tuple[str, str, str]] = [
    ("vl_blood_plasma", "results_vl_blood_plasma", "VL blood/plasma"),
    ("vl_dbs", "results_vl_dbs", "VL DBS"),
    ("eid_blood", "results_eid_blood", "EID blood"),
    ("eid_dbs", "results_eid_dbs", "EID DBS"),
    ("sputum", "results_sputum", "Sputum"),
    ("sputum_culture_dr", "results_sputum_culture_dr", "Sputum culture DR"),
    ("hpv", "results_hpv", "HPV"),
]

REJECTION_REASON_COLUMNS: list[tuple[str, str]] = [
    ("rejected_too_old", "Too old"),
    ("rejected_patient_info_mismatch", "Info mismatch"),
    ("rejected_request_form_missing", "Form missing"),
    ("rejected_sample_missing", "Sample missing"),
    ("rejected_other", "Other"),
]


def _intz(value) -> int:
    return int(value or 0)


def _week_fuel_for_user(
    rider_id: int, week_start: date, report_ids: list[int]
) -> tuple[Decimal, Decimal]:
    row = (
        RiderWeekFuelSummary.objects.filter(rider_id=rider_id, week_start=week_start)
        .only("fuel_allocated", "fuel_used")
        .first()
    )
    if row is not None:
        fa = row.fuel_allocated if row.fuel_allocated is not None else Decimal("0")
        fu = row.fuel_used if row.fuel_used is not None else Decimal("0")
        return (fa, fu)
    if not report_ids:
        return (Decimal("0"), Decimal("0"))
    s = RiderTripEntry.objects.filter(report_id__in=report_ids).aggregate(
        a=Sum("fuel_allocated"),
        u=Sum("fuel_used"),
    )
    fa = s["a"] if s["a"] is not None else Decimal("0")
    fu = s["u"] if s["u"] is not None else Decimal("0")
    return (fa, fu)


def _aggregate_rejections(report_ids: list[int]) -> dict[str, Any]:
    qs = SampleRejection.objects.filter(report_id__in=report_ids)
    totals = qs.aggregate(
        rejected_total=Sum("rejected_total"),
        rejected_too_old=Sum("rejected_too_old"),
        rejected_patient_info_mismatch=Sum("rejected_patient_info_mismatch"),
        rejected_request_form_missing=Sum("rejected_request_form_missing"),
        rejected_sample_missing=Sum("rejected_sample_missing"),
        rejected_other=Sum("rejected_other"),
    )
    by_type_rows = list(
        qs.values("sample_type")
        .annotate(
            rejected_total=Sum("rejected_total"),
            rejected_too_old=Sum("rejected_too_old"),
            rejected_patient_info_mismatch=Sum("rejected_patient_info_mismatch"),
            rejected_request_form_missing=Sum("rejected_request_form_missing"),
            rejected_sample_missing=Sum("rejected_sample_missing"),
            rejected_other=Sum("rejected_other"),
        )
        .order_by("sample_type")
    )
    by_type: list[dict[str, Any]] = []
    for row in by_type_rows:
        st = row["sample_type"]
        try:
            label = SampleRejection.SampleType(st).label
        except ValueError:
            label = str(st or "")
        reasons = {
            key: _intz(row.get(key))
            for key, _ in REJECTION_REASON_COLUMNS
        }
        total = _intz(row.get("rejected_total"))
        if total == 0 and not any(reasons.values()):
            continue
        by_type.append(
            {
                "key": st,
                "label": label,
                "rejected_total": total,
                "reasons": reasons,
            }
        )
    reason_totals = [
        {
            "key": key,
            "label": label,
            "count": _intz(totals.get(key)),
        }
        for key, label in REJECTION_REASON_COLUMNS
    ]
    return {
        "rejected_total": _intz(totals.get("rejected_total")),
        "by_sample_type": by_type,
        "reason_totals": reason_totals,
    }


def build_rider_week_stats(user: User, week_start: date) -> dict[str, Any]:
    """Aggregate transport, rejection, fuel, and distance stats for one rider week."""
    reports = list(
        get_reports_queryset(user)
        .filter(week_start=week_start)
        .prefetch_related("trip_entries", "sample_rejections")
        .order_by("-updated_at", "-id")
    )
    report_ids = [r.id for r in reports]

    trip_agg = RiderTripEntry.objects.filter(report_id__in=report_ids).aggregate(
        vl_blood_plasma=Sum("vl_blood_plasma"),
        vl_dbs=Sum("vl_dbs"),
        eid_blood=Sum("eid_blood"),
        eid_dbs=Sum("eid_dbs"),
        sputum=Sum("sputum"),
        sputum_culture_dr=Sum("sputum_culture_dr"),
        hpv=Sum("hpv"),
        results_vl_blood_plasma=Sum("results_vl_blood_plasma"),
        results_vl_dbs=Sum("results_vl_dbs"),
        results_eid_blood=Sum("results_eid_blood"),
        results_eid_dbs=Sum("results_eid_dbs"),
        results_sputum=Sum("results_sputum"),
        results_sputum_culture_dr=Sum("results_sputum_culture_dr"),
        results_hpv=Sum("results_hpv"),
    )

    specimens_by_type: list[dict[str, Any]] = []
    results_by_type: list[dict[str, Any]] = []
    specimens_total = 0
    results_total = 0
    for spec_key, res_key, label in SPECIMEN_TYPE_ROWS:
        spec_count = _intz(trip_agg.get(spec_key))
        res_count = _intz(trip_agg.get(res_key))
        specimens_total += spec_count
        results_total += res_count
        specimens_by_type.append({"key": spec_key, "label": label, "count": spec_count})
        results_by_type.append({"key": res_key, "label": label, "count": res_count})

    total_distance = Decimal("0")
    for report in reports:
        total_distance += Decimal(round_distance_km(report.distance_travelled))

    fuel_allocated, fuel_used = _week_fuel_for_user(user.id, week_start, report_ids)

    rejections = _aggregate_rejections(report_ids)

    return {
        "report_count": len(reports),
        "has_data": bool(reports),
        "specimens_by_type": specimens_by_type,
        "specimens_total": specimens_total,
        "results_by_type": results_by_type,
        "results_total": results_total,
        "rejections": rejections,
        "fuel_allocated": fuel_allocated,
        "fuel_used": fuel_used,
        "distance_km": total_distance,
    }
