"""Rider API: only users with a rider profile can access protected endpoints."""
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from operations.models import RiderProfile, UserProfile


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
            try:
                return request.user.rider_profile is not None
            except ObjectDoesNotExist:
                rp, _ = RiderProfile.objects.get_or_create(user=request.user)
                request.user.rider_profile = rp
                return True
        except Exception:
            return False
