"""Trip route kinds, endpoint roles (Hub / VL Lab), and facility querysets for From/To dropdowns."""

from django.db.models import QuerySet

from ..models import Facility, TripRouteKind, UserProfile
from ..selectors import pc_province_ids as get_pc_province_ids

# Hub routes: PEPFAR hubs plus clinics / district & mission hospitals (stored as clinic).
HUB_ENDPOINT_KINDS = frozenset({Facility.Kind.HUB, Facility.Kind.CLINIC})
VL_LAB_ENDPOINT_KINDS = frozenset({Facility.Kind.LAB})

_LEGACY_ROUTE_KIND_ALIASES = {
    "facility_to_facility": TripRouteKind.HUB_TO_HUB,
    "facility_to_lab": TripRouteKind.HUB_TO_LAB,
    "lab_to_facility": TripRouteKind.LAB_TO_HUB,
}


def normalize_route_kind(route_kind: str) -> str:
    """Map removed facility_* route slugs to hub / VL Lab routes."""
    rk = (route_kind or "").strip()
    return _LEGACY_ROUTE_KIND_ALIASES.get(rk, rk)


def route_endpoint_roles(route_kind: str) -> tuple[str, str] | None:
    """
    Return (from_role, to_role) where each role is 'hub' or 'vl_lab'.
    Provincial hospitals and reference labs use Facility.kind=lab (VL Lab endpoint).
    """
    rk = normalize_route_kind(route_kind)
    m = {
        TripRouteKind.HUB_TO_HUB: ("hub", "hub"),
        TripRouteKind.HUB_TO_LAB: ("hub", "vl_lab"),
        TripRouteKind.LAB_TO_HUB: ("vl_lab", "hub"),
        TripRouteKind.LAB_TO_LAB: ("vl_lab", "vl_lab"),
    }
    return m.get(rk)


def kinds_for_endpoint_role(role: str) -> frozenset[str]:
    if role == "hub":
        return HUB_ENDPOINT_KINDS
    if role == "vl_lab":
        return VL_LAB_ENDPOINT_KINDS
    return frozenset()


def facility_matches_route_endpoint(facility: Facility | None, role: str) -> bool:
    if not facility:
        return False
    return facility.kind in kinds_for_endpoint_role(role)


def route_endpoint_kinds(route_kind: str) -> tuple[str, str] | None:
    """Deprecated: use route_endpoint_roles. Kept for callers expecting kind slugs."""
    roles = route_endpoint_roles(route_kind)
    if not roles:
        return None
    from_role, to_role = roles
    from_kind = next(iter(kinds_for_endpoint_role(from_role)))
    to_kind = next(iter(kinds_for_endpoint_role(to_role)))
    return from_kind, to_kind


def _base_facility_qs() -> QuerySet:
    return Facility.objects.select_related("district", "district__province").order_by("name")


def _filter_qs_for_endpoint_role(qs: QuerySet, role: str) -> QuerySet:
    kinds = kinds_for_endpoint_role(role)
    if role == "vl_lab":
        return qs.filter(kind=Facility.Kind.LAB)
    return qs.filter(kind__in=kinds)


def facilities_for_rider_endpoint(
    user,
    route_kind: str,
    slot: str,
    *,
    district_id: int | None = None,
    province_ids: list[int] | None = None,
) -> QuerySet:
    """
    Rider: district-scoped hub sites; province-scoped VL labs.
    Driver: province-scoped for all endpoint roles.
    PC / ME / admin: province filter when provided.
    slot: 'from' or 'to'
    """
    roles = route_endpoint_roles(route_kind)
    if not roles or slot not in ("from", "to"):
        return _base_facility_qs().none()
    want_role = roles[0] if slot == "from" else roles[1]

    qs = _filter_qs_for_endpoint_role(_base_facility_qs(), want_role)

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
        if want_role == "vl_lab":
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
