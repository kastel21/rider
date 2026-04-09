from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Q, QuerySet
from django.utils import timezone

from .models import (
    Bike,
    Car,
    District,
    Facility,
    PCProfile,
    Province,
    ReferredSample,
    ReportAuditLog,
    RiderProfile,
    RiderTripEntry,
    RiderWeeklyReport,
    UserProfile,
)


def sunday_of_week(week_start_monday: date) -> date:
    """Week runs Monday through the following Sunday."""
    return week_start_monday + timedelta(days=6)


def week_saved_trip_entries(*, report, rider, week_start_monday: date) -> QuerySet:
    """Persisted trip rows for the weekly report period (same Mon–Sun as week_start)."""
    if report is not None and getattr(report, "pk", None):
        return (
            report.trip_entries.select_related("origin_facility", "destination_facility").order_by(
                "sequence", "id"
            )
        )
    rider_id = getattr(rider, "pk", rider)
    return (
        RiderTripEntry.objects.filter(report__rider_id=rider_id, report__week_start=week_start_monday)
        .select_related("origin_facility", "destination_facility")
        .order_by("sequence", "id")
    )


def week_range_label(week_start_monday: date) -> str:
    """Human-readable Mon–Sun range for display."""
    end = sunday_of_week(week_start_monday)
    return (
        f"{week_start_monday.strftime('%a %d %b')} – {end.strftime('%a %d %b %Y')}"
    )


def monday_of_local_today() -> date:
    """Monday of the calendar week containing the current local date."""
    d = timezone.localdate()
    return d - timedelta(days=d.weekday())


def monday_of_week_containing(day: date) -> date:
    """Monday of the calendar week containing ``day`` (Mon–Sun)."""
    return day - timedelta(days=day.weekday())


def week_start_from_request(request) -> date:
    """
    Parse optional ``?week=YYYY-MM-DD`` (any day in the week); return that week's Monday.
    Falls back to the current week's Monday if missing or invalid.
    """
    raw = (request.GET.get("week") or "").strip()
    if not raw:
        return monday_of_local_today()
    try:
        d = date.fromisoformat(raw[:10])
    except ValueError:
        return monday_of_local_today()
    return monday_of_week_containing(d)


def rider_home_profile_metrics(user) -> dict:
    """Summary about the rider for the home dashboard (all-time counts)."""
    if not user or not getattr(user, "is_authenticated", False):
        return {}
    rp = getattr(user, "rider_profile", None)
    district = getattr(rp, "district", None) if rp else None
    province = getattr(district, "province", None) if district else None
    qs = RiderWeeklyReport.objects.filter(rider=user)
    profile = getattr(user, "profile", None)
    role_display = profile.get_role_display() if profile else ""
    joined = getattr(user, "date_joined", None)
    return {
        "display_name": user.get_full_name() or user.username,
        "district": getattr(district, "name", None) or "—",
        "province": getattr(province, "name", None) or "—",
        "role_display": role_display,
        "member_since": joined.date() if joined else None,
        "total_reports": qs.count(),
        "approved_reports": qs.filter(status=RiderWeeklyReport.Status.APPROVED).count(),
        "submitted_pending": qs.filter(
            status__in=(
                RiderWeeklyReport.Status.SUBMITTED,
                RiderWeeklyReport.Status.UNDER_REVIEW,
            )
        ).count(),
    }


def rider_home_weekly_trends(user, *, num_weeks: int = 12) -> dict:
    """
    Per-week series for charts (oldest → newest Monday).
    Missing weeks are filled with zeros.
    """
    labels: list[str] = []
    samples: list[int] = []
    trips: list[int] = []
    distance_km: list[float] = []

    end_monday = monday_of_local_today()
    start_monday = end_monday - timedelta(weeks=num_weeks - 1)

    reports = (
        RiderWeeklyReport.objects.filter(
            rider=user,
            week_start__gte=start_monday,
            week_start__lte=end_monday,
        )
        .order_by("week_start")
        .prefetch_related("trip_entries")
    )
    by_week = {r.week_start: r for r in reports}

    d = start_monday
    for _ in range(num_weeks):
        labels.append(d.strftime("%Y-%m-%d"))
        r = by_week.get(d)
        if r:
            tr = list(r.trip_entries.all())
            samples.append(int(r.samples_collected or 0))
            trips.append(len(tr))
            dist = sum(
                (x.distance_travelled if x.distance_travelled is not None else Decimal("0") for x in tr),
                Decimal("0"),
            )
            distance_km.append(float(dist))
        else:
            samples.append(0)
            trips.append(0)
            distance_km.append(0.0)
        d += timedelta(days=7)

    return {
        "labels": labels,
        "samples": samples,
        "trips": trips,
        "distance_km": distance_km,
    }


