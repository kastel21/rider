"""
Access control mixins and helpers for operations views.
"""
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from operations.models import Role, ReportStatus


class OperationsLoginRequiredMixin(LoginRequiredMixin):
    login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')


class RiderRequiredMixin(UserPassesTestMixin):
    """Authenticated user with RIDER or DRIVER role and a rider profile."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        try:
            role = user.operations_profile.role
        except Exception:
            return False
        if role not in (Role.RIDER, Role.DRIVER):
            return False
        return hasattr(user, 'operations_rider_profile')


class PCRequiredMixin(UserPassesTestMixin):
    """PC dashboard / review flows: PC, ME, or Admin (same data scope as selectors)."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        try:
            role = user.operations_profile.role
        except Exception:
            return False
        return role in (Role.PC, Role.ME, Role.ADMIN)


class RiderSections1To3OnlyMixin:
    """Rider operational form (sections 1-3); access is enforced by RiderRequiredMixin on the same view."""

    pass


def can_edit_report(user, report):
    """Whether the user may use the rider edit view for this report (own draft only)."""
    if report is None or not user.is_authenticated:
        return False
    try:
        role = user.operations_profile.role
    except Exception:
        return False
    if role not in (Role.RIDER, Role.DRIVER):
        return False
    try:
        rider = user.operations_rider_profile
    except Exception:
        return False
    if report.rider_id != rider.pk:
        return False
    return report.status == ReportStatus.DRAFT
