"""
Read-side queries: permission-filtered querysets for reports and related data.
"""
from django.db.models import Q

from operations.models import (
    RiderWeeklyReport,
    UserProfile,
    PCProfile,
    RiderProfile,
    Role,
    ProvincialDriverWeekly,
    ReferredSample,
    TransportIncident,
    RiderAccidentRecord,
    IncompleteTripRecord,
)


def get_reports_queryset(user):
    """
    Return RiderWeeklyReport queryset filtered by user role:
    RIDER: own only; PC: assigned provinces; ME: all; ADMIN: all.
    """
    try:
        profile = user.operations_profile
    except Exception:
        return RiderWeeklyReport.objects.none()

    if profile.role == Role.ADMIN or profile.role == Role.ME:
        return RiderWeeklyReport.objects.all().select_related(
            'rider', 'rider__user', 'district', 'province'
        )

    if profile.role == Role.PC:
        try:
            pc = user.operations_pc_profile
            province_ids = pc.provinces.values_list('id', flat=True)
            return RiderWeeklyReport.objects.filter(
                province_id__in=province_ids
            ).select_related('rider', 'rider__user', 'district', 'province')
        except Exception:
            return RiderWeeklyReport.objects.none()

    if profile.role in (Role.RIDER, Role.DRIVER):
        try:
            rider = user.operations_rider_profile
            return RiderWeeklyReport.objects.filter(
                rider=rider
            ).select_related('rider', 'rider__user', 'district', 'province')
        except Exception:
            return RiderWeeklyReport.objects.none()

    return RiderWeeklyReport.objects.none()


def get_provinces_queryset(user):
    """Provinces visible to user: ADMIN/ME all; PC assigned only."""
    from operations.models import Province
    try:
        profile = user.operations_profile
    except Exception:
        return Province.objects.none()
    if profile.role in (Role.ADMIN, Role.ME):
        return Province.objects.all()
    if profile.role == Role.PC:
        try:
            return user.operations_pc_profile.provinces.all()
        except Exception:
            return Province.objects.none()
    return Province.objects.none()


def get_districts_queryset(user, province_id=None):
    """Districts in scope: by province if given; else all visible provinces."""
    from operations.models import District
    provinces = get_provinces_queryset(user)
    qs = District.objects.filter(province__in=provinces)
    if province_id:
        qs = qs.filter(province_id=province_id)
    return qs


def get_facilities_queryset(user, district_id=None):
    """Facilities in scope (districts from visible provinces)."""
    from operations.models import Facility
    districts = get_districts_queryset(user)
    qs = Facility.objects.filter(district__in=districts)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_bikes_queryset(user, district_id=None):
    """Bikes in scope (districts from visible provinces)."""
    from operations.models import Bike
    districts = get_districts_queryset(user)
    qs = Bike.objects.filter(district__in=districts, is_active=True)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_bikes_for_functionality_queryset(user, district_id=None, province_id=None, rider_id=None):
    """All bikes in PC's provinces for the bike functionality page (includes inactive).
    When rider_id is set: bikes from rider's records (reports) first; if no reports, bikes assigned to that rider in DB."""
    from operations.models import Bike, RiderWeeklyReport
    districts = get_districts_queryset(user, province_id=province_id)
    qs = Bike.objects.filter(district__in=districts).select_related(
        'district', 'district__province'
    )
    if district_id:
        qs = qs.filter(district_id=district_id)
    if rider_id:
        # Bikes from this rider's reports (records sent by rider)
        regs_from_reports = list(
            RiderWeeklyReport.objects.filter(rider_id=rider_id)
            .values_list('bike_registration', flat=True)
            .distinct()
        )
        regs_from_reports = [r for r in regs_from_reports if r and str(r).strip()]
        bikes_from_reports = qs.filter(registration_number__in=regs_from_reports) if regs_from_reports else qs.none()
        # Union: bikes that appear in rider's reports OR are assigned to rider in DB
        from django.db.models import Q
        qs = qs.filter(
            Q(pk__in=bikes_from_reports.values_list('pk', flat=True)) |
            Q(assigned_riders__id=rider_id)
        ).distinct()
    return qs.order_by('district__province__name', 'district__name', 'registration_number')


