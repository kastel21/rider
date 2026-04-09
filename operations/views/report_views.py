import json
import uuid
from datetime import timedelta
from decimal import Decimal
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import RiderOperationalForm, RiderTripEntryFormSet, SampleRejectionFormSet
from ..models import Facility, RiderTripEntry, RiderWeeklyReport, TripTransportKind, UserProfile
from ..permissions import (
    can_edit_report_as_pc,
    can_edit_report_as_rider,
    can_view_report,
    is_rider_like,
)
from ..selectors import (
    facilities_for_ajax,
    get_reports_queryset,
    pc_province_ids,
    rider_home_profile_metrics,
    rider_home_weekly_trends,
    week_range_label,
    week_saved_trip_entries,
    week_start_from_request,
)
from ..services import report_service
from ..services.trip_facilities import facilities_for_rider_endpoint
from ..services.sync_service import apply_sync_batch, register_device


def _report_location_for_user(user):
    """Match dashboard PWA report_location context (province / district / PEPFAR line)."""
    rider_profile = getattr(user, "rider_profile", None)
    district = getattr(rider_profile, "district", None) if rider_profile else None
    province = None
    if district is not None:
        province = getattr(district, "province", None)
    if province is None and rider_profile is not None:
        province = getattr(rider_profile, "province", None)
    pepfar = "—"
    if rider_profile:
        if rider_profile.support_type:
            pepfar = rider_profile.get_support_type_display()
        elif district and district.support_type:
            pepfar = district.get_support_type_display()
    return {
        "province_name": getattr(province, "name", None) or "—",
        "district_name": getattr(district, "name", None) or "—",
        "pepfar_support_type": pepfar,
    }


def _monday_of_current_week():
    d = timezone.localdate()
    return d - timedelta(days=d.weekday())


def _week_saved_table_context(report, rider, week_start_monday):
    """Read-only trip rows for the form's week (DB state)."""
    return {
        "week_saved_trips": week_saved_trip_entries(
            report=report, rider=rider, week_start_monday=week_start_monday
        ),
        "week_range_label": week_range_label(week_start_monday),
    }


def _trip_formset_kwargs(user, *, for_pc: bool):
    if for_pc:
        return {"user": user, "pc_province_ids": pc_province_ids(user)}
    return {"user": user, "pc_province_ids": None}


def _pc_trip_formset_kwargs(user):
    kw = _trip_formset_kwargs(user, for_pc=True)
    kw["include_transport_kind"] = True
    return kw


def _report_form_ajax_context():
    url = reverse("operations:report_facilities_ajax")
    return {
        "report_facilities_ajax_url": url,
        "rider_scoped_facilities_ajax_url": url,
    }


def _driver_trip_formset_kwargs(user):
    kw = _trip_formset_kwargs(user, for_pc=False)
    kw["driver_dual_mode"] = True
    return kw


def _resequence_trip_entries(report):
    """
    Assign sequence 1..n across all trip rows: relayed and legacy together, then
    first-transport (stable within each group via prior sequence and pk).
    """
    kind_order = {
        TripTransportKind.RELAYED: 0,
        TripTransportKind.LEGACY: 0,
        TripTransportKind.FIRST_TRANSPORT: 1,
    }
    entries = list(report.trip_entries.all())
    entries.sort(key=lambda e: (kind_order.get(e.transport_kind, 9), e.sequence, e.pk))
    for i, e in enumerate(entries, start=1):
        e.sequence = i
    if entries:
        RiderTripEntry.objects.bulk_update(entries, ["sequence"])


def _rollup_totals(report):
    rows = report.trip_entries.all()
    report.samples_collected = sum(
        (
            r.vl_blood_plasma
            + r.vl_dbs
            + r.eid_blood
            + r.eid_dbs
            + r.sputum
            + r.sputum_culture_dr
            + r.hpv
        )
        for r in rows
    )
    report.save(update_fields=["samples_collected", "updated_at"])


