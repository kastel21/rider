"""National M&E overview aggregates beyond core RiderWeeklyReport counts.

Trip/rejection aggregates filter by ``report__week_start`` in the metrics window.
Referrals use ``created_at`` date in the same calendar span as ``build_me_referred_samples_table``.
Fuel weekly series use ``RiderWeekFuelSummary``; distance uses ``RiderWeeklyReport.distance_travelled``.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any

from django.db.models import (
    Count,
    F,
    IntegerField,
    Q,
    Sum,
)
from django.db.models.functions import Coalesce

from .distance_km import round_distance_km
from ..models import (
    PCDistrictWeeklyTransportStat,
    Province,
    ReferredSample,
    RiderTripEntry,
    RiderWeeklyReport,
    RiderWeekFuelSummary,
    SampleRejection,
)
from ..selectors import sunday_of_week


def _trip_window_filter(start_monday: date, end_monday: date) -> Q:
    return Q(report__week_start__gte=start_monday, report__week_start__lte=end_monday)


def _week_start_key(value: date | datetime | str | None) -> date | None:
    """Normalize ORM week values for dict lookup (SQL Server may return datetime)."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        return date.fromisoformat(value[:10])
    return None


def _aggregate_trip_specimens_results(*, start_monday: date, end_monday: date) -> dict[str, Any]:
    flt = _trip_window_filter(start_monday, end_monday)
    agg = RiderTripEntry.objects.filter(flt).aggregate(
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
        fuel_allocated=Sum("fuel_allocated"),
        fuel_used=Sum("fuel_used"),
        distance_travelled=Sum("distance_travelled"),
    )
    intz = lambda k: int(agg.get(k) or 0)

    spec = {
        "vl_blood_plasma": intz("vl_blood_plasma"),
        "vl_dbs": intz("vl_dbs"),
        "eid_blood": intz("eid_blood"),
        "eid_dbs": intz("eid_dbs"),
        "sputum": intz("sputum"),
        "sputum_culture_dr": intz("sputum_culture_dr"),
        "hpv": intz("hpv"),
    }
    spec["total"] = sum(spec.values())

    res = {
        "vl_blood_plasma": intz("results_vl_blood_plasma"),
        "vl_dbs": intz("results_vl_dbs"),
        "eid_blood": intz("results_eid_blood"),
        "eid_dbs": intz("results_eid_dbs"),
        "sputum": intz("results_sputum"),
        "sputum_culture_dr": intz("results_sputum_culture_dr"),
        "hpv": intz("results_hpv"),
    }
    res["total"] = sum(res.values())

    fuel_alloc = agg.get("fuel_allocated") or Decimal("0")
    fuel_used = agg.get("fuel_used") or Decimal("0")
    dist = agg.get("distance_travelled") or Decimal("0")

    ratio = None
    if spec["total"] > 0:
        ratio = round(res["total"] / spec["total"], 3)

    return {
        "specimens_by_type": spec,
        "results_by_type": res,
        "results_to_specimens_ratio": ratio,
        "fuel_allocated_trip_sum": float(fuel_alloc),
        "fuel_used_trip_sum": float(fuel_used),
        "distance_trip_sum": float(round_distance_km(dist)),
    }


def _province_specimen_top(*, start_monday: date, end_monday: date, n: int = 5) -> list[dict[str, Any]]:
    sp_sum = (
        Coalesce(F("vl_blood_plasma"), 0)
        + Coalesce(F("vl_dbs"), 0)
        + Coalesce(F("eid_blood"), 0)
        + Coalesce(F("eid_dbs"), 0)
        + Coalesce(F("sputum"), 0)
        + Coalesce(F("sputum_culture_dr"), 0)
        + Coalesce(F("hpv"), 0)
    )
    rows = list(
        RiderTripEntry.objects.filter(_trip_window_filter(start_monday, end_monday))
        .annotate(
            pid=Coalesce(
                "report__rider__rider_profile__district__province_id",
                "report__rider__rider_profile__province_id",
                output_field=IntegerField(),
            ),
            specimens_row=sp_sum,
        )
        .values("pid")
        .annotate(volume=Sum("specimens_row"))
        .order_by("-volume")[: (n + 5)]
    )
    ids = [r["pid"] for r in rows if r["pid"] is not None]
    names = Province.objects.in_bulk(ids) if ids else {}
    out: list[dict[str, Any]] = []
    for r in rows:
        if len(out) >= n:
            break
        pid = r["pid"]
        if pid is None:
            continue
        p = names.get(pid)
        out.append(
            {
                "name": p.name if p else f"Province #{pid}",
                "volume": int(r["volume"] or 0),
            }
        )
    return out