def bikes_queryset_for_rider_district(rider_user) -> QuerySet:
    """Active bikes registered in the rider's district (report bike dropdown)."""
    if not rider_user or not getattr(rider_user, "is_authenticated", False):
        return Bike.objects.none()
    rp = getattr(rider_user, "rider_profile", None)
    if not rp or not rp.district_id:
        return Bike.objects.none()
    return Bike.objects.filter(district_id=rp.district_id, active=True).order_by("code")


def cars_queryset_for_driver(driver_user) -> QuerySet:
    """Active cars the driver may select: assigned vehicle and/or vehicles in the driver's district."""
    if not driver_user or not getattr(driver_user, "is_authenticated", False):
        return Car.objects.none()
    rp = getattr(driver_user, "rider_profile", None)
    if not rp:
        return Car.objects.none()
    qs = Car.objects.filter(active=True)
    if rp.district_id:
        return (
            qs.filter(Q(district_id=rp.district_id) | Q(pk=rp.car_id))
            .distinct()
            .order_by("code")
        )
    if rp.car_id:
        return qs.filter(pk=rp.car_id).order_by("code")
    return Car.objects.none()


def pc_province_ids(user) -> list[int]:
    """Province PKs assigned to this user as PC. Empty if not a PC or no profile."""
    if not user.is_authenticated:
        return []
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return []
    if profile.role != UserProfile.Role.PC:
        return []
    try:
        pc = user.pc_profile
    except PCProfile.DoesNotExist:
        return []
    return list(pc.provinces.values_list("id", flat=True))


def reports_in_pc_scope(user) -> QuerySet:
    """
    Reports visible to a PC: rider's district province in assigned provinces, or (drivers
    only) province on profile when district is unset — same rule as get_drivers_queryset.
    """
    ids = pc_province_ids(user)
    if not ids:
        return RiderWeeklyReport.objects.none()
    return (
        RiderWeeklyReport.objects.filter(
            Q(rider__rider_profile__district__province_id__in=ids)
            | Q(
                rider__profile__role=UserProfile.Role.DRIVER,
                rider__rider_profile__district__isnull=True,
                rider__rider_profile__province_id__in=ids,
            )
        )
        .select_related("rider")
        .distinct()
    )


def reports_for_user(user) -> QuerySet:
    if not user.is_authenticated:
        return RiderWeeklyReport.objects.none()
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return RiderWeeklyReport.objects.none()

    qs = RiderWeeklyReport.objects.select_related("rider")
    if profile.role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER):
        return qs.filter(rider=user)
    if profile.role == UserProfile.Role.ME:
        return qs
    if profile.role == UserProfile.Role.ADMIN:
        return qs
    if profile.role == UserProfile.Role.PC:
        return reports_in_pc_scope(user)
    return RiderWeeklyReport.objects.none()


def get_reports_queryset(user) -> QuerySet:
    """docs/operations-compatible selector name."""
    return reports_for_user(user)


def facilities_for_ajax(user, district_id=None) -> QuerySet:
    qs = Facility.objects.select_related("district", "district__province").order_by("name")
    if district_id:
        qs = qs.filter(district_id=district_id)

    if not user.is_authenticated:
        return qs.none()
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return qs

    if profile.role == UserProfile.Role.PC:
        pids = pc_province_ids(user)
        if not pids:
            return qs.none()
        qs = qs.filter(district__province_id__in=pids)
    return qs


def get_provinces_queryset(user) -> QuerySet:
    if not user.is_authenticated:
        return Province.objects.none()
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return Province.objects.none()
    if profile.role in (UserProfile.Role.ADMIN, UserProfile.Role.ME):
        return Province.objects.all()
    if profile.role == UserProfile.Role.PC:
        return Province.objects.filter(id__in=pc_province_ids(user))
    return Province.objects.none()


def get_districts_queryset(user, province_id=None) -> QuerySet:
    qs = District.objects.filter(province__in=get_provinces_queryset(user))
    if province_id:
        qs = qs.filter(province_id=province_id)
    return qs


def get_facilities_queryset(user, district_id=None) -> QuerySet:
    qs = Facility.objects.filter(district__in=get_districts_queryset(user))
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_bikes_queryset(user, district_id=None) -> QuerySet:
    """Bikes registered in districts within the user's scope (e.g. PC provinces)."""
    qs = Bike.objects.filter(district__in=get_districts_queryset(user)).select_related("district")
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs.order_by("code")


