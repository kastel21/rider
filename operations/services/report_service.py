from django.utils import timezone

from ..models import ReportAuditLog, RiderWeeklyReport


def submit_report(report: RiderWeeklyReport, user):
    """Rider submit or resend. Clears any earlier lab-manager release so they review again."""
    report.status = RiderWeeklyReport.Status.SUBMITTED
    report.submitted_at = timezone.now()
    report.lab_cleared_at = None
    report.lab_cleared_by = None
    report.lab_notes = ""
    report.save(
        update_fields=[
            "status",
            "submitted_at",
            "lab_cleared_at",
            "lab_cleared_by",
            "lab_notes",
            "updated_at",
        ]
    )
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="submit",
        payload={},
    )


def release_report_to_pc(report: RiderWeeklyReport, user) -> bool:
    """Lab manager approves a waiting submission. The rider can no longer edit it."""
    if report.status != RiderWeeklyReport.Status.SUBMITTED or report.lab_cleared_at:
        return False
    report.lab_cleared_at = timezone.now()
    report.lab_cleared_by = user
    report.lab_notes = ""
    report.save(
        update_fields=["lab_cleared_at", "lab_cleared_by", "lab_notes", "updated_at"]
    )
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="lab_approve",
        payload={},
    )
    return True


def send_report_back_to_rider(report: RiderWeeklyReport, user, reason: str) -> bool:
    """Lab manager send-back. Reason is required. Status rejected unlocks the existing APK edit."""
    reason = (reason or "").strip()
    if not reason:
        return False
    if report.status != RiderWeeklyReport.Status.SUBMITTED or report.lab_cleared_at:
        return False
    report.status = RiderWeeklyReport.Status.REJECTED
    report.lab_notes = reason
    report.lab_cleared_at = None
    report.lab_cleared_by = None
    # The rider APK already shows Notes. Put the reason there so no new screen is required.
    note_line = f"Lab manager: {reason}"
    existing = (report.notes or "").strip()
    if note_line not in existing:
        report.notes = f"{existing}\n\n{note_line}".strip() if existing else note_line
    report.save(
        update_fields=[
            "status",
            "notes",
            "lab_notes",
            "lab_cleared_at",
            "lab_cleared_by",
            "updated_at",
        ]
    )
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="lab_send_back",
        payload={"lab_notes": reason},
    )
    return True


def start_review(report: RiderWeeklyReport, user):
    report.status = RiderWeeklyReport.Status.UNDER_REVIEW
    report.review_started_at = timezone.now()
    report.save(update_fields=["status", "review_started_at", "updated_at"])
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="start_review",
        payload={},
    )


def complete_review(report: RiderWeeklyReport, user, approved: bool, pc_notes: str = ""):
    report.reviewed_by = user
    report.reviewed_at = timezone.now()
    report.pc_notes = pc_notes or report.pc_notes
    report.status = (
        RiderWeeklyReport.Status.APPROVED if approved else RiderWeeklyReport.Status.REJECTED
    )
    report.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "pc_notes",
            "updated_at",
        ]
    )
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="approve" if approved else "reject",
        payload={"pc_notes": pc_notes},
    )


def audit_entries_for_report(report):
    return report.audit_logs.select_related("actor").all()
