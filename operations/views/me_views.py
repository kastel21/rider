from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView

from ..permissions import MERequiredMixin
from ..selectors import sunday_of_week, week_range_label
from ..services.me_accidents_data import load_me_accidents_incomplete_data, me_accidents_week_start_from_request
from ..services.me_metrics_service import build_me_metrics, parse_weeks_param
from ..services.me_referred_samples_table import build_me_referred_samples_table
from ..services.me_report_service import build_driver_me_report_table, build_me_report_table
from .me_export_views import me_accidents_export_hrefs, me_matrix_export_hrefs


def _me_export_weeks_context(*, weeks: int, table: dict, url_name: str) -> dict:
    """Week filter + period label for rider/driver/referred M&E tables (N-week window)."""
    ws = table["window_start"]
    we = table["window_end"]
    window_range_label = (
        f"{ws.strftime('%d %b %Y')} – {sunday_of_week(we).strftime('%d %b %Y')}"
    )
    return {
        "weeks_param": weeks,
        "weeks_form_action": reverse(f"operations:{url_name}"),
        "window_range_label": window_range_label,
    }


class MEMetricsOverviewView(LoginRequiredMixin, MERequiredMixin, TemplateView):
    """National summary cards and trend chart (no export matrices)."""

    template_name = "operations/me/metrics_overview.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        weeks = parse_weeks_param(self.request.GET.get("weeks"))
        ctx["me_metrics"] = build_me_metrics(weeks=weeks)
        ctx["weeks_param"] = weeks
        ctx.update(
            me_matrix_export_hrefs(
                name_csv="operations:me_metrics_overview_export_csv",
                name_xlsx="operations:me_metrics_overview_export_xlsx",
                weeks=weeks,
            )
        )
        return ctx


class MEMetricsRidersView(LoginRequiredMixin, MERequiredMixin, TemplateView):
    template_name = "operations/me/metrics_riders.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        weeks = parse_weeks_param(self.request.GET.get("weeks"))
        table = build_me_report_table(weeks=weeks)
        ctx["me_report"] = table
        ctx.update(_me_export_weeks_context(weeks=weeks, table=table, url_name="me_metrics_riders"))
        ctx.update(
            me_matrix_export_hrefs(
                name_csv="operations:me_metrics_riders_export_csv",
                name_xlsx="operations:me_metrics_riders_export_xlsx",
                weeks=weeks,
            )
        )
        return ctx


class MEMetricsDriversView(LoginRequiredMixin, MERequiredMixin, TemplateView):
    template_name = "operations/me/metrics_drivers.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        weeks = parse_weeks_param(self.request.GET.get("weeks"))
        table = build_driver_me_report_table(weeks=weeks)
        ctx["me_driver_report"] = table
        ctx.update(_me_export_weeks_context(weeks=weeks, table=table, url_name="me_metrics_drivers"))
        ctx.update(
            me_matrix_export_hrefs(
                name_csv="operations:me_metrics_drivers_export_csv",
                name_xlsx="operations:me_metrics_drivers_export_xlsx",
                weeks=weeks,
            )
        )
        return ctx


class MEMetricsReferredSamplesView(LoginRequiredMixin, MERequiredMixin, TemplateView):
    template_name = "operations/me/metrics_referred_samples.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        weeks = parse_weeks_param(self.request.GET.get("weeks"))
        table = build_me_referred_samples_table(weeks=weeks)
        ctx["me_referred_samples"] = table
        ctx.update(
            _me_export_weeks_context(weeks=weeks, table=table, url_name="me_metrics_referred_samples")
        )
        ctx.update(
            me_matrix_export_hrefs(
                name_csv="operations:me_metrics_referred_samples_export_csv",
                name_xlsx="operations:me_metrics_referred_samples_export_xlsx",
                weeks=weeks,
            )
        )
        return ctx


class MEAccidentsIncompleteView(LoginRequiredMixin, MERequiredMixin, TemplateView):
    """Read-only national accidents / incomplete transport for one calendar week."""

    template_name = "operations/me/accidents_incomplete.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        week_start = me_accidents_week_start_from_request(self.request)
        bundle = load_me_accidents_incomplete_data(week_start=week_start)
        transport_stats = bundle["transport_stats"]
        accident_details = bundle["accident_details"]

        ctx["selected_week_start"] = week_start
        ctx["week_range_label"] = week_range_label(week_start)
        ctx["me_prev_week"] = (week_start - timedelta(days=7)).isoformat()
        ctx["me_next_week"] = (week_start + timedelta(days=7)).isoformat()
        ctx["transport_stats"] = transport_stats
        ctx["accident_details"] = accident_details
        ctx.update(me_accidents_export_hrefs(week_iso=week_start.isoformat()))
        return ctx