def _rejections_block(*, start_monday: date | None, end_monday: date | None) -> dict[str, Any]:
    flt = Q()
    if start_monday is not None and end_monday is not None:
        flt = Q(report__week_start__gte=start_monday, report__week_start__lte=end_monday)

    qs = SampleRejection.objects.filter(flt)
    totals = qs.aggregate(
        rejected_total=Sum("rejected_total"),
        too_old=Sum("rejected_too_old"),
        patient_mismatch=Sum("rejected_patient_info_mismatch"),
        form_missing=Sum("rejected_request_form_missing"),
        sample_missing=Sum("rejected_sample_missing"),
        other=Sum("rejected_other"),
    )
    by_type = list(
        qs.values("sample_type")
        .annotate(count=Sum("rejected_total"))
        .order_by("-count")
    )
    labels = []
    for row in by_type:
        st = row["sample_type"]
        try:
            labels.append({"key": st, "label": SampleRejection.SampleType(st).label, "count": int(row["count"] or 0)})
        except ValueError:
            labels.append({"key": st or "", "label": str(st), "count": int(row["count"] or 0)})

    return {
        "rejected_total": int(totals["rejected_total"] or 0),
        "reasons": [
            {"key": "too_old", "label": "Too old", "count": int(totals["too_old"] or 0)},
            {"key": "patient_mismatch", "label": "Patient info mismatch", "count": int(totals["patient_mismatch"] or 0)},
            {"key": "form_missing", "label": "Request form missing", "count": int(totals["form_missing"] or 0)},
            {"key": "sample_missing", "label": "Sample missing", "count": int(totals["sample_missing"] or 0)},
            {"key": "other", "label": "Other", "count": int(totals["other"] or 0)},
        ],
        "by_sample_type": labels,
    }


def _operations_kpis(*, window: Any, all_reports: Any) -> dict[str, Any]:
    st = RiderWeeklyReport.Status

    def _block(qs) -> dict[str, Any]:
        with_temp = qs.filter(average_datalogger_temperature__isnull=False).count()
        total = qs.count()
        temp_pct = round(100.0 * with_temp / total, 1) if total else None

        appr = qs.filter(status=st.APPROVED)
        appr_n = appr.count()
        me_n = appr.filter(me_reviewed_at__isnull=False).count()
        me_pct = round(100.0 * me_n / appr_n, 1) if appr_n else None

        scheduled_qs = qs.filter(scheduled_visits__gt=0).annotate(tcount=Count("trip_entries"))
        sched_total = 0
        actual_rows = 0
        n_sched_reports = 0
        for r in scheduled_qs.iterator(chunk_size=500):
            n_sched_reports += 1
            sched_total += int(r.scheduled_visits or 0)
            actual_rows += int(r.tcount)

        visit_rate = None
        if sched_total > 0:
            visit_rate = round(100.0 * actual_rows / sched_total, 1)

        return {
            "reports_with_temperature_pct": temp_pct,
            "reports_with_temperature_n": with_temp,
            "reports_total_n": total,
            "me_review_of_approved_pct": me_pct,
            "me_reviewed_n": me_n,
            "approved_n": appr_n,
            "visit_completion_pct": visit_rate,
            "reports_with_scheduled_visits_n": n_sched_reports,
            "scheduled_visits_sum": sched_total,
            "trip_rows_as_actual_visits_sum": actual_rows,
        }

    return {
        "window": _block(window),
        "all_time": _block(all_reports),
    }


