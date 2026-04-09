from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from ..forms import PCReportForm, ReportReviewForm, RiderTripEntryFormSet, SampleRejectionFormSet
from ..models import ReportAuditLog, RiderWeeklyReport
from ..permissions import can_edit_report_as_pc, require_pc
from ..selectors import (
    get_reports_queryset,
    report_audit_logs_for_user,
    reports_for_rider_week_in_scope,
)
from ..services import report_edit_service, report_service
from .report_views import (
    _pc_trip_formset_kwargs,
    _report_form_ajax_context,
    _report_location_for_user,
    _resequence_trip_entries,
    _rollup_totals,
    _week_saved_table_context,
)


class PCReportEditView(LoginRequiredMixin, UpdateView):
    model = RiderWeeklyReport
    form_class = PCReportForm
    template_name = "operations/reports/report_form.html"
    context_object_name = "report"

    def dispatch(self, request, *args, **kwargs):
        require_pc(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return get_reports_queryset(self.request.user).select_related(
            "bike",
            "car",
            "rider",
            "rider__profile",
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_report_as_pc(self.request.user, obj):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["is_pc_edit"] = True
        report = self.object
        rider_user = report.rider
        loc = _report_location_for_user(rider_user)
        ctx["report_location"] = loc
        ctx["demographics"] = {
            "rider_name": rider_user.get_full_name() or rider_user.username,
            "province": loc["province_name"],
            "district": loc["district_name"],
        }
        ctx["is_rider_form"] = False
        ctx["is_rider_scoped"] = False
        ctx.update(_report_form_ajax_context())
        kw = _pc_trip_formset_kwargs(self.request.user)
        trip_qs = self.object.trip_entries.all().order_by("sequence", "pk")
        if "trip_formset" not in ctx:
            if self.request.method == "POST":
                ctx["trip_formset"] = RiderTripEntryFormSet(
                    self.request.POST,
                    instance=self.object,
                    prefix="trips",
                    queryset=trip_qs,
                    **kw,
                )
            else:
                ctx["trip_formset"] = RiderTripEntryFormSet(
                    instance=self.object,
                    prefix="trips",
                    queryset=trip_qs,
                    **kw,
                )
        if "rejection_formset" not in ctx:
            if self.request.method == "POST":
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    self.request.POST, instance=self.object, prefix="rejections"
                )
            else:
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    instance=self.object, prefix="rejections"
                )
        report = self.object
        ctx.update(_week_saved_table_context(report, report.rider, report.week_start))
        ctx["pc_visit_count"] = report.trip_entries.count()
        return ctx

    def form_valid(self, form):
        kw = _pc_trip_formset_kwargs(self.request.user)
        trip_formset = RiderTripEntryFormSet(
            self.request.POST,
            instance=self.object,
            prefix="trips",
            queryset=self.object.trip_entries.all().order_by("sequence", "pk"),
            **kw,
        )
        if not trip_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(form=form, trip_formset=trip_formset)
            )
        track = ["pc_notes", "scheduled_visits"]
        before = {k: getattr(self.object, k) for k in track}
        try:
            with transaction.atomic():
                self.object = form.save()
                trip_formset.instance = self.object
                trip_formset.save()
                _resequence_trip_entries(self.object)
                _rollup_totals(self.object)
                rejection_formset = SampleRejectionFormSet(
                    self.request.POST, instance=self.object, prefix="rejections"
                )
                if not rejection_formset.is_valid():
                    transaction.set_rollback(True)
                    return self.render_to_response(
                        self.get_context_data(
                            form=form,
                            trip_formset=trip_formset,
                            rejection_formset=rejection_formset,
                        )
                    )
                rejection_formset.save()
                self.object.refresh_from_db()
                report_service.complete_review(
                    self.object,
                    self.request.user,
                    approved=True,
                    pc_notes=self.object.pc_notes or "",
                )
        except Exception:
            raise
        after = {k: getattr(self.object, k) for k in track}
        changed = [k for k in track if before.get(k) != after.get(k)]
        report_edit_service.record_pc_edit(
            self.object,
            self.request.user,
            summary=f"PC edit: {', '.join(changed) or 'save'}",
            diff_data={"before": before, "after": after},
        )
        messages.success(self.request, "Report saved and marked reviewed (approved).")
        return redirect(self.get_success_url())

    def get_success_url(self):
        w = self.object.week_start.isoformat()
        return f"{reverse('operations:pc_reports')}?{urlencode({'week': w})}"


class ReportEditHistoryView(LoginRequiredMixin, ListView):
    template_name = "operations/reports/report_edit_history.html"
    context_object_name = "snapshots"

    def dispatch(self, request, *args, **kwargs):
        require_pc(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["report"] = get_object_or_404(
            get_reports_queryset(self.request.user),
            pk=self.kwargs["pk"],
        )
        return ctx

    def get_queryset(self):
        report = get_object_or_404(
            get_reports_queryset(self.request.user),
            pk=self.kwargs["pk"],
        )
        return report.edit_snapshots.select_related("editor").all()


class ReportStartReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        require_pc(request.user)
        report = get_object_or_404(get_reports_queryset(request.user), pk=pk)
        report_service.start_review(report, request.user)
        messages.success(request, "Review started.")
        return redirect("operations:pc_report_edit", pk=pk)


class ReportReviewView(LoginRequiredMixin, View):
    def post(self, request, pk):
        require_pc(request.user)
        report = get_object_or_404(get_reports_queryset(request.user), pk=pk)
        form = ReportReviewForm(request.POST)
        approved = request.POST.get("approved") == "1"
        if form.is_valid():
            report_service.complete_review(
                report,
                request.user,
                approved=approved,
                pc_notes=form.cleaned_data.get("pc_notes", ""),
            )
        messages.success(request, "Review saved.")
        return redirect("operations:pc_reports")


class ReportStartReviewGroupView(LoginRequiredMixin, View):
    def post(self, request, rider_id, week_str):
        require_pc(request.user)
        qs = reports_for_rider_week_in_scope(request.user, rider_id, week_str)
        for report in qs:
            if report.status == RiderWeeklyReport.Status.SUBMITTED:
                report_service.start_review(report, request.user)
        messages.success(request, "Review started for group.")
        return redirect("operations:pc_reports")


class ReportReviewGroupView(LoginRequiredMixin, View):
    def post(self, request, rider_id, week_str):
        require_pc(request.user)
        form = ReportReviewForm(request.POST)
        approved = request.POST.get("approved") == "1"
        pc_notes = form.cleaned_data.get("pc_notes", "") if form.is_valid() else ""
        qs = reports_for_rider_week_in_scope(request.user, rider_id, week_str)
        for report in qs:
            report_service.complete_review(report, request.user, approved=approved, pc_notes=pc_notes)
        messages.success(request, "Group review saved.")
        return redirect("operations:pc_reports")


class ReportAuditLogListView(LoginRequiredMixin, ListView):
    model = ReportAuditLog
    template_name = "operations/reports/report_audit_log_list.html"
    context_object_name = "entries"

    def dispatch(self, request, *args, **kwargs):
        require_pc(request.user)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return report_audit_logs_for_user(self.request.user)