def get_cars_queryset(user, district_id=None, province_id=None) -> QuerySet:
    """
    Cars in scoped districts, plus cars linked to drivers in the PC's provinces
    when the car has no district (same pattern as driver roster visibility).
    """
    try:
        actor_profile = user.profile
    except UserProfile.DoesNotExist:
        return Car.objects.none()

    district_qs = get_districts_queryset(user, province_id=province_id)
    qs = Car.objects.select_related("district", "district__province")

    if actor_profile.role == UserProfile.Role.PC:
        pids = pc_province_ids(user)
        if not pids:
            return Car.objects.none()
        driver_car_pks = (
            RiderProfile.objects.filter(
                user__profile__role=UserProfile.Role.DRIVER,
                car__isnull=False,
            )
            .filter(
                Q(district__province_id__in=pids) | Q(district__isnull=True, province_id__in=pids)
            )
            .values_list("car_id", flat=True)
        )
        qs = qs.filter(Q(district__in=district_qs) | Q(pk__in=driver_car_pks))
    elif actor_profile.role in (UserProfile.Role.ADMIN, UserProfile.Role.ME):
        qs = qs.filter(Q(district__in=district_qs) | Q(district__isnull=True))
    else:
        return Car.objects.none()

    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs.order_by("code")


def get_riders_queryset(user, district_id=None, province_id=None) -> QuerySet:
    qs = RiderProfile.objects.filter(
        district__in=get_districts_queryset(user, province_id=province_id),
        user__profile__role=UserProfile.Role.RIDER,
    )
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs.select_related(
        "user",
        "user__profile",
        "district",
        "district__province",
        "facility",
        "bike",
    )


def get_drivers_queryset(user, district_id=None, province_id=None) -> QuerySet:
    """
    Drivers use the same RiderProfile model as riders. Many drivers only have ``province``
    set (no district); scope them by province for PCs instead of requiring a district row.
    """
    try:
        actor_profile = user.profile
    except UserProfile.DoesNotExist:
        return RiderProfile.objects.none()

    qs = RiderProfile.objects.filter(user__profile__role=UserProfile.Role.DRIVER)
    district_qs = get_districts_queryset(user, province_id=province_id)
    provinces_qs = get_provinces_queryset(user)

    if actor_profile.role == UserProfile.Role.PC:
        pids = pc_province_ids(user)
        if not pids:
            return RiderProfile.objects.none()
        qs = qs.filter(
            Q(district__in=district_qs) | Q(district__isnull=True, province_id__in=pids)
        )
    elif actor_profile.role in (UserProfile.Role.ADMIN, UserProfile.Role.ME):
        qs = qs.filter(
            Q(district__in=district_qs)
            | Q(district__isnull=True, province__in=provinces_qs)
        )
    else:
        return RiderProfile.objects.none()

    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs.select_related(
        "user",
        "user__profile",
        "province",
        "district",
        "district__province",
        "facility",
        "car",
    )


def report_audit_logs_for_user(user, limit: int = 500) -> QuerySet:
    qs = ReportAuditLog.objects.select_related("report", "actor").order_by("-created_at")
    if not user.is_authenticated:
        return qs.none()
    if user.is_superuser:
        return qs[:limit]
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return qs.none()
    if profile.role == UserProfile.Role.ADMIN:
        return qs.all()[:limit]
    if profile.role == UserProfile.Role.PC:
        pids = pc_province_ids(user)
        if not pids:
            return qs.none()
        return qs.filter(
            Q(report__rider__rider_profile__district__province_id__in=pids)
            | Q(
                report__rider__profile__role=UserProfile.Role.DRIVER,
                report__rider__rider_profile__district__isnull=True,
                report__rider__rider_profile__province_id__in=pids,
            )
        )[:limit]
    return qs.none()


def get_referred_samples_queryset(user) -> QuerySet:
    """Referred-sample rows where the referring lab is in the user's province scope."""
    qs = (
        ReferredSample.objects.select_related(
            "from_facility",
            "from_facility__district",
            "from_facility__district__province",
            "to_facility",
            "to_facility__district",
            "to_facility__district__province",
        )
        .order_by("-created_at", "-id")
    )
    if not user.is_authenticated:
        return qs.none()
    if getattr(user, "is_superuser", False):
        return qs
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return qs.none()
    if profile.role == UserProfile.Role.ADMIN:
        return qs
    if profile.role == UserProfile.Role.PC:
        pids = pc_province_ids(user)
        if not pids:
            return qs.none()
        return qs.filter(from_facility__district__province_id__in=pids)
    return qs.none()


def reports_for_rider_week_in_scope(user, rider_id, week_str) -> QuerySet:
    """Group review: only reports the PC may act on for that rider/week."""
    from django.utils.dateparse import parse_date

    if isinstance(week_str, str):
        d = parse_date(week_str)
        if d is None:
            return RiderWeeklyReport.objects.none()
        week_val = d
    else:
        week_val = week_str

    qs = RiderWeeklyReport.objects.filter(rider_id=rider_id, week_start=week_val)
    if not user.is_authenticated:
        return qs.none()
    if user.is_superuser:
        return qs
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return qs.none()
    if profile.role == UserProfile.Role.ADMIN:
        return qs
    if profile.role == UserProfile.Role.PC:
        return qs.filter(pk__in=reports_in_pc_scope(user).values_list("pk", flat=True))
    return qs.none()