class RiderReportListView(LoginRequiredMixin, ListView):
    model = RiderWeeklyReport
    context_object_name = "reports"

    def get_queryset(self):
        qs = get_reports_queryset(self.request.user)
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None
        if role == UserProfile.Role.PC:
            week_start = week_start_from_request(self.request)
            qs = (
                qs.filter(week_start=week_start)
                .select_related(
                    "rider",
                    "bike",
                    "car",
                    "rider__rider_profile__district",
                    "rider__rider_profile__district__province",
                )
                .annotate(week_trip_count=Count("trip_entries"))
                .order_by(
                    "rider__first_name",
                    "rider__last_name",
                    "rider__username",
                    "pk",
                )
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None

        if role == UserProfile.Role.PC:
            week_start = week_start_from_request(self.request)
            ctx["selected_week_start"] = week_start
            ctx["week_range_label"] = week_range_label(week_start)
            ctx["pc_prev_week"] = (week_start - timedelta(days=7)).isoformat()
            ctx["pc_next_week"] = (week_start + timedelta(days=7)).isoformat()
            user = self.request.user
            ctx["pc_report_rows"] = [
                {"report": r, "can_edit": can_edit_report_as_pc(user, r)}
                for r in self.object_list
            ]
            return ctx

        if not is_rider_like(self.request.user):
            return ctx
        week_start = week_start_from_request(self.request)
        qs = get_reports_queryset(self.request.user)
        week_report = (
            qs.filter(week_start=week_start)
            .select_related("bike", "car")
            .prefetch_related("trip_entries")
            .first()
        )
        ctx["week_start_monday"] = week_start
        ctx["selected_week_start"] = week_start
        ctx["week_range_label"] = week_range_label(week_start)
        ctx["week_report"] = week_report
        ctx["rider_profile_metrics"] = rider_home_profile_metrics(self.request.user)
        ctx["rider_trend_chart_data"] = rider_home_weekly_trends(self.request.user, num_weeks=12)
        if week_report:
            trips = list(week_report.trip_entries.all())
            total_distance = sum(
                (t.distance_travelled if t.distance_travelled is not None else Decimal("0") for t in trips),
                Decimal("0"),
            )
            total_results = sum((t.results_total for t in trips), 0)
            ctx["week_metrics"] = {
                "status_display": week_report.get_status_display(),
                "samples_collected": week_report.samples_collected,
                "trip_count": len(trips),
                "total_distance": total_distance,
                "total_results": total_results,
            }
            ctx["week_report_can_edit"] = can_edit_report_as_rider(self.request.user, week_report)
        else:
            ctx["week_metrics"] = None
            ctx["week_report_can_edit"] = False
        return ctx

    def get_template_names(self):
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None
        if role == UserProfile.Role.PC:
            return ["operations/reports/pc_report_list.html"]
        if role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER):
            return ["operations/reports/rider_report_list.html"]
        return ["operations/reports/report_list.html"]


class RiderReportCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = RiderWeeklyReport
    form_class = RiderOperationalForm
    template_name = "operations/reports/report_form.html"

    def test_func(self):
        return is_rider_like(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        kw = _trip_formset_kwargs(self.request.user, for_pc=False)
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None

        if role == UserProfile.Role.DRIVER:
            dk = _driver_trip_formset_kwargs(self.request.user)
            if "trip_formset_relay" not in ctx and "trip_formset_first" not in ctx:
                if self.request.method == "POST":
                    ctx["trip_formset_relay"] = RiderTripEntryFormSet(
                        self.request.POST,
                        prefix="trips_relay",
                        queryset=RiderTripEntry.objects.none(),
                        fixed_transport_kind=TripTransportKind.RELAYED,
                        **dk,
                    )
                    ctx["trip_formset_first"] = RiderTripEntryFormSet(
                        self.request.POST,
                        prefix="trips_first",
                        queryset=RiderTripEntry.objects.none(),
                        fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                        **dk,
                    )
                else:
                    ctx["trip_formset_relay"] = RiderTripEntryFormSet(
                        prefix="trips_relay",
                        queryset=RiderTripEntry.objects.none(),
                        fixed_transport_kind=TripTransportKind.RELAYED,
                        **dk,
                    )
                    ctx["trip_formset_first"] = RiderTripEntryFormSet(
                        prefix="trips_first",
                        queryset=RiderTripEntry.objects.none(),
                        fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                        **dk,
                    )
            ctx["driver_dual_tabs"] = True
        else:
            if "trip_formset" not in ctx:
                if self.request.method == "POST":
                    ctx["trip_formset"] = RiderTripEntryFormSet(
                        self.request.POST,
                        prefix="trips",
                        queryset=RiderTripEntry.objects.none(),
                        **kw,
                    )
                else:
                    ctx["trip_formset"] = RiderTripEntryFormSet(
                        prefix="trips",
                        queryset=RiderTripEntry.objects.none(),
                        **kw,
                    )
            ctx["driver_dual_tabs"] = False
        rider_profile = getattr(self.request.user, "rider_profile", None)
        loc = _report_location_for_user(self.request.user)
        ctx["demographics"] = {
            "rider_name": self.request.user.get_full_name() or self.request.user.username,
            "province": loc["province_name"],
            "district": loc["district_name"],
        }
        ctx["report_location"] = loc
        ctx["is_rider_form"] = True
        ctx["is_rider_scoped"] = True
        ctx.update(_report_form_ajax_context())
        if "rejection_formset" not in ctx:
            if self.request.method == "POST":
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    self.request.POST, instance=RiderWeeklyReport(), prefix="rejections"
                )
            else:
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    instance=RiderWeeklyReport(), prefix="rejections"
                )
        ctx.update(_week_saved_table_context(None, self.request.user, _monday_of_current_week()))
        ctx["sync_week_start"] = _monday_of_current_week().isoformat()
        ctx["offline_client_uuid"] = str(uuid.uuid4())
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["rider_user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None

        week_start = _monday_of_current_week()
        existing = RiderWeeklyReport.objects.filter(
            rider=self.request.user,
            week_start=week_start,
        ).first()
        if existing and not can_edit_report_as_rider(self.request.user, existing):
            messages.info(
                self.request,
                "You already have a report for this week; it cannot be edited here.",
            )
            return redirect("operations:report_detail", pk=existing.pk)

        if role == UserProfile.Role.DRIVER:
            dk = _driver_trip_formset_kwargs(self.request.user)
            if existing:
                relay_qs = existing.trip_entries.filter(
                    transport_kind=TripTransportKind.RELAYED
                )
                first_qs = existing.trip_entries.filter(
                    transport_kind=TripTransportKind.FIRST_TRANSPORT
                )
            else:
                relay_qs = RiderTripEntry.objects.none()
                first_qs = RiderTripEntry.objects.none()
            trip_relay = RiderTripEntryFormSet(
                self.request.POST,
                instance=existing if existing else None,
                prefix="trips_relay",
                queryset=relay_qs,
                fixed_transport_kind=TripTransportKind.RELAYED,
                **dk,
            )
            trip_first = RiderTripEntryFormSet(
                self.request.POST,
                instance=existing if existing else None,
                prefix="trips_first",
                queryset=first_qs,
                fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                **dk,
            )
            if not trip_relay.is_valid() or not trip_first.is_valid():
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        trip_formset_relay=trip_relay,
                        trip_formset_first=trip_first,
                    )
                )
        else:
            kw = _trip_formset_kwargs(self.request.user, for_pc=False)
            trip_fs_kwargs = dict(prefix="trips", **kw)
            if existing:
                trip_fs_kwargs["queryset"] = existing.trip_entries.filter(
                    transport_kind=TripTransportKind.LEGACY
                )
            else:
                trip_fs_kwargs["queryset"] = RiderTripEntry.objects.none()
            trip_formset = RiderTripEntryFormSet(
                self.request.POST,
                instance=existing if existing else None,
                **trip_fs_kwargs,
            )
            if not trip_formset.is_valid():
                return self.render_to_response(
                    self.get_context_data(form=form, trip_formset=trip_formset)
                )
        rider_profile = getattr(self.request.user, "rider_profile", None)
        if existing:
            form.instance = existing
        else:
            form.instance.rider = self.request.user
            form.instance.week_start = week_start
        if rider_profile and rider_profile.district_id:
            form.instance.title = f"{rider_profile.district.province.name} / {rider_profile.district.name}"
        cu = (self.request.POST.get("client_uuid") or "").strip()
        if cu:
            try:
                uid = uuid.UUID(cu)
                if form.instance.client_uuid is None:
                    form.instance.client_uuid = uid
            except (ValueError, TypeError):
                pass
        try:
            with transaction.atomic():
                self.object = form.save()
                if role == UserProfile.Role.DRIVER:
                    trip_relay.instance = self.object
                    trip_first.instance = self.object
                    trip_relay.save()
                    trip_first.save()
                    _resequence_trip_entries(self.object)
                else:
                    trip_formset.instance = self.object
                    trip_formset.save()
                    _resequence_trip_entries(self.object)
                rejection_formset = SampleRejectionFormSet(
                    self.request.POST, instance=self.object, prefix="rejections"
                )
                if not rejection_formset.is_valid():
                    transaction.set_rollback(True)
                    ctx = self.get_context_data(
                        form=form,
                        rejection_formset=rejection_formset,
                    )
                    if role == UserProfile.Role.DRIVER:
                        ctx["trip_formset_relay"] = trip_relay
                        ctx["trip_formset_first"] = trip_first
                    else:
                        ctx["trip_formset"] = trip_formset
                    return self.render_to_response(ctx)
                rejection_formset.save()
        except Exception:
            raise
        _rollup_totals(self.object)
        is_submit = self.request.POST.get("action") == "submit"
        if is_submit:
            report_service.submit_report(self.object, self.request.user)
            messages.success(self.request, "Report saved and submitted.")
            return redirect("operations:role_redirect")
        messages.success(
            self.request,
            "Draft saved. Saved trips appear in the table below; add more if needed.",
        )
        edit_url = reverse("operations:report_edit", kwargs={"pk": self.object.pk})
        return redirect(f"{edit_url}?draft_cleared=1")

    def get_success_url(self):
        return reverse("operations:report_detail", kwargs={"pk": self.object.pk})


