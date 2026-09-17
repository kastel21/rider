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
