from ..models import ReportEditSnapshot, RiderWeeklyReport


def record_pc_edit(report: RiderWeeklyReport, editor, summary: str, diff_data: dict | None = None):
    ReportEditSnapshot.objects.create(
        report=report,
        editor=editor,
        summary=summary,
        diff_data=diff_data or {},
    )
