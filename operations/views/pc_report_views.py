from decimal import Decimal, InvalidOperation
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from ..forms import PCReportForm, ReportReviewForm, RiderTripEntryFormSet, SampleRejectionFormSet
from ..models import ReportAuditLog, RiderTripEntry, RiderWeeklyReport
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


def _pc_fuel_week_totals_from_db(report: RiderWeeklyReport) -> dict:
    s = report.trip_entries.aggregate(
        a=Sum("fuel_allocated"),
        u=Sum("fuel_used"),
        d=Sum("distance_travelled"),
    )
    return {
        "allocated": str(s["a"] if s["a"] is not None else Decimal("0")),
        "used": str(s["u"] if s["u"] is not None else Decimal("0")),
        "distance": str(s["d"] if s["d"] is not None else Decimal("0")),
    }


def _pc_fuel_week_totals_from_post(post) -> dict:
    return {
        "allocated": (post.get("pc_fuel_allocated_total") or "0").strip(),
        "used": (post.get("pc_fuel_used_total") or "0").strip(),
        "distance": (post.get("pc_distance_travelled_total") or "0").strip(),
    }


def _parse_pc_fuel_week_post(post) -> tuple[Decimal, Decimal, Decimal]:
    def one(key: str) -> Decimal:
        raw = (post.get(key) or "").strip().replace(",", ".")
        if not raw:
            return Decimal("0")
        try:
            return Decimal(raw)
        except InvalidOperation as e:
            raise ValueError("Enter a valid number for week fuel or distance totals.") from e

    return (
        one("pc_fuel_allocated_total"),
        one("pc_fuel_used_total"),
        one("pc_distance_travelled_total"),
    )


def _apply_pc_week_fuel_distance_rollup(
    report: RiderWeeklyReport,
    fuel_allocated: Decimal,
    fuel_used: Decimal,
    distance: Decimal,
) -> None:
    qs = report.trip_entries.order_by("sequence", "pk")
    first = qs.first()
    if not first:
        return
    RiderTripEntry.objects.filter(pk=first.pk).update(
        fuel_allocated=fuel_allocated,
        fuel_used=fuel_used,
        distance_travelled=distance,
    )
    rest_ids = list(qs.exclude(pk=first.pk).values_list("pk", flat=True))
    if rest_ids:
        RiderTripEntry.objects.filter(pk__in=rest_ids).update(
            fuel_allocated=Decimal("0"),
            fuel_used=Decimal("0"),
            distance_travelled=Decimal("0"),
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
        pc_fuel_post_override = kwargs.pop("pc_fuel_post_override", None)
        pc_fuel_aggregate_errors = kwargs.pop("pc_fuel_aggregate_errors", None)
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
        if ctx.get("is_pc_edit"):
            if pc_fuel_post_override is not None:
                ctx["pc_fuel_week_totals"] = _pc_fuel_week_totals_from_post(pc_fuel_post_override)
            else:
                ctx["pc_fuel_week_totals"] = _pc_fuel_week_totals_from_db(report)
            ctx["pc_fuel_aggregate_errors"] = list(pc_fuel_aggregate_errors or [])
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
                self.get_context_data(
                    form=form,
                    trip_formset=trip_formset,
                    pc_fuel_post_override=self.request.POST,
                )
            )
        try:
            fuel_alloc, fuel_used, distance_km = _parse_pc_fuel_week_post(self.request.POST)
        except ValueError as exc:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    trip_formset=trip_formset,
                    pc_fuel_post_override=self.request.POST,
                    pc_fuel_aggregate_errors=[str(exc)],
                )
            )
        if fuel_used > fuel_alloc:
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    trip_formset=trip_formset,
                    pc_fuel_post_override=self.request.POST,
                    pc_fuel_aggregate_errors=[
                        "Fuel used cannot exceed fuel allocated (week totals)."
                    ],
                )
            )
        track = ["pc_notes", "scheduled_visits"]
        before = {k: getattr(self.object, k) for k in track}
        try:
            with transaction.atomic():
                self.object = form.save()
                trip_formset.instance = self.object
                trip_formset.save()
                _resequence_trip_entries(self.object)
                _apply_pc_week_fuel_distance_rollup(
                    self.object, fuel_alloc, fuel_used, distance_km
                )
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
                            pc_fuel_post_override=self.request.POST,
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
