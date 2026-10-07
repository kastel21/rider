"""Decide whether an installed Android build must update, and which APK to offer."""

from __future__ import annotations

import os
import re
from urllib.parse import quote

from operations.models import RiderAppRelease, RiderRemoteConfig

HEADER_VERSION = "X-App-Version-Code"
HEADER_APP_ID = "X-App-Id"
UPDATE_REQUIRED_CODE = "update_required"

_APP_ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*(\.[A-Za-z][A-Za-z0-9_]*)+$")

_RELEASE_LABELS = {
    "com.ecollect.app.bit64": "E-Collect (64-bit)",
    "com.ecollect.app.bit32": "E-Collect (32-bit)",
    "com.operations.rider.bit64": "Operations Rider (64-bit)",
    "com.operations.rider.bit32": "Operations Rider (32-bit)",
}

# Reachability probes and the in-app download itself must stay open.
EXEMPT_PATHS = (
    "/api/rider/health",
    "/api/rider/app-update",
    "/api/rider/app-download",
    "/api/rider/local-session",
    "/api/rider/jwt-bootstrap",
)


def apply_android_identity_headers(headers: dict) -> dict:
    """Attach this APK's version when the embedded server calls the cloud."""
    version = os.environ.get("OPS_APP_VERSION_CODE", "").strip()
    app_id = os.environ.get("OPS_APP_ID", "").strip()
    if version:
        headers[HEADER_VERSION] = version
    if app_id:
        headers[HEADER_APP_ID] = app_id
    return headers


def valid_application_id(value: str) -> bool:
    return bool(_APP_ID_RE.match((value or "").strip()))


def release_label(application_id: str) -> str:
    return _RELEASE_LABELS.get(application_id, application_id)


def parse_version_code(raw) -> int | None:
    if raw is None:
        return None
    text = str(raw).strip()
    if not text:
        return None
    try:
        value = int(text)
    except (TypeError, ValueError):
        return None
    if value < 0:
        return None
    return value


def request_version_code(request) -> int | None:
    raw = request.headers.get(HEADER_VERSION)
    if raw in (None, ""):
        raw = request.GET.get("version_code")
    return parse_version_code(raw)


def request_application_id(request) -> str:
    raw = (request.headers.get(HEADER_APP_ID) or request.GET.get("application_id") or "").strip()
    if valid_application_id(raw):
        return raw
    return ""


def is_android_client(request) -> bool:
    """Installed APKs call the cloud with OkHttp or the embedded Python proxy."""
    if request.headers.get(HEADER_VERSION) or request.headers.get(HEADER_APP_ID):
        return True
    ua = (request.META.get("HTTP_USER_AGENT") or "").lower()
    return "okhttp" in ua or "python-urllib" in ua


def remote_config() -> RiderRemoteConfig:
    config, _ = RiderRemoteConfig.objects.get_or_create(
        pk=1,
        defaults={
            "sync_interval": 60,
            "max_batch_size": 10,
            "latest_app_version": "",
            "update_required": False,
            "min_version_code": 0,
        },
    )
    return config


def must_update(version_code: int | None, config: RiderRemoteConfig | None = None) -> bool:
    config = config or remote_config()
    if not config.update_required or config.min_version_code < 1:
        return False
    if version_code is None:
        return True
    return version_code < config.min_version_code


def latest_release(application_id: str) -> RiderAppRelease | None:
    if not valid_application_id(application_id):
        return None
    return (
        RiderAppRelease.objects.filter(application_id=application_id)
        .order_by("-version_code", "-pk")
        .first()
    )


def offerable_release(application_id: str, config: RiderRemoteConfig | None = None):
    config = config or remote_config()
    release = latest_release(application_id)
    if release is None:
        return None
    if config.min_version_code and release.version_code < config.min_version_code:
        return None
    return release


def download_path_for(application_id: str) -> str:
    return f"/api/rider/app-download/?application_id={quote(application_id)}"


def status_payload(version_code: int | None, application_id: str) -> dict:
    config = remote_config()
    required = must_update(version_code, config)
    release = offerable_release(application_id, config) if application_id else None
    newer = (
        release is not None
        and version_code is not None
        and release.version_code > version_code
    )
    path = ""
    if release is not None and application_id and (required or newer):
        path = download_path_for(application_id)
    version_name = ""
    latest_code = 0
    if release is not None:
        version_name = release.version_name or ""
        latest_code = release.version_code
    if not version_name:
        version_name = config.latest_app_version or ""
    return {
        "update_required": required,
        "update_available": bool(path),
        "min_version_code": config.min_version_code,
        "latest_version_code": latest_code,
        "latest_app_version": version_name,
        "download_path": path,
        "application_id": application_id,
    }


def rejection_payload(request) -> dict | None:
    """Body for a blocked Android client, or None when the request may proceed."""
    from django.conf import settings

    if not getattr(settings, "OPS_ENFORCE_APP_VERSION", True):
        return None
    if not request.path.startswith("/api/rider/"):
        return None
    path = request.path.rstrip("/")
    if any(path == item or path.startswith(item + "/") for item in EXEMPT_PATHS):
        return None
    if not is_android_client(request):
        return None
    config = remote_config()
    version_code = request_version_code(request)
    if not must_update(version_code, config):
        return None
    application_id = request_application_id(request)
    release = offerable_release(application_id, config) if application_id else None
    version_name = ""
    if release is not None and release.version_name:
        version_name = release.version_name
    elif config.latest_app_version:
        version_name = config.latest_app_version
    return {
        "error": "This version of the app is no longer allowed. Open /app/update/ in the phone browser.",
        "code": UPDATE_REQUIRED_CODE,
        "min_version_code": config.min_version_code,
        "latest_app_version": version_name,
        "download_path": download_path_for(application_id) if release is not None else "",
    }


def latest_releases():
    """Newest uploaded APK for each application id."""
    seen = set()
    rows = []
    for release in RiderAppRelease.objects.order_by("-version_code", "-pk"):
        if release.application_id in seen:
            continue
        seen.add(release.application_id)
        rows.append(release)
    return rows
