from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import UpdateView

from ..forms import PCReportForm, ReportReviewForm, RiderTripEntryPCFormSet, SampleRejectionFormSet
from ..models import ReportAuditLog, RiderTripEntry, RiderWeeklyReport
from ..permissions import can_edit_report_as_pc, require_pc
from ..selectors import (
    get_reports_queryset,
    report_audit_logs_for_user,
    reports_for_rider_week_in_scope,
)
from ..services import report_edit_service, report_service, weekly_review_service
from ..services.week_fuel_service import (
    apply_week_fuel_distance_rollup,
    parse_week_fuel_bulk_post,
    parse_week_fuel_pc_post,
    upsert_rider_week_fuel_summary,
    week_fuel_totals_for_report,
    week_fuel_totals_from_bulk_post,
    week_fuel_totals_from_pc_post,
)
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
                ctx["trip_formset"] = RiderTripEntryPCFormSet(
                    self.request.POST,
                    instance=self.object,
                    prefix="trips",
                    queryset=trip_qs,
                    **kw,
                )
            else:
                ctx["trip_formset"] = RiderTripEntryPCFormSet(
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
        rider_week_reports = (
            get_reports_queryset(self.request.user)
            .filter(rider=report.rider, week_start=report.week_start)
            .select_related("rider", "rider__profile")
            .order_by("created_at", "pk")
        )
        ctx["rider_week_reports"] = [
            {
                "report": r,
                "can_edit": can_edit_report_as_pc(self.request.user, r),
            }
            for r in rider_week_reports
        ]
        submitted_statuses = (
            RiderWeeklyReport.Status.SUBMITTED,
            RiderWeeklyReport.Status.UNDER_REVIEW,
            RiderWeeklyReport.Status.APPROVED,
            RiderWeeklyReport.Status.REJECTED,
        )
        submitted_week_reports = RiderWeeklyReport.objects.filter(
            rider=report.rider,
            week_start=report.week_start,
            status__in=submitted_statuses,
        ).values_list("pk", flat=True)
        ctx["pc_visit_count"] = RiderTripEntry.objects.filter(
            report_id__in=submitted_week_reports
        ).count()
        if ctx.get("is_pc_edit"):
            if pc_fuel_post_override is not None:
                ctx["pc_fuel_week_totals"] = week_fuel_totals_from_pc_post(pc_fuel_post_override)
            else:
                ctx["pc_fuel_week_totals"] = week_fuel_totals_for_report(report)
            ctx["pc_fuel_aggregate_errors"] = list(pc_fuel_aggregate_errors or [])
        return ctx

    def form_valid(self, form):
        action = (self.request.POST.get("action") or "save").strip().lower()
        kw = _pc_trip_formset_kwargs(self.request.user)
        trip_formset = RiderTripEntryPCFormSet(
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
            fuel_alloc, fuel_used = parse_week_fuel_pc_post(self.request.POST)
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
        rejection_formset = SampleRejectionFormSet(
            self.request.POST, instance=self.object, prefix="rejections"
        )
        if not rejection_formset.is_valid():
            return self.render_to_response(
                self.get_context_data(
                    form=form,
                    trip_formset=trip_formset,
                    rejection_formset=rejection_formset,
                    pc_fuel_post_override=self.request.POST,
                )
            )
        track = ["pc_notes", "scheduled_visits"]
        before = {k: getattr(self.object, k) for k in track}
        with transaction.atomic():
            self.object = form.save()
            trip_formset.instance = self.object
            trip_formset.save()
            _resequence_trip_entries(self.object)
            apply_week_fuel_distance_rollup(
                self.object, fuel_alloc, fuel_used
            )
            upsert_rider_week_fuel_summary(
                self.object.rider_id, self.object.week_start, fuel_alloc, fuel_used
            )
            _rollup_totals(self.object)
            rejection_formset.instance = self.object
            rejection_formset.save()
            self.object.refresh_from_db()
            report_service.complete_review(
                self.object,
                self.request.user,
                approved=True,
                pc_notes=self.object.pc_notes or "",
            )
            if action == "review":
                weekly_review_service.create_weekly_review_record(
                    source_report=self.object,
                    reviewer=self.request.user,
                )
        after = {k: getattr(self.object, k) for k in track}
        changed = [k for k in track if before.get(k) != after.get(k)]
        report_edit_service.record_pc_edit(
            self.object,
            self.request.user,
            summary=f"PC edit: {', '.join(changed) or 'save'}",
            diff_data={"before": before, "after": after},
        )
        if action == "review":
            messages.success(self.request, "Review recorded and snapshot saved.")
        else:
            messages.success(self.request, "Record saved.")
        return redirect("operations:pc_reports")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        action = (request.POST.get("action") or "save").strip().lower()
        if action == "review":
            track = ["pc_notes", "scheduled_visits"]
            before = {k: getattr(self.object, k) for k in track}

            self.object.pc_notes = request.POST.get("pc_notes", "")
            raw_scheduled = (request.POST.get("scheduled_visits") or "").strip()
            if raw_scheduled == "":
                self.object.scheduled_visits = None
            else:
                try:
                    self.object.scheduled_visits = int(raw_scheduled)
                except (TypeError, ValueError):
                    # For review action we do not block on invalid user input.
                    pass
            self.object.save(update_fields=["pc_notes", "scheduled_visits", "updated_at"])

            report_service.complete_review(
                self.object,
                request.user,
                approved=True,
                pc_notes=self.object.pc_notes or "",
            )
            weekly_review_service.create_weekly_review_record(
                source_report=self.object,
                reviewer=request.user,
            )
            self.object.refresh_from_db()
            after = {k: getattr(self.object, k) for k in track}
            changed = [k for k in track if before.get(k) != after.get(k)]
            report_edit_service.record_pc_edit(
                self.object,
                request.user,
                summary=f"PC review: {', '.join(changed) or 'review'}",
                diff_data={"before": before, "after": after},
            )
            messages.success(request, "Review recorded and snapshot saved.")
            return redirect("operations:pc_reports")
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        w = self.object.week_start.isoformat()
        return f"{reverse('operations:pc_reports')}?{urlencode({'week': w})}"


class PCBulkWeekEditView(LoginRequiredMixin, View):
    template_name = "operations/reports/pc_report_bulk_edit.html"

    def dispatch(self, request, *args, **kwargs):
        require_pc(request.user)
        return super().dispatch(request, *args, **kwargs)

    def _week_start(self):
        week_str = self.kwargs["week_str"]
        week_start = parse_date(week_str)
        if week_start is None:
            from django.http import Http404

            raise Http404("Invalid week value")
        return week_start

    def _reports(self):
        return list(
            reports_for_rider_week_in_scope(
                self.request.user, self.kwargs["rider_id"], self.kwargs["week_str"]
            )
            .select_related("rider", "rider__profile", "bike", "car")
            .prefetch_related("trip_entries", "sample_rejections")
            .order_by("created_at", "pk")
        )

    def _build_bundle(self, report, *, post_data=None):
        form_prefix = f"report_{report.pk}"
        trip_prefix = f"trips_{report.pk}"
        rej_prefix = f"rejections_{report.pk}"
        kw = _pc_trip_formset_kwargs(self.request.user)
        trip_qs = report.trip_entries.all().order_by("sequence", "pk")
        if post_data is not None:
            form = PCReportForm(post_data, instance=report, prefix=form_prefix)
            trip_formset = RiderTripEntryPCFormSet(
                post_data,
                instance=report,
                prefix=trip_prefix,
                queryset=trip_qs,
                **kw,
            )
            rejection_formset = SampleRejectionFormSet(
                post_data, instance=report, prefix=rej_prefix
            )
            fuel_totals = week_fuel_totals_from_bulk_post(post_data, report.pk)
        else:
            form = PCReportForm(instance=report, prefix=form_prefix)
            trip_formset = RiderTripEntryPCFormSet(
                instance=report,
                prefix=trip_prefix,
                queryset=trip_qs,
                **kw,
            )
            rejection_formset = SampleRejectionFormSet(instance=report, prefix=rej_prefix)
            fuel_totals = week_fuel_totals_for_report(report)
        return {
            "report": report,
            "can_edit": can_edit_report_as_pc(self.request.user, report),
            "form": form,
            "trip_formset": trip_formset,
            "rejection_formset": rejection_formset,
            "fuel_totals": fuel_totals,
            "fuel_errors": [],
        }

    def _context(self, bundles):
        first_report = bundles[0]["report"]
        rider_user = first_report.rider
        loc = _report_location_for_user(rider_user)
        return {
            "bundles": bundles,
            "week_start": first_report.week_start,
            "report_location": loc,
            "demographics": {
                "rider_name": rider_user.get_full_name() or rider_user.username,
                "province": loc["province_name"],
                "district": loc["district_name"],
            },
            "is_pc_edit": True,
            "bulk_edit": True,
            **_report_form_ajax_context(),
        }

    def get(self, request, *args, **kwargs):
        reports = self._reports()
        if not reports:
            messages.error(request, "No reports found for this rider and week in your scope.")
            return redirect("operations:pc_reports")
        bundles = [self._build_bundle(r) for r in reports]
        return self.render_to_response(self._context(bundles))

    def render_to_response(self, context, **response_kwargs):
        from django.shortcuts import render

        return render(self.request, self.template_name, context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        reports = self._reports()
        if not reports:
            messages.error(request, "No reports found for this rider and week in your scope.")
            return redirect("operations:pc_reports")
        action = (request.POST.get("action") or "save_all").strip().lower()
        bundles = [self._build_bundle(r, post_data=request.POST) for r in reports]
        editable_bundles = [b for b in bundles if b["can_edit"]]

        if action == "review_all":
            reviewed = 0
            with transaction.atomic():
                for bundle in editable_bundles:
                    report = bundle["report"]
                    form = bundle["form"]
                    # Review-all is best-effort and does not block on validation.
                    report.pc_notes = form.data.get(form.add_prefix("pc_notes"), report.pc_notes) or ""
                    raw_scheduled = (form.data.get(form.add_prefix("scheduled_visits")) or "").strip()
                    if raw_scheduled == "":
                        report.scheduled_visits = None
                    else:
                        try:
                            report.scheduled_visits = int(raw_scheduled)
                        except (TypeError, ValueError):
                            pass
                    report.save(update_fields=["pc_notes", "scheduled_visits", "updated_at"])
                    report_service.complete_review(
                        report,
                        request.user,
                        approved=True,
                        pc_notes=report.pc_notes or "",
                    )
                    weekly_review_service.create_weekly_review_record(
                        source_report=report,
                        reviewer=request.user,
                    )
                    report_edit_service.record_pc_edit(
                        report,
                        request.user,
                        summary="PC bulk review",
                        diff_data={"action": "bulk_review_all"},
                    )
                    reviewed += 1
            messages.success(request, f"Reviewed {reviewed} record(s).")
            week = self._week_start().isoformat()
            return redirect(f"{reverse('operations:pc_reports')}?{urlencode({'week': week})}")

        # save_all path: full validation before commit.
        has_errors = False
        parsed_fuel = {}
        for bundle in editable_bundles:
            form = bundle["form"]
            trip_formset = bundle["trip_formset"]
            rejection_formset = bundle["rejection_formset"]
            if not form.is_valid():
                has_errors = True
            if not trip_formset.is_valid():
                has_errors = True
            if not rejection_formset.is_valid():
                has_errors = True
            try:
                fuel_alloc, fuel_used = parse_week_fuel_bulk_post(
                    request.POST, bundle["report"].pk
                )
                if fuel_used > fuel_alloc:
                    bundle["fuel_errors"].append(
                        "Fuel used cannot exceed fuel allocated (week totals)."
                    )
                    has_errors = True
                parsed_fuel[bundle["report"].pk] = (fuel_alloc, fuel_used)
            except ValueError as exc:
                bundle["fuel_errors"].append(str(exc))
                has_errors = True
        if has_errors:
            return self.render_to_response(self._context(bundles))

        saved = 0
        with transaction.atomic():
            for bundle in editable_bundles:
                report = bundle["report"]
                form = bundle["form"]
                trip_formset = bundle["trip_formset"]
                rejection_formset = bundle["rejection_formset"]
                before = {
                    "pc_notes": report.pc_notes,
                    "scheduled_visits": report.scheduled_visits,
                }
                report = form.save()
                trip_formset.instance = report
                trip_formset.save()
                _resequence_trip_entries(report)
                fuel_alloc, fuel_used = parsed_fuel[report.pk]
                apply_week_fuel_distance_rollup(report, fuel_alloc, fuel_used)
                upsert_rider_week_fuel_summary(
                    report.rider_id, report.week_start, fuel_alloc, fuel_used
                )
                _rollup_totals(report)
                rejection_formset.instance = report
                rejection_formset.save()
                report.refresh_from_db()
                after = {
                    "pc_notes": report.pc_notes,
                    "scheduled_visits": report.scheduled_visits,
                }
                changed = [k for k in before if before[k] != after[k]]
                report_edit_service.record_pc_edit(
                    report,
                    request.user,
                    summary=f"PC bulk save: {', '.join(changed) or 'save'}",
                    diff_data={"before": before, "after": after},
                )
                saved += 1
        messages.success(request, f"Saved {saved} record(s).")
        week = self._week_start().isoformat()
        return redirect(f"{reverse('operations:pc_reports')}?{urlencode({'week': week})}")


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