def get_riders_queryset(user, district_id=None, province_id=None):
    """Riders in scope (PC: assigned provinces; ADMIN/ME: all)."""
    districts = get_districts_queryset(user, province_id=province_id)
    qs = RiderProfile.objects.filter(district__in=districts).select_related(
        'user', 'district', 'facility', 'bike'
    )
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_provincial_driver_weekly_queryset(user, province_id=None, district_id=None):
    """Provincial Driver Weekly entries in scope. PC: assigned provinces; ME/ADMIN: all."""
    if not user.is_authenticated:
        return ProvincialDriverWeekly.objects.none()
    try:
        profile = user.operations_profile
    except Exception:
        return ProvincialDriverWeekly.objects.none()
    if profile.role == Role.ADMIN or profile.role == Role.ME:
        qs = ProvincialDriverWeekly.objects.all()
    elif profile.role == Role.PC:
        try:
            province_ids = user.operations_pc_profile.provinces.values_list('id', flat=True)
            qs = ProvincialDriverWeekly.objects.filter(province_id__in=province_ids)
        except Exception:
            return ProvincialDriverWeekly.objects.none()
    else:
        return ProvincialDriverWeekly.objects.none()
    qs = qs.select_related('province', 'district')
    if province_id:
        qs = qs.filter(province_id=province_id)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_referred_samples_queryset(user, province_id=None, district_id=None):
    """Referred samples in scope. PC: assigned provinces; ME/ADMIN: all."""
    if not user.is_authenticated:
        return ReferredSample.objects.none()
    try:
        profile = user.operations_profile
    except Exception:
        return ReferredSample.objects.none()
    if profile.role == Role.ADMIN or profile.role == Role.ME:
        qs = ReferredSample.objects.all()
    elif profile.role == Role.PC:
        try:
            province_ids = user.operations_pc_profile.provinces.values_list('id', flat=True)
            qs = ReferredSample.objects.filter(province_id__in=province_ids)
        except Exception:
            return ReferredSample.objects.none()
    else:
        return ReferredSample.objects.none()
    qs = qs.select_related('province', 'district', 'facility')
    if province_id:
        qs = qs.filter(province_id=province_id)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_transport_incidents_queryset(user, province_id=None, district_id=None):
    """Transport incidents in scope. PC: assigned provinces; ME/ADMIN: all."""
    if not user.is_authenticated:
        return TransportIncident.objects.none()
    try:
        profile = user.operations_profile
    except Exception:
        return TransportIncident.objects.none()
    if profile.role == Role.ADMIN or profile.role == Role.ME:
        qs = TransportIncident.objects.all()
    elif profile.role == Role.PC:
        try:
            province_ids = user.operations_pc_profile.provinces.values_list('id', flat=True)
            qs = TransportIncident.objects.filter(province_id__in=province_ids)
        except Exception:
            return TransportIncident.objects.none()
    else:
        return TransportIncident.objects.none()
    qs = qs.select_related('province', 'district')
    if province_id:
        qs = qs.filter(province_id=province_id)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_rider_accident_records_queryset(user, province_id=None, district_id=None):
    """Rider accident capture rows in scope. PC: assigned provinces; ME/ADMIN: all."""
    if not user.is_authenticated:
        return RiderAccidentRecord.objects.none()
    try:
        profile = user.operations_profile
    except Exception:
        return RiderAccidentRecord.objects.none()
    if profile.role == Role.ADMIN or profile.role == Role.ME:
        qs = RiderAccidentRecord.objects.all()
    elif profile.role == Role.PC:
        try:
            province_ids = user.operations_pc_profile.provinces.values_list('id', flat=True)
            qs = RiderAccidentRecord.objects.filter(province_id__in=province_ids)
        except Exception:
            return RiderAccidentRecord.objects.none()
    else:
        return RiderAccidentRecord.objects.none()
    qs = qs.select_related('province', 'district')
    if province_id:
        qs = qs.filter(province_id=province_id)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs


def get_incomplete_trip_records_queryset(user, province_id=None, district_id=None):
    """Incomplete trip capture rows in scope. PC: assigned provinces; ME/ADMIN: all."""
    if not user.is_authenticated:
        return IncompleteTripRecord.objects.none()
    try:
        profile = user.operations_profile
    except Exception:
        return IncompleteTripRecord.objects.none()
    if profile.role == Role.ADMIN or profile.role == Role.ME:
        qs = IncompleteTripRecord.objects.all()
    elif profile.role == Role.PC:
        try:
            province_ids = user.operations_pc_profile.provinces.values_list('id', flat=True)
            qs = IncompleteTripRecord.objects.filter(province_id__in=province_ids)
        except Exception:
            return IncompleteTripRecord.objects.none()
    else:
        return IncompleteTripRecord.objects.none()
    qs = qs.select_related('province', 'district')
    if province_id:
        qs = qs.filter(province_id=province_id)
    if district_id:
        qs = qs.filter(district_id=district_id)
    return qs
