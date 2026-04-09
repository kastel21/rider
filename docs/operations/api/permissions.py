"""Rider API: only users with a rider profile can access protected endpoints."""
from rest_framework.permissions import BasePermission


class IsRider(BasePermission):
    """Allow only authenticated users who have an operations rider profile (RIDER or DRIVER role)."""
    message = 'Rider profile required.'

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            profile = getattr(request.user, 'operations_profile', None)
            if not profile:
                return False
            role = getattr(profile, 'role', None)
            if role not in ('RIDER', 'DRIVER'):
                return False
            return hasattr(request.user, 'operations_rider_profile')
        except Exception:
            return False
