"""Resolve ``source`` keys from ``me_report_schema`` into display values for one report row."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from decimal import Decimal
from typing import Any

from django.contrib.auth import get_user_model

from ..models import Bike, Car, RiderTripEntry, RiderWeeklyReport, TripVisitPurpose, UserProfile

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
        agg["distance"] += e.distance_travelled or Decimal("0")
        specimens_total += e.specimens_total
        results_total += e.results_total
        if e.visit_purpose == TripVisitPurpose.ADHOC:
            agg["adhoc_row_count"] += 1
            agg["adhoc_specimens"] += e.specimens_total
            agg["adhoc_results"] += e.results_total

    agg["specimens"] = specimens_total
    agg["results"] = results_total
    agg["specimens_other_joined"] = _dedupe_join(agg["specimens_other_parts"])
    agg["results_other_joined"] = _dedupe_join(agg["results_other_parts"])
    del agg["specimens_other_parts"]
    del agg["results_other_parts"]

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
    return _str_or_empty(fn(report))
