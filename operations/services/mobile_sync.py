"""Landing-sync service accounts (APK OPS_SYNC_USERNAME)."""

from django.conf import settings


def mobile_sync_usernames() -> set[str]:
    raw = getattr(settings, "OPS_MOBILE_SYNC_USERNAMES", frozenset())
    if isinstance(raw, str):
        return {p.strip().lower() for p in raw.split(",") if p.strip()}
    return {str(x).strip().lower() for x in raw if str(x).strip()}


def is_mobile_sync_user(user) -> bool:
    name = (getattr(user, "get_username", lambda: "")() or "").strip().lower()
    return bool(name) and name in mobile_sync_usernames()


def fallback_district_id(user=None) -> int | None:
    """
    Numeric district id so APK landing sync will download users/passwords.

    The APK skips user import when bootstrap.district_id and profile.district.id
    are missing or JSON null. Prefer the account's rider district; otherwise the
    lowest existing district id.
    """
    rider = getattr(user, "rider_profile", None) if user is not None else None
    if rider is not None and getattr(rider, "district_id", None):
        return int(rider.district_id)
    from operations.models import District

    row = District.objects.order_by("id").values_list("id", flat=True).first()
    return int(row) if row is not None else None
