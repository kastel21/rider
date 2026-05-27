"""
Fetch rider JWT tokens from the remote HTTPS API (embedded Android uplink).

When remote login fails (SSL, timeout) but JWT_SIGNING_KEY matches the cloud server,
mint tokens locally for the logged-in user (same user ids after landing user import).
"""
import json
import logging
import urllib.error
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def _rider_login_user_payload(user, rider) -> dict:
    return {
        "id": user.pk,
        "username": user.get_username(),
        "rider_id": rider.pk,
        "district_id": rider.district_id,
        "province_id": rider.province_id
        or (rider.district.province_id if rider.district_id else None),
    }


def mint_local_rider_tokens(user):
    """
    Issue JWT with the configured SIMPLE_JWT signing key (embedded APK / shared cloud secret).
    """
    if not getattr(settings, "OPS_ALLOW_LOCAL_JWT_MINT", False):
        return None
    if not user or not user.is_authenticated:
        return None
    rider = getattr(user, "rider_profile", None)
    if not rider:
        return None
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
    except ImportError:
        return None
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": _rider_login_user_payload(user, rider),
    }


def resolve_rider_jwt_tokens(user, api_base: str = "", username: str = "", password: str = ""):
    """
    Prefer cloud-issued tokens; fall back to local mint when allowed and remote login fails.
    """
    base = (api_base or getattr(settings, "OPS_REMOTE_API_BASE", "") or "").strip()
    if base and username and password:
        tokens = fetch_remote_rider_tokens(base, username, password)
        if tokens:
            return tokens
        logger.info("remote rider login unavailable; trying local JWT mint for %s", username)
    return mint_local_rider_tokens(user)


def fetch_remote_rider_tokens(api_base: str, username: str, password: str, timeout: float = 15.0):
    """
    POST {api_base}/api/rider/login/ with username/password.
    Returns dict with access, refresh, user keys or None on failure.
    """
    base = (api_base or "").strip().rstrip("/")
    if not base or not username or not password:
        return None
    url = f"{base}/api/rider/login/"
    body = json.dumps({"username": username, "password": password}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        logger.warning("remote rider login HTTP %s: %s", e.code, e.reason)
        return None
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError) as e:
        logger.warning("remote rider login failed: %s", e)
        return None
    access = data.get("access")
    if not access:
        return None
    return {
        "access": access,
        "refresh": data.get("refresh") or "",
        "user": data.get("user") or {},
    }
