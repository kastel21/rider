"""Weekly report: same layout as M&E rider/driver export, one aggregated row per person per week."""

from datetime import timedelta
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from ..models import UserProfile
from ..selectors import (
    monday_of_local_today,
    parse_pc_approved_param,
    week_range_label,
    week_start_from_request,
)
from ..services.me_report_service import build_me_report_table_for_week
from .me_export_views import me_week_export_hrefs


class WeeklyReportView(LoginRequiredMixin, TemplateView):
    template_name = "operations/reports/weekly_report.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        default_week = monday_of_local_today() - timedelta(days=7)
        week_start = week_start_from_request(self.request, default_week_monday=default_week)
        pc_approved_only = parse_pc_approved_param(self.request)

        ctx["selected_week_start"] = week_start
        ctx["pc_approved_only"] = pc_approved_only
        ctx["week_range_label"] = week_range_label(week_start)
        prev_week = (week_start - timedelta(days=7)).isoformat()
        next_week = (week_start + timedelta(days=7)).isoformat()
        ctx["weekly_report_prev_week_href"] = (
            f"?week={prev_week}&pc_approved={'1' if pc_approved_only else '0'}"
        )
        ctx["weekly_report_next_week_href"] = (
            f"?week={next_week}&pc_approved={'1' if pc_approved_only else '0'}"
        )
        ctx["me_rider_report"] = build_me_report_table_for_week(
            week_start=week_start,
            role=UserProfile.Role.RIDER,
            pc_approved_only=pc_approved_only,
        )
        ctx["me_driver_report"] = build_me_report_table_for_week(
            week_start=week_start,
            role=UserProfile.Role.DRIVER,
            pc_approved_only=pc_approved_only,
        )
        week_iso = week_start.isoformat()
        ctx.update(
            me_week_export_hrefs(
                name_csv="operations:weekly_report_riders_export_csv",
                name_xlsx="operations:weekly_report_riders_export_xlsx",
                week_iso=week_iso,
                pc_approved_only=pc_approved_only,
            )
        )
        ctx["rider_export_csv_href"] = ctx["export_csv_href"]
        ctx["rider_export_xlsx_href"] = ctx["export_xlsx_href"]
        driver_hrefs = me_week_export_hrefs(
            name_csv="operations:weekly_report_drivers_export_csv",
            name_xlsx="operations:weekly_report_drivers_export_xlsx",
            week_iso=week_iso,
            pc_approved_only=pc_approved_only,
        )
        ctx["driver_export_csv_href"] = driver_hrefs["export_csv_href"]
        ctx["driver_export_xlsx_href"] = driver_hrefs["export_xlsx_href"]
        return ctx