def _fuel_distance(*, start_monday: date, end_monday: date, labels: list[str]) -> dict[str, Any]:
    """Weekly national fuel from RiderWeekFuelSummary; distance from weekly reports."""
    rows = {
        r["week_start"]: r
        for r in RiderWeekFuelSummary.objects.filter(
            week_start__gte=start_monday,
            week_start__lte=end_monday,
        )
        .values("week_start")
        .annotate(
            fa=Sum("fuel_allocated"),
            fu=Sum("fuel_used"),
        )
        .order_by("week_start")
    }
    dist_rows = {
        r["week_start"]: r
        for r in RiderWeeklyReport.objects.filter(
            week_start__gte=start_monday,
            week_start__lte=end_monday,
        )
        .values("week_start")
        .annotate(dt=Sum("distance_travelled"))
        .order_by("week_start")
    }
    fuel_allocated: list[float] = []
    fuel_used: list[float] = []
    distance: list[float] = []
    for iso in labels:
        d = date.fromisoformat(iso)
        row = rows.get(d)
        drow = dist_rows.get(d)
        if row:
            fuel_allocated.append(float(row["fa"] or 0))
            fuel_used.append(float(row["fu"] or 0))
        else:
            fuel_allocated.append(0.0)
            fuel_used.append(0.0)
        if drow:
            distance.append(float(round_distance_km(drow["dt"] or 0)))
        else:
            distance.append(0.0)

    totals = (
        RiderWeekFuelSummary.objects.filter(
            week_start__gte=start_monday,
            week_start__lte=end_monday,
        )
        .order_by()
        .aggregate(
            fa=Sum("fuel_allocated"),
            fu=Sum("fuel_used"),
        )
    )
    fa = totals["fa"] or Decimal("0")
    fu = totals["fu"] or Decimal("0")
    dist_totals = RiderWeeklyReport.objects.filter(
        week_start__gte=start_monday,
        week_start__lte=end_monday,
    ).aggregate(dt=Sum("distance_travelled"))
    dt = dist_totals["dt"] or Decimal("0")
    dt_km = round_distance_km(dt)

    # samples per km from window reports (same window as fuel weeks)
    window_reports = RiderWeeklyReport.objects.filter(
        week_start__gte=start_monday,
        week_start__lte=end_monday,
    )
    samples_sum = int(window_reports.aggregate(s=Sum("samples_collected"))["s"] or 0)
    eff_samples_per_km = None
    if dt_km > 0:
        eff_samples_per_km = round(samples_sum / dt_km, 4)

    return {
        "week_fuel_allocated": fuel_allocated,
        "week_fuel_used": fuel_used,
        "week_distance": distance,
        "period_fuel_allocated": float(fa),
        "period_fuel_used": float(fu),
        "period_distance_km": float(dt_km),
        "samples_per_km_in_period": eff_samples_per_km,
        "note": (
            "Fuel totals follow the week fuel capture (RiderWeekFuelSummary). "
            "Distance is recorded on each weekly report (RiderWeeklyReport). "
            "Trip-row fuel sums can differ when week summaries are not entered."
        ),
    }


def _referred_kpis(*, start_monday: date, end_monday: date) -> dict[str, Any]:
    end_date = sunday_of_week(end_monday)
    qs = ReferredSample.objects.filter(
        created_at__date__gte=start_monday,
        created_at__date__lte=end_date,
    )
    total = qs.aggregate(n=Count("id"), samples=Sum("total_samples_referred_out"))
    by_test = list(
        qs.values("test_type")
        .annotate(cnt=Count("id"), samples=Sum("total_samples_referred_out"))
        .order_by("-samples")
    )
    out_test = []
    for row in by_test:
        tt = row["test_type"]
        try:
            label = ReferredSample.TestType(tt).label
        except ValueError:
            label = str(tt)
        out_test.append(
            {
                "key": tt or "",
                "label": label,
                "records": int(row["cnt"] or 0),
                "samples": int(row["samples"] or 0),
            }
        )
    return {
        "referral_records": int(total["n"] or 0),
        "samples_referred_out": int(total["samples"] or 0),
        "by_test_type": out_test,
    }


def _pc_transport(*, start_monday: date, end_monday: date) -> dict[str, Any]:
    agg = PCDistrictWeeklyTransportStat.objects.filter(
        week_start__gte=start_monday,
        week_start__lte=end_monday,
    ).aggregate(
        rider_accidents=Sum("rider_accidents"),
        incomplete_bike_transport_trips=Sum("incomplete_bike_transport_trips"),
        specimens_non_ist_total=Sum("specimens_non_ist_total"),
        specimens_ambulance=Sum("specimens_ambulance"),
        specimens_alternative_ip_transport=Sum("specimens_alternative_ip_transport"),
        specimens_mohcc_arranged_transport=Sum("specimens_mohcc_arranged_transport"),
        specimens_courier=Sum("specimens_courier"),
        specimens_other_non_ist=Sum("specimens_other_non_ist"),
    )
    return {k: int(agg.get(k) or 0) for k in agg}


