"""Rider API: only users with a rider profile can access protected endpoints."""
from rest_framework.permissions import BasePermission

from operations.models import UserProfile


class IsRider(BasePermission):
    """Allow only authenticated users who have a rider profile (RIDER or DRIVER role)."""

    message = "Rider profile required."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            profile = getattr(request.user, "profile", None)
            if not profile:
                return False
            role = getattr(profile, "role", None)
            if role not in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER):
                return False
            return getattr(request.user, "rider_profile", None) is not None
        except Exception:
            return False
