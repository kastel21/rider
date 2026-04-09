"""Report workflow: submit, PC review transitions, audit logging."""
from operations.models import AuditAction, AuditLog, ReportStatus, RiderWeeklyReport


class ReportService:
    """State transitions and audit entries for weekly reports."""

    @staticmethod
    def submit(report: RiderWeeklyReport, user):
        if report.status != ReportStatus.DRAFT:
            return report
        report.status = ReportStatus.SUBMITTED
        report.save(update_fields=['status', 'updated_at'])
        ReportService._audit(user, AuditAction.SUBMIT, report, {'status': ReportStatus.SUBMITTED})
        return report

    @staticmethod
    def start_review(report: RiderWeeklyReport, user):
        if report.status != ReportStatus.SUBMITTED:
            return report
        report.status = ReportStatus.UNDER_REVIEW
        report.save(update_fields=['status', 'updated_at'])
        ReportService._audit(user, AuditAction.REVIEW, report, {'status': ReportStatus.UNDER_REVIEW})
        return report

    @staticmethod
    def review(report: RiderWeeklyReport, user):
        if report.status not in (ReportStatus.SUBMITTED, ReportStatus.UNDER_REVIEW):
            return report
        report.status = ReportStatus.REVIEWED
        report.save(update_fields=['status', 'updated_at'])
        ReportService._audit(user, AuditAction.REVIEW, report, {'status': ReportStatus.REVIEWED})
        return report

    @staticmethod
    def _audit(user, action, report: RiderWeeklyReport, changes: dict):
        try:
            AuditLog.objects.create(
                user=user,
                action=action,
                model_name='RiderWeeklyReport',
                object_id=str(report.pk),
                object_repr=str(report),
                changes=changes,
                ip_address=None,
            )
        except Exception:
            pass
