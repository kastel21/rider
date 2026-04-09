from django.utils import timezone

from ..models import ReportAuditLog, RiderWeeklyReport


def submit_report(report: RiderWeeklyReport, user):
    report.status = RiderWeeklyReport.Status.SUBMITTED
    report.submitted_at = timezone.now()
    report.save(update_fields=["status", "submitted_at", "updated_at"])
    ReportAuditLog.objects.create(
        report=report,
        actor=user,
        action="submit",
        payload={},
    )


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
