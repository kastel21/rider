"""Resolve ``source`` keys from ``me_report_schema`` into display values for one report row."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model

from ..models import Bike, Car, RiderTripEntry, RiderWeeklyReport, RiderWeekFuelSummary, TripVisitPurpose, UserProfile
from .distance_km import distance_km_str
from .other_specify_aggregate import aggregate_other_specify_texts

User = get_user_model()

_NOTES_MAX_LEN = 8000

_TRIP_AGG_ATTR = "_me_report_trip_agg"


def _str_or_empty(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "Yes" if v else "No"
    if isinstance(v, Decimal):
        if v == v.to_integral():
            return str(int(v))
        return format(v, "f").rstrip("0").rstrip(".")
    return str(v)


def _full_name(user: User) -> str:
    name = (user.get_full_name() or "").strip()
    return name or user.get_username()


def _dedupe_join(parts: list[str], sep: str = "; ") -> str:
    seen: list[str] = []
    for p in parts:
        t = (p or "").strip()
        if t and t not in seen:
            seen.append(t)
    return sep.join(seen)


def _trip_aggregate(report: RiderWeeklyReport) -> dict[str, Any]:
    cached = getattr(report, _TRIP_AGG_ATTR, None)
    if cached is not None:
        return cached

    entries: list[RiderTripEntry] = list(report.trip_entries.all())
    agg: dict[str, Any] = {
        "count": len(entries),
        "vl_blood_plasma": 0,
        "vl_dbs": 0,
        "eid_blood": 0,
        "eid_dbs": 0,
        "sputum": 0,
        "sputum_culture_dr": 0,
        "hpv": 0,
        "specimens_other_parts": [],
        "results_vl_blood_plasma": 0,
        "results_vl_dbs": 0,
        "results_eid_blood": 0,
        "results_eid_dbs": 0,
        "results_sputum": 0,
        "results_sputum_culture_dr": 0,
        "results_hpv": 0,
        "results_other_parts": [],
        "fuel_allocated": Decimal("0"),
        "fuel_used": Decimal("0"),
        "distance": Decimal("0"),
        "adhoc_row_count": 0,
        "adhoc_specimens": 0,
        "adhoc_results": 0,
    }
    specimens_total = 0
    results_total = 0
    for e in entries:
        agg["vl_blood_plasma"] += e.vl_blood_plasma or 0
        agg["vl_dbs"] += e.vl_dbs or 0
        agg["eid_blood"] += e.eid_blood or 0
        agg["eid_dbs"] += e.eid_dbs or 0
        agg["sputum"] += e.sputum or 0
        agg["sputum_culture_dr"] += e.sputum_culture_dr or 0
        agg["hpv"] += e.hpv or 0
        if (e.specimens_other_specify or "").strip():
            agg["specimens_other_parts"].append(e.specimens_other_specify.strip())
        agg["results_vl_blood_plasma"] += e.results_vl_blood_plasma or 0
        agg["results_vl_dbs"] += e.results_vl_dbs or 0
        agg["results_eid_blood"] += e.results_eid_blood or 0
        agg["results_eid_dbs"] += e.results_eid_dbs or 0
        agg["results_sputum"] += e.results_sputum or 0
        agg["results_sputum_culture_dr"] += e.results_sputum_culture_dr or 0
        agg["results_hpv"] += e.results_hpv or 0
        if (e.results_other_specify or "").strip():
            agg["results_other_parts"].append(e.results_other_specify.strip())
        agg["fuel_allocated"] += e.fuel_allocated or Decimal("0")
        agg["fuel_used"] += e.fuel_used or Decimal("0")
        specimens_total += e.specimens_total
        results_total += e.results_total
        if e.visit_purpose == TripVisitPurpose.ADHOC:
            agg["adhoc_row_count"] += 1
            agg["adhoc_specimens"] += e.specimens_total
            agg["adhoc_results"] += e.results_total

    agg["specimens"] = specimens_total
    agg["results"] = results_total
    agg["specimens_other_joined"] = aggregate_other_specify_texts(agg["specimens_other_parts"])
    agg["results_other_joined"] = aggregate_other_specify_texts(agg["results_other_parts"])
    del agg["specimens_other_parts"]
    del agg["results_other_parts"]

    fw = (
        RiderWeekFuelSummary.objects.filter(rider_id=report.rider_id, week_start=report.week_start)
        .only("fuel_allocated", "fuel_used")
        .first()
    )
    if fw is not None:
        agg["fuel_allocated"] = fw.fuel_allocated or Decimal("0")
        agg["fuel_used"] = fw.fuel_used or Decimal("0")
    agg["distance"] = report.distance_travelled or Decimal("0")

    setattr(report, _TRIP_AGG_ATTR, agg)
    return agg


def _bike_or_car(report: RiderWeeklyReport) -> str:
    if report.bike_id and report.bike:
        return report.bike.code
    if report.car_id and report.car:
        return report.car.code
    return ""


def _snp_vehicle(report: RiderWeeklyReport) -> Bike | Car | None:
    if report.bike_id and report.bike:
        return report.bike
    if report.car_id and report.car:
        return report.car
    rp = getattr(report.rider, "rider_profile", None)
    if not rp:
        return None
    if rp.bike_id and getattr(rp, "bike", None):
        return rp.bike
    if rp.car_id and getattr(rp, "car", None):
        return rp.car
    return None


def _role_display(report: RiderWeeklyReport) -> str:
    p = getattr(report.rider, "profile", None)
    if not p:
        return ""
    role = getattr(p, "role", None)
    if not role:
        return ""
    try:
        return UserProfile.Role(role).label
    except ValueError:
        return str(role)


def _role_value_lower(report: RiderWeeklyReport) -> str:
    p = getattr(report.rider, "profile", None)
    if not p or not getattr(p, "role", None):
        return ""
    return str(p.role).lower()


def _profile_facility(report: RiderWeeklyReport) -> str:
    rp = getattr(report.rider, "rider_profile", None)
    if not rp or not rp.facility_id:
        return ""
    return rp.facility.name


def _profile_district(report: RiderWeeklyReport) -> str:
    rp = getattr(report.rider, "rider_profile", None)
    if not rp or not rp.district_id:
        return ""
    return rp.district.name


def _profile_province(report: RiderWeeklyReport) -> str:
    rp = getattr(report.rider, "rider_profile", None)
    if not rp:
        return ""
    if rp.province_id:
        return rp.province.name
    if rp.district_id and rp.district and rp.district.province_id:
        return rp.district.province.name
    return ""


def _support_type_display(report: RiderWeeklyReport) -> str:
    rp = getattr(report.rider, "rider_profile", None)
    if not rp or not (rp.support_type or "").strip():
        return ""
    return rp.get_support_type_display()


def _relief_rider_name(report: RiderWeeklyReport) -> str:
    ex = report.extra_data or {}
    if not isinstance(ex, dict):
        return ""
    return (
        str(ex.get("relief_rider_name") or ex.get("reliefRiderName") or ex.get("relief_rider") or "")
        .strip()
    )


def _days_bike_functional(report: RiderWeeklyReport) -> str:
    ex = report.extra_data or {}
    if isinstance(ex, dict):
        for k in ("days_bike_functional", "bike_functional_days", "days_bike_was_functional"):
            v = ex.get(k)
            if v is not None and str(v).strip() != "":
                return str(v).strip()
    return ""


def _days_vehicle_functional(report: RiderWeeklyReport) -> str:
    ex = report.extra_data or {}
    if isinstance(ex, dict):
        for k in (
            "days_vehicle_functional",
            "days_vehicle_was_functional",
            "vehicle_functional_days",
            "days_bike_functional",
            "bike_functional_days",
        ):
            v = ex.get(k)
            if v is not None and str(v).strip() != "":
                return str(v).strip()
    return ""


def _dominant_transport_kind_label(report: RiderWeeklyReport) -> str:
    entries = list(report.trip_entries.all())
    if not entries:
        return ""
    kinds: list[str] = []
    for e in entries:
        k = (e.transport_kind or "").strip()
        kinds.append(k if k else "__empty__")
    winner, _ = Counter(kinds).most_common(1)[0]
    if winner == "__empty__":
        return ""
    try:
        return RiderTripEntry.TransportKind(winner).label
    except ValueError:
        return winner


def _snp_int(vehicle: Bike | Car | None, attr: str) -> int:
    if vehicle is None:
        return 0
    return int(getattr(vehicle, attr, 0) or 0)


def _snp_other_specify(report: RiderWeeklyReport) -> str:
    v = _snp_vehicle(report)
    if v is None:
        return ""
    return (getattr(v, "snp_other_specify", "") or "").strip()


def _mitigation(report: RiderWeeklyReport) -> str:
    v = _snp_vehicle(report)
    if v is None:
        return ""
    return (getattr(v, "mitigation_measures", "") or "").strip()


def _comments(report: RiderWeeklyReport) -> str:
    return (report.notes or "").strip()[:_NOTES_MAX_LEN]


def _date_week_sunday(report: RiderWeeklyReport) -> str:
    from ..selectors import sunday_of_week

    if not report.week_start:
        return ""
    return sunday_of_week(report.week_start).strftime("%d/%m/%Y")


def _week_label(report: RiderWeeklyReport) -> str:
    if not report.week_start:
        return ""
    y, w, _ = report.week_start.isocalendar()
    return f"{y}-W{w:02d}"


SOURCE_RESOLVERS: dict[str, Callable[[RiderWeeklyReport], Any]] = {
    "rider.full_name": lambda r: _full_name(r.rider),
    "profile.role_lower": _role_value_lower,
    "extra.relief_rider_name": _relief_rider_name,
    "report.bike_or_car": _bike_or_car,
    "profile.province_name": _profile_province,
    "profile.district_name": _profile_district,
    "profile.support_type_display": _support_type_display,
    "trip.vl_blood_plasma": lambda r: _trip_aggregate(r)["vl_blood_plasma"],
    "trip.vl_dbs": lambda r: _trip_aggregate(r)["vl_dbs"],
    "trip.eid_blood": lambda r: _trip_aggregate(r)["eid_blood"],
    "trip.eid_dbs": lambda r: _trip_aggregate(r)["eid_dbs"],
    "trip.sputum": lambda r: _trip_aggregate(r)["sputum"],
    "trip.sputum_culture_dr": lambda r: _trip_aggregate(r)["sputum_culture_dr"],
    "trip.hpv": lambda r: _trip_aggregate(r)["hpv"],
    "trip.specimens_other_joined": lambda r: _trip_aggregate(r)["specimens_other_joined"],
    "trip.results_vl_blood_plasma": lambda r: _trip_aggregate(r)["results_vl_blood_plasma"],
    "trip.results_vl_dbs": lambda r: _trip_aggregate(r)["results_vl_dbs"],
    "trip.results_eid_blood": lambda r: _trip_aggregate(r)["results_eid_blood"],
    "trip.results_eid_dbs": lambda r: _trip_aggregate(r)["results_eid_dbs"],
    "trip.results_sputum": lambda r: _trip_aggregate(r)["results_sputum"],
    "trip.results_sputum_culture_dr": lambda r: _trip_aggregate(r)["results_sputum_culture_dr"],
    "trip.results_hpv": lambda r: _trip_aggregate(r)["results_hpv"],
    "trip.results_other_joined": lambda r: _trip_aggregate(r)["results_other_joined"],
    "trip.fuel_allocated_total": lambda r: _trip_aggregate(r)["fuel_allocated"],
    "trip.fuel_used_total": lambda r: _trip_aggregate(r)["fuel_used"],
    "trip.distance_total": lambda r: _trip_aggregate(r)["distance"],
    "report.days_bike_functional": _days_bike_functional,
    "report.days_vehicle_functional": _days_vehicle_functional,
    "trip.dominant_transport_kind_label": _dominant_transport_kind_label,
    "report.scheduled_visits": lambda r: r.scheduled_visits if r.scheduled_visits is not None else "",
    "trip.actual_visit_row_count": lambda r: _trip_aggregate(r)["count"],
    "trip.adhoc_visit_row_count": lambda r: _trip_aggregate(r)["adhoc_row_count"],
    "trip.adhoc_specimens_total": lambda r: _trip_aggregate(r)["adhoc_specimens"],
    "trip.adhoc_results_total": lambda r: _trip_aggregate(r)["adhoc_results"],
    "vehicle.snp_bike_breakdown": lambda r: _snp_int(_snp_vehicle(r), "snp_bike_breakdown"),
    "vehicle.snp_bike_routine_service": lambda r: _snp_int(_snp_vehicle(r), "snp_bike_routine_service"),
    "vehicle.snp_bike_no_fuel": lambda r: _snp_int(_snp_vehicle(r), "snp_bike_no_fuel"),
    "vehicle.snp_rider_sick_leave": lambda r: _snp_int(_snp_vehicle(r), "snp_rider_sick_leave"),
    "vehicle.snp_rider_annual_leave": lambda r: _snp_int(_snp_vehicle(r), "snp_rider_annual_leave"),
    "vehicle.snp_inclement_weather": lambda r: _snp_int(_snp_vehicle(r), "snp_inclement_weather"),
    "vehicle.snp_bike_accident": lambda r: _snp_int(_snp_vehicle(r), "snp_bike_accident"),
    "vehicle.snp_clinical_ip": lambda r: _snp_int(_snp_vehicle(r), "snp_clinical_ip"),
    "vehicle.snp_other_specify": _snp_other_specify,
    "vehicle.mitigation_measures": _mitigation,
    "report.notes_full": _comments,
    "report.week_end_date_dmY": _date_week_sunday,
    "report.iso_week_label": _week_label,
    "report.average_datalogger_temperature": lambda r: (
        r.average_datalogger_temperature if r.average_datalogger_temperature is not None else ""
    ),
    # Legacy keys (older schema / callers)
    "report.id": lambda r: r.pk,
    "profile.role_display": _role_display,
    "profile.facility_name": _profile_facility,
    "report.week_start": lambda r: r.week_start.isoformat() if r.week_start else "",
    "report.status_display": lambda r: r.get_status_display() if r.status else "",
    "report.samples_collected": lambda r: r.samples_collected,
    "report.trip_entry_count": lambda r: _trip_aggregate(r)["count"],
    "report.specimens_from_trips": lambda r: _trip_aggregate(r)["specimens"],
    "report.results_from_trips": lambda r: _trip_aggregate(r)["results"],
    "report.fuel_used_total": lambda r: _trip_aggregate(r)["fuel_used"],
    "report.distance_total": lambda r: _trip_aggregate(r)["distance"],
    "report.notes_excerpt": lambda r: _comments(r)[:240],
    "report.pc_notes_excerpt": lambda r: (r.pc_notes or "").strip()[:240],
    "report.submitted_at": lambda r: r.submitted_at.strftime("%Y-%m-%d %H:%M") if r.submitted_at else "",
    "report.title": lambda r: (r.title or "").strip(),
}


def resolve_cell(report: RiderWeeklyReport, source: str | None) -> str:
    if not source:
        return ""
    fn = SOURCE_RESOLVERS.get(source)
    if not fn:
        return ""
    val = fn(report)
    if source in ("trip.distance_total", "report.distance_total"):
        return distance_km_str(val)
    return _str_or_empty(val)


def _trip_aggregate_many(
    reports: list[RiderWeeklyReport],
    *,
    vehicle_scoped: bool = False,
) -> dict[str, Any]:
    """Sum trip rows across reports.

    When ``vehicle_scoped`` is true (rider + bike grouping), fuel/distance are summed from
    trip rows and report fields only — not the rider-week fuel summary.
    """
    agg: dict[str, Any] = {
        "count": 0,
        "vl_blood_plasma": 0,
        "vl_dbs": 0,
        "eid_blood": 0,
        "eid_dbs": 0,
        "sputum": 0,
        "sputum_culture_dr": 0,
        "hpv": 0,
        "specimens_other_parts": [],
        "results_vl_blood_plasma": 0,
        "results_vl_dbs": 0,
        "results_eid_blood": 0,
        "results_eid_dbs": 0,
        "results_sputum": 0,
        "results_sputum_culture_dr": 0,
        "results_hpv": 0,
        "results_other_parts": [],
        "fuel_allocated": Decimal("0"),
        "fuel_used": Decimal("0"),
        "distance": Decimal("0"),
        "adhoc_row_count": 0,
        "adhoc_specimens": 0,
        "adhoc_results": 0,
    }
    for report in reports:
        for e in report.trip_entries.all():
            agg["vl_blood_plasma"] += e.vl_blood_plasma or 0
            agg["vl_dbs"] += e.vl_dbs or 0
            agg["eid_blood"] += e.eid_blood or 0
            agg["eid_dbs"] += e.eid_dbs or 0
            agg["sputum"] += e.sputum or 0
            agg["sputum_culture_dr"] += e.sputum_culture_dr or 0
            agg["hpv"] += e.hpv or 0
            if (e.specimens_other_specify or "").strip():
                agg["specimens_other_parts"].append(e.specimens_other_specify.strip())
            agg["results_vl_blood_plasma"] += e.results_vl_blood_plasma or 0
            agg["results_vl_dbs"] += e.results_vl_dbs or 0
            agg["results_eid_blood"] += e.results_eid_blood or 0
            agg["results_eid_dbs"] += e.results_eid_dbs or 0
            agg["results_sputum"] += e.results_sputum or 0
            agg["results_sputum_culture_dr"] += e.results_sputum_culture_dr or 0
            agg["results_hpv"] += e.results_hpv or 0
            if (e.results_other_specify or "").strip():
                agg["results_other_parts"].append(e.results_other_specify.strip())
            if e.visit_purpose == TripVisitPurpose.ADHOC:
                agg["adhoc_row_count"] += 1
                agg["adhoc_specimens"] += e.specimens_total
                agg["adhoc_results"] += e.results_total
            agg["count"] += 1

    agg["specimens_other_joined"] = aggregate_other_specify_texts(agg["specimens_other_parts"])
    agg["results_other_joined"] = aggregate_other_specify_texts(agg["results_other_parts"])

    if vehicle_scoped:
        for report in reports:
            for e in report.trip_entries.all():
                agg["fuel_allocated"] += e.fuel_allocated or Decimal("0")
                agg["fuel_used"] += e.fuel_used or Decimal("0")
                agg["distance"] += e.distance_travelled or Decimal("0")
        report_dist = sum(
            (r.distance_travelled or Decimal("0") for r in reports),
            Decimal("0"),
        )
        if report_dist > agg["distance"]:
            agg["distance"] = report_dist
    else:
        rider_id = reports[0].rider_id
        week_start = reports[0].week_start
        fw = (
            RiderWeekFuelSummary.objects.filter(rider_id=rider_id, week_start=week_start)
            .only("fuel_allocated", "fuel_used", "distance_travelled")
            .first()
        )
        if fw is not None:
            agg["fuel_allocated"] = fw.fuel_allocated or Decimal("0")
            agg["fuel_used"] = fw.fuel_used or Decimal("0")
            agg["distance"] = fw.distance_travelled or Decimal("0")
        else:
            dists = [r.distance_travelled for r in reports if r.distance_travelled is not None]
            agg["distance"] = max(dists) if dists else Decimal("0")

    return agg


def _max_days_functional(reports: list[RiderWeeklyReport], *, bike: bool) -> str:
    nums: list[int] = []
    for r in reports:
        raw = _days_bike_functional(r) if bike else _days_vehicle_functional(r)
        if raw and str(raw).strip().isdigit():
            nums.append(int(str(raw).strip()))
    return str(max(nums)) if nums else ""


def resolve_cell_group(
    reports: list[RiderWeeklyReport],
    source: str | None,
    *,
    vehicle_scoped: bool = False,
) -> str:
    """
    One export cell for reports in the same rider + bike/vehicle + Monday week group.
    Numeric trip counts and visits are summed. Fuel uses week summary when not vehicle-scoped.
    """
    if not source or not reports:
        return ""

    primary = max(reports, key=lambda r: r.id)
    week_start = primary.week_start

    if source in (
        "rider.full_name",
        "profile.role_lower",
        "profile.role_display",
        "profile.province_name",
        "profile.district_name",
        "profile.support_type_display",
        "profile.facility_name",
    ):
        return resolve_cell(primary, source)

    if source == "extra.relief_rider_name":
        return _dedupe_join([_relief_rider_name(r) for r in reports])

    if source == "report.bike_or_car":
        return _bike_or_car(primary)

    if source == "report.scheduled_visits":
        return _str_or_empty(sum(int(r.scheduled_visits or 0) for r in reports))

    if source == "report.days_bike_functional":
        return _max_days_functional(reports, bike=True)

    if source == "report.days_vehicle_functional":
        return _max_days_functional(reports, bike=False)

    if source == "report.average_datalogger_temperature":
        temps = [
            r.average_datalogger_temperature
            for r in reports
            if r.average_datalogger_temperature is not None
        ]
        if not temps:
            return ""
        return _str_or_empty(round(sum(temps) / len(temps)))

    if source == "report.notes_full":
        parts = [_comments(r) for r in reports]
        return _dedupe_join([p for p in parts if p])[:_NOTES_MAX_LEN]

    if source == "report.week_end_date_dmY":
        from ..selectors import sunday_of_week

        return sunday_of_week(week_start).strftime("%d/%m/%Y") if week_start else ""

    if source == "report.iso_week_label":
        if not week_start:
            return ""
        y, w, _ = week_start.isocalendar()
        return f"{y}-W{w:02d}"

    if source.startswith("vehicle."):
        return resolve_cell(primary, source)

    if source == "trip.dominant_transport_kind_label":
        return resolve_cell(primary, source)

    trip = _trip_aggregate_many(reports, vehicle_scoped=vehicle_scoped)
    trip_sources = {
        "trip.vl_blood_plasma": "vl_blood_plasma",
        "trip.vl_dbs": "vl_dbs",
        "trip.eid_blood": "eid_blood",
        "trip.eid_dbs": "eid_dbs",
        "trip.sputum": "sputum",
        "trip.sputum_culture_dr": "sputum_culture_dr",
        "trip.hpv": "hpv",
        "trip.specimens_other_joined": "specimens_other_joined",
        "trip.results_vl_blood_plasma": "results_vl_blood_plasma",
        "trip.results_vl_dbs": "results_vl_dbs",
        "trip.results_eid_blood": "results_eid_blood",
        "trip.results_eid_dbs": "results_eid_dbs",
        "trip.results_sputum": "results_sputum",
        "trip.results_sputum_culture_dr": "results_sputum_culture_dr",
        "trip.results_hpv": "results_hpv",
        "trip.results_other_joined": "results_other_joined",
        "trip.fuel_allocated_total": "fuel_allocated",
        "trip.fuel_used_total": "fuel_used",
        "trip.distance_total": "distance",
        "trip.actual_visit_row_count": "count",
        "trip.adhoc_visit_row_count": "adhoc_row_count",
        "trip.adhoc_specimens_total": "adhoc_specimens",
        "trip.adhoc_results_total": "adhoc_results",
    }
    if source in trip_sources:
        key = trip_sources[source]
        if key == "distance":
            return distance_km_str(trip[key])
        return _str_or_empty(trip[key])

    return resolve_cell(primary, source)