def _weekly_delivery_trends(*, start_monday: date, end_monday: date, labels: list[str]) -> dict[str, Any]:
    """National trip-row specimens/results by report week (VL, HPV, TB programs)."""
    rows: dict[date, dict[str, Any]] = {}
    for r in (
        RiderTripEntry.objects.filter(_trip_window_filter(start_monday, end_monday))
        .values("report__week_start")
        .annotate(
            vl_plasma=Sum("vl_blood_plasma"),
            vl_dbs=Sum("vl_dbs"),
            res_vl_plasma=Sum("results_vl_blood_plasma"),
            res_vl_dbs=Sum("results_vl_dbs"),
            hpv=Sum("hpv"),
            res_hpv=Sum("results_hpv"),
            sputum=Sum("sputum"),
            sputum_dr=Sum("sputum_culture_dr"),
            res_sputum=Sum("results_sputum"),
            res_sputum_dr=Sum("results_sputum_culture_dr"),
        )
        .order_by("report__week_start")
    ):
        key = _week_start_key(r["report__week_start"])
        if key is not None:
            rows[key] = r

    def _int(row: dict | None, key: str) -> int:
        if not row:
            return 0
        return int(row.get(key) or 0)

    vl_specimens: list[int] = []
    vl_results: list[int] = []
    hpv_specimens: list[int] = []
    hpv_results: list[int] = []
    tb_specimens: list[int] = []
    tb_results: list[int] = []

    for iso in labels:
        row = rows.get(date.fromisoformat(iso))
        vl_specimens.append(_int(row, "vl_plasma") + _int(row, "vl_dbs"))
        vl_results.append(_int(row, "res_vl_plasma") + _int(row, "res_vl_dbs"))
        hpv_specimens.append(_int(row, "hpv"))
        hpv_results.append(_int(row, "res_hpv"))
        tb_specimens.append(_int(row, "sputum") + _int(row, "sputum_dr"))
        tb_results.append(_int(row, "res_sputum") + _int(row, "res_sputum_dr"))

    return {
        "vl": {"specimens": vl_specimens, "results": vl_results},
        "hpv": {"specimens": hpv_specimens, "results": hpv_results},
        "tb": {"specimens": tb_specimens, "results": tb_results},
    }


def _trip_province_pid_expr():
    return Coalesce(
        "report__rider__rider_profile__district__province_id",
        "report__rider__rider_profile__province_id",
        output_field=IntegerField(),
    )


