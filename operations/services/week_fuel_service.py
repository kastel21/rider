"""Week-level fuel: trip rollup helpers, per-rider weekly RiderWeekFuelSummary, and report-level distance."""

from decimal import Decimal, InvalidOperation

from django.db.models import Sum

from ..models import RiderTripEntry, RiderWeeklyReport, RiderWeekFuelSummary


def week_fuel_alloc_used_from_report(report: RiderWeeklyReport) -> tuple[Decimal, Decimal]:
    """Week fuel allocated/used: prefer RiderWeekFuelSummary; else sum trip rows."""
    row = (
        RiderWeekFuelSummary.objects.filter(rider_id=report.rider_id, week_start=report.week_start)
        .only("fuel_allocated", "fuel_used")
        .first()
    )
    if row is not None:
        fa = row.fuel_allocated if row.fuel_allocated is not None else Decimal("0")
        fu = row.fuel_used if row.fuel_used is not None else Decimal("0")
        return (fa, fu)
    s = report.trip_entries.aggregate(a=Sum("fuel_allocated"), u=Sum("fuel_used"))
    fa = s["a"] if s["a"] is not None else Decimal("0")
    fu = s["u"] if s["u"] is not None else Decimal("0")
    return (fa, fu)


def week_fuel_totals_from_db(report: RiderWeeklyReport) -> dict:
    s = report.trip_entries.aggregate(
        a=Sum("fuel_allocated"),
        u=Sum("fuel_used"),
        d=Sum("distance_travelled"),
    )
    return {
        "allocated": str(s["a"] if s["a"] is not None else Decimal("0")),
        "used": str(s["u"] if s["u"] is not None else Decimal("0")),
        "distance": str(s["d"] if s["d"] is not None else Decimal("0")),
    }


def week_fuel_totals_for_report(report: RiderWeeklyReport) -> dict:
    """Fuel from week summary or trip sums; distance from this weekly report record."""
    fa, fu = week_fuel_alloc_used_from_report(report)
    dt = report.distance_travelled if report.distance_travelled is not None else Decimal("0")
    return {"allocated": str(fa), "used": str(fu), "distance": str(dt)}


def rider_week_fuel_totals_for_user_week(rider_id: int, week_start) -> dict:
    """Fuel totals from RiderWeekFuelSummary; distance is no longer captured on the week fuel page."""
    row = RiderWeekFuelSummary.objects.filter(rider_id=rider_id, week_start=week_start).first()
    if row is None:
        return {"allocated": "0", "used": "0", "distance": "0"}
    fa = row.fuel_allocated if row.fuel_allocated is not None else Decimal("0")
    fu = row.fuel_used if row.fuel_used is not None else Decimal("0")
    return {"allocated": str(fa), "used": str(fu), "distance": "0"}


def upsert_rider_week_fuel_summary(
    rider_id: int,
    week_start,
    fuel_allocated: Decimal,
    fuel_used: Decimal,
) -> None:
    RiderWeekFuelSummary.objects.update_or_create(
        rider_id=rider_id,
        week_start=week_start,
        defaults={
            "fuel_allocated": fuel_allocated,
            "fuel_used": fuel_used,
            "distance_travelled": Decimal("0"),
        },
    )


def week_fuel_decimals_from_report(report: RiderWeeklyReport) -> tuple[Decimal, Decimal, Decimal]:
    fa, fu = week_fuel_alloc_used_from_report(report)
    dt = report.distance_travelled if report.distance_travelled is not None else Decimal("0")
    return (fa, fu, dt)


def week_fuel_totals_from_pc_post(post) -> dict:
    return {
        "allocated": (post.get("pc_fuel_allocated_total") or "0").strip(),
        "used": (post.get("pc_fuel_used_total") or "0").strip(),
        "distance": "0",
    }


def parse_week_fuel_pc_post(post) -> tuple[Decimal, Decimal]:
    def one(key: str) -> Decimal:
        raw = (post.get(key) or "").strip().replace(",", ".")
        if not raw:
            return Decimal("0")
        try:
            return Decimal(raw)
        except InvalidOperation as e:
            raise ValueError("Enter a valid number for week fuel totals.") from e

    return (one("pc_fuel_allocated_total"), one("pc_fuel_used_total"))


def apply_week_fuel_distance_rollup(
    report: RiderWeeklyReport,
    fuel_allocated: Decimal,
    fuel_used: Decimal,
) -> None:
    distance = report.distance_travelled if report.distance_travelled is not None else Decimal("0")
    qs = report.trip_entries.order_by("sequence", "pk")
    first = qs.first()
    if not first:
        return
    RiderTripEntry.objects.filter(pk=first.pk).update(
        fuel_allocated=fuel_allocated,
        fuel_used=fuel_used,
        distance_travelled=distance,
    )
    rest_ids = list(qs.exclude(pk=first.pk).values_list("pk", flat=True))
    if rest_ids:
        RiderTripEntry.objects.filter(pk__in=rest_ids).update(
            fuel_allocated=Decimal("0"),
            fuel_used=Decimal("0"),
            distance_travelled=Decimal("0"),
        )


def bulk_week_fuel_totals_key(report_id: int, field: str) -> str:
    return f"pc_{field}_total_{report_id}"


def week_fuel_totals_from_bulk_post(post, report_id: int) -> dict:
    return {
        "allocated": (post.get(bulk_week_fuel_totals_key(report_id, "fuel_allocated")) or "0").strip(),
        "used": (post.get(bulk_week_fuel_totals_key(report_id, "fuel_used")) or "0").strip(),
        "distance": "0",
    }


def parse_week_fuel_bulk_post(post, report_id: int) -> tuple[Decimal, Decimal]:
    def one(key: str) -> Decimal:
        raw = (post.get(key) or "").strip().replace(",", ".")
        if not raw:
            return Decimal("0")
        try:
            return Decimal(raw)
        except InvalidOperation as e:
            raise ValueError("Enter a valid number for week fuel totals.") from e

    return (
        one(bulk_week_fuel_totals_key(report_id, "fuel_allocated")),
        one(bulk_week_fuel_totals_key(report_id, "fuel_used")),
    )


def ensure_anchor_trip_for_fuel(report: RiderWeeklyReport) -> RiderTripEntry | None:
    """Ensure at least one trip row exists so week fuel rollup can persist."""
    if report.trip_entries.exists():
        return report.trip_entries.order_by("sequence", "pk").first()
    return RiderTripEntry.objects.create(
        report=report,
        sequence=1,
    )
