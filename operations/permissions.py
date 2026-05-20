from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import RiderWeeklyReport, UserProfile


def _role(user):
    if not user.is_authenticated:
        return None
    p = getattr(user, "profile", None)
    return p.role if p else None


def is_rider_like(user):
    return _role(user) in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER)


def is_pc(user):
    return _role(user) in (UserProfile.Role.PC, UserProfile.Role.ADMIN)


def is_me(user):
    return _role(user) == UserProfile.Role.ME


def report_in_pc_scope(user, report: RiderWeeklyReport) -> bool:
    """True if this report's rider is in the user's PC province scope."""
    from .selectors import reports_in_pc_scope

    return reports_in_pc_scope(user).filter(pk=report.pk).exists()


def can_view_report(user, report: RiderWeeklyReport) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    role = _role(user)
    if role == UserProfile.Role.ADMIN:
        return True
    if role == UserProfile.Role.ME:
        return True
    if role == UserProfile.Role.PC:
        return report_in_pc_scope(user, report)
    if role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER):
        return report.rider_id == user.id
    return False


def can_edit_report_as_rider(user, report: RiderWeeklyReport) -> bool:
    if not is_rider_like(user):
        return False
    if report.rider_id != user.id:
        return False
    # Draft or PC-rejected only: once submitted for PC review (submitted / under review /
    # approved), the rider must wait for PC outcome before editing again.
    return report.status in (
        RiderWeeklyReport.Status.DRAFT,
        RiderWeeklyReport.Status.REJECTED,
    )


def can_edit_report_as_pc(user, report: RiderWeeklyReport) -> bool:
    if report.me_reviewed_at is not None:
        return False
    if user.is_authenticated and user.is_superuser:
        return report.status in (
            RiderWeeklyReport.Status.DRAFT,
            RiderWeeklyReport.Status.SUBMITTED,
            RiderWeeklyReport.Status.UNDER_REVIEW,
            RiderWeeklyReport.Status.REJECTED,
        )
    if not is_pc(user):
        return False
    if _role(user) == UserProfile.Role.PC and not report_in_pc_scope(user, report):
        return False
    return report.status in (
        RiderWeeklyReport.Status.DRAFT,
        RiderWeeklyReport.Status.SUBMITTED,
        RiderWeeklyReport.Status.UNDER_REVIEW,
        RiderWeeklyReport.Status.REJECTED,
    )


def can_mark_me_review(user, report: RiderWeeklyReport) -> bool:
    """M&E may record that national review is complete (locks PC edits for this report)."""
    if not user.is_authenticated or not is_me(user):
        return False
    return can_view_report(user, report)


def require_pc(user):
    if not is_pc(user) and not (user.is_authenticated and user.is_superuser):
        raise PermissionDenied


class PCRequiredMixin(UserPassesTestMixin):
    """PC or Admin (or superuser): same gate as require_pc, for class-based views."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return is_pc(user)


class MERequiredMixin(UserPassesTestMixin):
    """Monitoring & Evaluation role only (national program metrics)."""

    def test_func(self):
        return is_me(self.request.user)


class ProgramReportingMixin(UserPassesTestMixin):
    """M&E, PC, and Admin may download national reporting tables."""

    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return _role(user) in (
            UserProfile.Role.ME,
            UserProfile.Role.PC,
            UserProfile.Role.ADMIN,
        )


# docs/operations-compatible mixin naming.
class OperationsLoginRequiredMixin(LoginRequiredMixin):
    pass
