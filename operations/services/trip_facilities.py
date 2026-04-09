"""Trip route kinds, endpoint kinds, and facility querysets for From/To dropdowns."""

from django.db.models import QuerySet

from ..models import Facility, TripRouteKind, UserProfile
from ..selectors import pc_province_ids as get_pc_province_ids


def route_endpoint_kinds(route_kind: str) -> tuple[str, str] | None:
    """Return (origin_facility.kind, destination_facility.kind) for a route_kind slug."""
    m = {
        TripRouteKind.FACILITY_TO_FACILITY: (Facility.Kind.CLINIC, Facility.Kind.CLINIC),
        TripRouteKind.FACILITY_TO_LAB: (Facility.Kind.CLINIC, Facility.Kind.LAB),
        TripRouteKind.LAB_TO_FACILITY: (Facility.Kind.LAB, Facility.Kind.CLINIC),
        TripRouteKind.HUB_TO_HUB: (Facility.Kind.HUB, Facility.Kind.HUB),
        TripRouteKind.HUB_TO_LAB: (Facility.Kind.HUB, Facility.Kind.LAB),
        TripRouteKind.LAB_TO_HUB: (Facility.Kind.LAB, Facility.Kind.HUB),
        TripRouteKind.LAB_TO_LAB: (Facility.Kind.LAB, Facility.Kind.LAB),
    }
    return m.get(route_kind)


def _base_facility_qs() -> QuerySet:
    return Facility.objects.select_related("district", "district__province").order_by("name")


def facilities_for_rider_endpoint(
    user,
    route_kind: str,
    slot: str,
    *,
    district_id: int | None = None,
    province_ids: list[int] | None = None,
) -> QuerySet:
    """
    Rider: district-scoped hubs/clinics; province-scoped labs (province from rider's district).
    Driver: province-scoped for all endpoint kinds (province from district if set, else rider_profile.province).
    PC: provinces from province_ids or the user's PC profile; optional district_id fallback.
    ME/admin: all facilities of the expected kind, optionally filtered by province_ids.
    slot: 'from' or 'to'
    """
    pair = route_endpoint_kinds(route_kind)
    if not pair or slot not in ("from", "to"):
        return _base_facility_qs().none()
    want_kind = pair[0] if slot == "from" else pair[1]

    qs = _base_facility_qs().filter(kind=want_kind)

    if not user.is_authenticated:
        return qs.none()

    try:
        role = user.profile.role
    except Exception:
        return qs.none()

    if role == UserProfile.Role.DRIVER:
        rp = getattr(user, "rider_profile", None)
        if not rp:
            return qs.none()
        prov_id = None
        if rp.district_id:
            prov_id = rp.district.province_id
        elif rp.province_id:
            prov_id = rp.province_id
        if not prov_id:
            return qs.none()
        return qs.filter(district__province_id=prov_id)

    if role == UserProfile.Role.RIDER:
        rp = getattr(user, "rider_profile", None)
        if not rp or not rp.district_id:
            return qs.none()
        dist = rp.district
        prov_id = dist.province_id
        if want_kind == Facility.Kind.LAB:
            return qs.filter(district__province_id=prov_id)
        return qs.filter(district_id=rp.district_id)

    if role == UserProfile.Role.PC:
        pids = list(province_ids) if province_ids is not None else get_pc_province_ids(user)
        if not pids and district_id:
            return qs.filter(district_id=district_id)
        if pids:
            return qs.filter(district__province_id__in=pids)
        return qs.none()

    if role in (UserProfile.Role.ADMIN, UserProfile.Role.ME):
        if province_ids:
            return qs.filter(district__province_id__in=province_ids)
        return qs

    return qs.none()


def facility_allowed_for_user(
    user,
    facility: Facility | None,
    route_kind: str,
    slot: str,
    *,
    district_id: int | None = None,
    province_ids: list[int] | None = None,
) -> bool:
    if not facility:
        return True
    qs = facilities_for_rider_endpoint(
        user, route_kind, slot, district_id=district_id, province_ids=province_ids
    )
    return qs.filter(pk=facility.pk).exists()
