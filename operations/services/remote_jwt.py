"""
Fetch rider JWT tokens from the remote HTTPS API (embedded Android uplink).
"""
import json
import logging
import urllib.error
import urllib.request

logger = logging.getLogger(__name__)


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