def _province_delivery_charts(
    *,
    start_monday: date,
    end_monday: date,
    weeks: int,
    top_n: int = 10,
) -> dict[str, Any]:
    """Top provinces by VL / HPV trip-row volume in the metrics window."""
    prov_rows = list(
        RiderTripEntry.objects.filter(_trip_window_filter(start_monday, end_monday))
        .annotate(pid=_trip_province_pid_expr())
        .values("pid")
        .annotate(
            vl_plasma=Sum("vl_blood_plasma"),
            vl_dbs=Sum("vl_dbs"),
            res_vl_plasma=Sum("results_vl_blood_plasma"),
            res_vl_dbs=Sum("results_vl_dbs"),
            hpv=Sum("hpv"),
            res_hpv=Sum("results_hpv"),
        )
        .order_by("pid")
    )

    def _intz(v: Any) -> int:
        return int(v or 0)

    vl_candidates: list[dict[str, Any]] = []
    hpv_candidates: list[dict[str, Any]] = []
    for r in prov_rows:
        pid = r["pid"]
        if pid is None:
            continue
        vp = _intz(r["vl_plasma"])
        vd = _intz(r["vl_dbs"])
        rp = _intz(r["res_vl_plasma"])
        rd = _intz(r["res_vl_dbs"])
        if vp + vd + rp + rd > 0:
            vl_candidates.append(
                {
                    "pid": pid,
                    "vl_plasma": vp,
                    "vl_dbs": vd,
                    "res_vl_plasma": rp,
                    "res_vl_dbs": rd,
                    "vl_spec_total": vp + vd,
                }
            )
        h = _intz(r["hpv"])
        rh = _intz(r["res_hpv"])
        if h + rh > 0:
            hpv_candidates.append({"pid": pid, "hpv": h, "res_hpv": rh, "hpv_total": h + rh})

    vl_candidates.sort(key=lambda x: x["vl_spec_total"], reverse=True)
    hpv_candidates.sort(key=lambda x: x["hpv_total"], reverse=True)
    vl_top = vl_candidates[:top_n]
    hpv_top = hpv_candidates[:top_n]

    all_pids = {x["pid"] for x in vl_top} | {x["pid"] for x in hpv_top}
    names = Province.objects.in_bulk(all_pids) if all_pids else {}

    def _prov_label(pid: int) -> str:
        p = names.get(pid)
        return p.name if p else f"Province #{pid}"

    chart_province_vl = {
        "weeks": weeks,
        "labels": [_prov_label(x["pid"]) for x in vl_top],
        "specimens": {
            "vl_plasma": [x["vl_plasma"] for x in vl_top],
            "vl_dbs": [x["vl_dbs"] for x in vl_top],
        },
        "results": {
            "vl_plasma": [x["res_vl_plasma"] for x in vl_top],
            "vl_dbs": [x["res_vl_dbs"] for x in vl_top],
        },
    }
    chart_province_hpv = {
        "weeks": weeks,
        "labels": [_prov_label(x["pid"]) for x in hpv_top],
        "specimens": [x["hpv"] for x in hpv_top],
        "results": [x["res_hpv"] for x in hpv_top],
    }
    return {
        "chart_province_vl": chart_province_vl,
        "chart_province_hpv": chart_province_hpv,
    }


def extend_me_metrics_analytics(
    *,
    start_monday: date,
    end_monday: date,
    labels: list[str],
    weeks: int,
    window: Any,
    all_reports: Any,
) -> dict[str, Any]:
    delivery = _aggregate_trip_specimens_results(start_monday=start_monday, end_monday=end_monday)
    delivery["province_top_specimens"] = _province_specimen_top(start_monday=start_monday, end_monday=end_monday)

    specimen_labels = [
        ("vl_blood_plasma", "VL blood/plasma"),
        ("vl_dbs", "VL DBS"),
        ("eid_blood", "EID blood"),
        ("eid_dbs", "EID DBS"),
        ("sputum", "Sputum"),
        ("sputum_culture_dr", "Sputum culture DR"),
        ("hpv", "HPV"),
    ]
    chart_spec = {
        "labels": [lbl for _, lbl in specimen_labels],
        "values": [delivery["specimens_by_type"][k] for k, _ in specimen_labels],
    }
    chart_res = {
        "labels": [lbl for _, lbl in specimen_labels],
        "values": [delivery["results_by_type"][k] for k, _ in specimen_labels],
    }

    fuel_block = _fuel_distance(start_monday=start_monday, end_monday=end_monday, labels=labels)
    delivery_trends = _weekly_delivery_trends(
        start_monday=start_monday, end_monday=end_monday, labels=labels
    )
    province_charts = _province_delivery_charts(
        start_monday=start_monday,
        end_monday=end_monday,
        weeks=weeks,
    )
    return {
        "delivery": delivery,
        "rejections_window": _rejections_block(start_monday=start_monday, end_monday=end_monday),
        "rejections_all_time": _rejections_block(start_monday=None, end_monday=None),
        "operations_kpis": _operations_kpis(window=window, all_reports=all_reports),
        "fuel_distance": fuel_block,
        "referred_window": _referred_kpis(start_monday=start_monday, end_monday=end_monday),
        "pc_transport_window": _pc_transport(start_monday=start_monday, end_monday=end_monday),
        "chart_delivery": {
            "specimens": chart_spec,
            "results": chart_res,
            "weeks": weeks,
        },
        "chart_fuel_distance": {
            "labels": labels,
            "fuel_allocated": fuel_block["week_fuel_allocated"],
            "fuel_used": fuel_block["week_fuel_used"],
            "distance": fuel_block["week_distance"],
            "weeks": weeks,
        },
        "chart_delivery_trends": {
            "labels": labels,
            "weeks": weeks,
            **delivery_trends,
        },
        **province_charts,
    }