class RiderReportDetailView(LoginRequiredMixin, DetailView):
    model = RiderWeeklyReport
    template_name = "operations/reports/report_detail.html"
    context_object_name = "report"

    def get_queryset(self):
        return (
            get_reports_queryset(self.request.user)
            .select_related(
                "bike",
                "car",
                "rider",
                "rider__profile",
                "rider__rider_profile__district",
                "rider__rider_profile__district__province",
            )
            .prefetch_related(
                "trip_entries__origin_facility",
                "trip_entries__destination_facility",
                "sample_rejections",
            )
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_view_report(self.request.user, obj):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        report = self.object
        user = self.request.user
        ctx["rider_can_edit"] = can_edit_report_as_rider(user, report)
        ctx["pc_can_edit"] = can_edit_report_as_pc(user, report)

        week_start = report.week_start
        ctx["week_range_label"] = week_range_label(week_start)
        trips = list(report.trip_entries.all())
        total_distance = sum(
            (t.distance_travelled if t.distance_travelled is not None else Decimal("0") for t in trips),
            Decimal("0"),
        )
        total_results = sum((t.results_total for t in trips), 0)
        ctx["week_metrics"] = {
            "status_display": report.get_status_display(),
            "samples_collected": report.samples_collected,
            "trip_count": len(trips),
            "total_distance": total_distance,
            "total_results": total_results,
        }
        rider = report.rider
        loc = _report_location_for_user(rider)
        ctx["report_subject"] = {
            "name": rider.get_full_name() or rider.username,
            "district": loc["district_name"],
            "province": loc["province_name"],
        }

        try:
            role = user.profile.role
        except UserProfile.DoesNotExist:
            role = None
        if role == UserProfile.Role.PC:
            base = reverse("operations:pc_reports")
            ctx["detail_back_url"] = f"{base}?{urlencode({'week': week_start.isoformat()})}"
        elif role in (UserProfile.Role.RIDER, UserProfile.Role.DRIVER):
            ctx["detail_back_url"] = reverse("operations:rider_reports")
        elif role == UserProfile.Role.ME:
            ctx["detail_back_url"] = reverse("operations:me_reports")
        else:
            ctx["detail_back_url"] = reverse("operations:rider_reports")

        return ctx


class RiderReportEditView(LoginRequiredMixin, UpdateView):
    model = RiderWeeklyReport
    form_class = RiderOperationalForm
    template_name = "operations/reports/report_form.html"
    context_object_name = "report"

    def get_queryset(self):
        return get_reports_queryset(self.request.user)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        kw = _trip_formset_kwargs(self.request.user, for_pc=False)
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None

        draft_cleared = (
            self.request.method != "POST"
            and self.request.GET.get("draft_cleared") == "1"
        )

        if role == UserProfile.Role.DRIVER:
            dk = _driver_trip_formset_kwargs(self.request.user)
            relay_qs = self.object.trip_entries.filter(transport_kind=TripTransportKind.RELAYED)
            first_qs = self.object.trip_entries.filter(
                transport_kind=TripTransportKind.FIRST_TRANSPORT
            )
            if draft_cleared:
                relay_qs = self.object.trip_entries.none()
                first_qs = self.object.trip_entries.none()
            if "trip_formset_relay" not in ctx and "trip_formset_first" not in ctx:
                if self.request.method == "POST":
                    ctx["trip_formset_relay"] = RiderTripEntryFormSet(
                        self.request.POST,
                        instance=self.object,
                        prefix="trips_relay",
                        queryset=relay_qs,
                        fixed_transport_kind=TripTransportKind.RELAYED,
                        **dk,
                    )
                    ctx["trip_formset_first"] = RiderTripEntryFormSet(
                        self.request.POST,
                        instance=self.object,
                        prefix="trips_first",
                        queryset=first_qs,
                        fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                        **dk,
                    )
                else:
                    ctx["trip_formset_relay"] = RiderTripEntryFormSet(
                        instance=self.object,
                        prefix="trips_relay",
                        queryset=relay_qs,
                        fixed_transport_kind=TripTransportKind.RELAYED,
                        **dk,
                    )
                    ctx["trip_formset_first"] = RiderTripEntryFormSet(
                        instance=self.object,
                        prefix="trips_first",
                        queryset=first_qs,
                        fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                        **dk,
                    )
            ctx["driver_dual_tabs"] = True
        else:
            if "trip_formset" not in ctx:
                trip_fs_kwargs = dict(prefix="trips", **kw)
                trip_fs_kwargs["queryset"] = self.object.trip_entries.filter(
                    transport_kind=TripTransportKind.LEGACY
                )
                if draft_cleared:
                    trip_fs_kwargs["queryset"] = self.object.trip_entries.none()
                if self.request.method == "POST":
                    ctx["trip_formset"] = RiderTripEntryFormSet(
                        self.request.POST, instance=self.object, **trip_fs_kwargs
                    )
                else:
                    ctx["trip_formset"] = RiderTripEntryFormSet(
                        instance=self.object, **trip_fs_kwargs
                    )
            ctx["driver_dual_tabs"] = False
        rider_profile = getattr(self.request.user, "rider_profile", None)
        loc = _report_location_for_user(self.request.user)
        ctx["demographics"] = {
            "rider_name": self.request.user.get_full_name() or self.request.user.username,
            "province": loc["province_name"],
            "district": loc["district_name"],
        }
        ctx["report_location"] = loc
        ctx["is_rider_form"] = True
        ctx["is_rider_scoped"] = True
        ctx.update(_report_form_ajax_context())
        if "rejection_formset" not in ctx:
            if self.request.method == "POST":
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    self.request.POST, instance=self.object, prefix="rejections"
                )
            else:
                ctx["rejection_formset"] = SampleRejectionFormSet(
                    instance=self.object, prefix="rejections"
                )
        ctx.update(
            _week_saved_table_context(self.object, self.request.user, self.object.week_start)
        )
        ctx["sync_week_start"] = self.object.week_start.isoformat()
        ctx["offline_client_uuid"] = (
            str(self.object.client_uuid) if self.object.client_uuid else str(uuid.uuid4())
        )
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["rider_user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not can_edit_report_as_rider(self.request.user, obj):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return obj

    def get_success_url(self):
        return reverse("operations:report_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None

        if role == UserProfile.Role.DRIVER:
            dk = _driver_trip_formset_kwargs(self.request.user)
            relay_qs = self.object.trip_entries.filter(transport_kind=TripTransportKind.RELAYED)
            first_qs = self.object.trip_entries.filter(
                transport_kind=TripTransportKind.FIRST_TRANSPORT
            )
            trip_relay = RiderTripEntryFormSet(
                self.request.POST,
                instance=self.object,
                prefix="trips_relay",
                queryset=relay_qs,
                fixed_transport_kind=TripTransportKind.RELAYED,
                **dk,
            )
            trip_first = RiderTripEntryFormSet(
                self.request.POST,
                instance=self.object,
                prefix="trips_first",
                queryset=first_qs,
                fixed_transport_kind=TripTransportKind.FIRST_TRANSPORT,
                **dk,
            )
            if not trip_relay.is_valid() or not trip_first.is_valid():
                return self.render_to_response(
                    self.get_context_data(
                        form=form,
                        trip_formset_relay=trip_relay,
                        trip_formset_first=trip_first,
                    )
                )
        else:
            kw = _trip_formset_kwargs(self.request.user, for_pc=False)
            trip_formset = RiderTripEntryFormSet(
                self.request.POST,
                instance=self.object,
                prefix="trips",
                queryset=self.object.trip_entries.filter(
                    transport_kind=TripTransportKind.LEGACY
                ),
                **kw,
            )
            if not trip_formset.is_valid():
                return self.render_to_response(
                    self.get_context_data(form=form, trip_formset=trip_formset)
                )
        rider_profile = getattr(self.request.user, "rider_profile", None)
        if rider_profile and rider_profile.district_id:
            form.instance.title = f"{rider_profile.district.province.name} / {rider_profile.district.name}"
        cu = (self.request.POST.get("client_uuid") or "").strip()
        if cu:
            try:
                form.instance.client_uuid = uuid.UUID(cu)
            except (ValueError, TypeError):
                pass
        try:
            with transaction.atomic():
                self.object = form.save()
                if role == UserProfile.Role.DRIVER:
                    trip_relay.instance = self.object
                    trip_first.instance = self.object
                    trip_relay.save()
                    trip_first.save()
                    _resequence_trip_entries(self.object)
                else:
                    trip_formset.instance = self.object
                    trip_formset.save()
                    _resequence_trip_entries(self.object)
                rejection_formset = SampleRejectionFormSet(
                    self.request.POST, instance=self.object, prefix="rejections"
                )
                if not rejection_formset.is_valid():
                    transaction.set_rollback(True)
                    ctx = self.get_context_data(
                        form=form,
                        rejection_formset=rejection_formset,
                    )
                    if role == UserProfile.Role.DRIVER:
                        ctx["trip_formset_relay"] = trip_relay
                        ctx["trip_formset_first"] = trip_first
                    else:
                        ctx["trip_formset"] = trip_formset
                    return self.render_to_response(ctx)
                rejection_formset.save()
        except Exception:
            raise
        _rollup_totals(self.object)
        is_submit = self.request.POST.get("action") == "submit"
        if is_submit:
            report_service.submit_report(self.object, self.request.user)
            messages.success(self.request, "Report saved and submitted.")
            return redirect("operations:role_redirect")
        messages.success(
            self.request,
            "Draft saved. Saved trips appear in the table below; add more if needed.",
        )
        edit_url = reverse("operations:report_edit", kwargs={"pk": self.object.pk})
        return redirect(f"{edit_url}?draft_cleared=1")


class ReportSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk, rider=request.user)
        if not can_edit_report_as_rider(request.user, report):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        report_service.submit_report(report, request.user)
        messages.success(request, "Report submitted.")
        return redirect("operations:report_detail", pk=pk)


class ReportFacilitiesAjaxView(LoginRequiredMixin, View):
    def get(self, request):
        raw_district = request.GET.get("district_id")
        district_id = int(raw_district) if raw_district and str(raw_district).isdigit() else None
        route_kind = (request.GET.get("route_kind") or "").strip()
        slot = (request.GET.get("slot") or "").strip()

        if route_kind and slot in ("from", "to"):
            qs = facilities_for_rider_endpoint(
                request.user,
                route_kind,
                slot,
                district_id=district_id,
            )
        elif is_rider_like(request.user):
            qs = Facility.objects.none()
        else:
            qs = facilities_for_ajax(request.user, district_id=district_id)
        data = [
            {
                "id": f.id,
                "name": f.name,
                "kind": f.kind,
                "district_id": f.district_id,
            }
            for f in qs[:500]
        ]
        return JsonResponse({"facilities": data})


class RiderRegisterDeviceView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            body = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            body = {}
        out = register_device(
            request.user,
            device_id=body.get("device_id", ""),
            platform=body.get("platform", ""),
            user_agent=body.get("user_agent", request.META.get("HTTP_USER_AGENT", "")),
        )
        return JsonResponse(out)


class RiderSyncView(LoginRequiredMixin, View):
    def post(self, request):
        if not is_rider_like(request.user):
            return JsonResponse({"ok": False, "error": "rider role required"}, status=403)
        try:
            body = json.loads(request.body.decode() or "{}")
        except json.JSONDecodeError:
            return JsonResponse({"ok": False, "error": "invalid json"}, status=400)
        operations = body.get("operations") or []
        if not isinstance(operations, list):
            return JsonResponse({"ok": False, "error": "operations must be a list"}, status=400)
        out = apply_sync_batch(request.user, operations)
        return JsonResponse(out)
