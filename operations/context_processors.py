def operations_nav(request):
    role = None
    if request.user.is_authenticated:
        profile = getattr(request.user, "profile", None)
        if profile:
            role = profile.role
    return {"user_role": role}


def ops_sync_settings(request):
    """Meta tags for offline-sync.js JWT mode (see docs/RIDER_PWA_REQUIREMENTS.md)."""
    from django.conf import settings

    return {
        "ops_sync_mode": getattr(settings, "OPS_SYNC_MODE", "") or "",
        "ops_remote_api_base": getattr(settings, "OPS_REMOTE_API_BASE", "") or "",
    }
