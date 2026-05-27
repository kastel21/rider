import json
import uuid
from datetime import date, timedelta
from decimal import Decimal
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from ..forms import RiderOperationalForm, RiderTripEntryFormSet, SampleRejectionFormSet
from ..services.distance_km import round_distance_km
from ..models import Facility, RiderTripEntry, RiderWeeklyReport, TripTransportKind, UserProfile
from ..permissions import (
    MERequiredMixin,
    can_edit_report_as_pc,
    can_edit_report_as_rider,
    can_mark_me_review,
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
from ..services.week_fuel_service import (
    apply_week_fuel_distance_rollup,
    parse_week_fuel_pc_post,
    rider_week_fuel_totals_for_user_week,
    upsert_rider_week_fuel_summary,
    week_fuel_alloc_used_from_report,
    week_fuel_totals_from_pc_post,
)
from ..services.trip_facilities import facilities_for_rider_endpoint
from ..services.sync_service import apply_sync_batch, register_device
from ..services.sync_payload import report_sync_envelope


def _jwt_remote_sync_enabled():
    from django.conf import settings

    return (
        getattr(settings, "OPS_SYNC_MODE", "").strip() == "jwt"
        and bool(getattr(settings, "OPS_REMOTE_API_BASE", "").strip())
    )


def _sync_enqueue_context(request, report=None):
    """Template hints for offline-sync.js to queue remote uplink."""
    ctx = {}
    if not _jwt_remote_sync_enabled():
        return ctx
    pk = None
    if report is not None and getattr(report, "pk", None):
        pk = report.pk
    raw = (request.GET.get("remote_sync_report") or "").strip()
    if raw.isdigit():
        pk = int(raw)
    if request.GET.get("remote_sync") == "1" and report is not None and report.pk:
        pk = report.pk
    if pk:
        ctx["sync_enqueue_report_id"] = pk
    return ctx


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
    return {"user": user, "pc_province_ids": None, "pc_aggregate_fuel": True}


def _pc_trip_formset_kwargs(user):
    kw = _trip_formset_kwargs(user, for_pc=True)
    kw["include_transport_kind"] = True
    # Keep per-row fuel fields on the form for compatibility with validation/error
    # plumbing, while PC UI continues to use week-level aggregate inputs.
    kw["pc_aggregate_fuel"] = False
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
    # Drivers enter fuel per trip row (required numerics); riders use week-level fuel rollup.
    kw["pc_aggregate_fuel"] = False
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
                    "rider__profile",
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
        elif role in (UserProfile.Role.ME, UserProfile.Role.ADMIN):
            qs = qs.select_related(
                "rider",
                "rider__profile",
                "rider__rider_profile__district",
                "rider__rider_profile__district__province",
                "rider__rider_profile__province",
            ).order_by("-week_start", "-updated_at")
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
            rows = []
            for report in self.object_list:
                rows.append(
                    {
                        "report": report,
                        "can_edit": can_edit_report_as_pc(user, report),
                    }
                )
            grouped: dict[int, list[dict]] = {}
            for row in rows:
                grouped.setdefault(row["report"].rider_id, []).append(row)

            aggregated_rows: list[dict] = []
            for rider_id, rider_rows in grouped.items():
                # Prefer the most recently updated report as the representative row.
                sorted_rows = sorted(
                    rider_rows,
                    key=lambda rr: (rr["report"].updated_at, rr["report"].id),
                    reverse=True,
                )
                latest = sorted_rows[0]
                edit_candidate = next((rr for rr in sorted_rows if rr["can_edit"]), None)
                status_values = {rr["report"].status for rr in sorted_rows}
                aggregated_rows.append(
                    {
                        "report": latest["report"],
                        "can_edit": bool(edit_candidate),
                        "status_display": (
                            latest["report"].get_status_display()
                            if len(status_values) == 1
                            else "Mixed"
                        ),
                        "samples_total": sum(
                            (rr["report"].samples_collected or 0) for rr in sorted_rows
                        ),
                        "trip_total": sum((rr["report"].week_trip_count or 0) for rr in sorted_rows),
                        "submitted_at": max(
                            (
                                rr["report"].submitted_at
                                for rr in sorted_rows
                                if rr["report"].submitted_at is not None
                            ),
                            default=None,
                        ),
                    }
                )

            rider_rows: list[dict] = []
            driver_rows: list[dict] = []
            for row in aggregated_rows:
                role = getattr(getattr(row["report"].rider, "profile", None), "role", None)
                if role == UserProfile.Role.DRIVER:
                    driver_rows.append(row)
                else:
                    rider_rows.append(row)
            ctx["pc_rider_report_rows"] = rider_rows
            ctx["pc_driver_report_rows"] = driver_rows
            return ctx

        if role in (UserProfile.Role.ME, UserProfile.Role.ADMIN):
            st = RiderWeeklyReport.Status
            base_qs = self.object_list
            ctx["me_reports_drafts"] = base_qs.filter(status=st.DRAFT)
            ctx["me_reports_finalized"] = base_qs.filter(status=st.APPROVED)
            ctx["me_reports_with_pc"] = base_qs.exclude(status__in=[st.DRAFT, st.APPROVED])
            return ctx

        if not is_rider_like(self.request.user):
            return ctx
        week_start = week_start_from_request(self.request)
        qs = get_reports_queryset(self.request.user)
        week_reports = (
            qs.filter(week_start=week_start)
            .select_related("bike", "car")
            .prefetch_related("trip_entries")
            .order_by("-updated_at", "-id")
        )
        ctx["week_start_monday"] = week_start
        ctx["selected_week_start"] = week_start
        ctx["week_range_label"] = week_range_label(week_start)
        ctx["week_reports"] = week_reports
        ctx["week_report_rows"] = []
        ctx["rider_profile_metrics"] = rider_home_profile_metrics(self.request.user)
        ctx["rider_trend_chart_data"] = rider_home_weekly_trends(self.request.user, num_weeks=12)
        if week_reports:
            total_samples = 0
            total_trips = 0
            total_distance = Decimal("0")
            total_results = 0
            week_report_rows = []
            for week_report in week_reports:
                trips = list(week_report.trip_entries.all())
                trip_count = len(trips)
                total_samples += week_report.samples_collected or 0
                total_trips += trip_count
                total_distance += Decimal(
                    round_distance_km(week_report.distance_travelled)
                )
                total_results += sum((t.results_total for t in trips), 0)
                week_report_rows.append(
                    {
                        "report": week_report,
                        "trip_count": trip_count,
                        "can_edit": can_edit_report_as_rider(self.request.user, week_report),
                    }
                )
            ctx["week_report_rows"] = week_report_rows
            ctx["week_metrics"] = {
                "report_count": len(week_reports),
                "samples_collected": total_samples,
                "trip_count": total_trips,
                "total_distance": total_distance,
                "total_results": total_results,
            }
        else:
            ctx["week_metrics"] = None
        ctx.update(_sync_enqueue_context(self.request))
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
        if role in (UserProfile.Role.ME, UserProfile.Role.ADMIN):
            return ["operations/reports/me_report_list.html"]
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
        ctx["form_save_failed"] = self.request.method == "POST"
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

        if role == UserProfile.Role.DRIVER:
            dk = _driver_trip_formset_kwargs(self.request.user)
            relay_qs = RiderTripEntry.objects.none()
            first_qs = RiderTripEntry.objects.none()
            trip_relay = RiderTripEntryFormSet(
                self.request.POST,
                instance=None,
                prefix="trips_relay",
                queryset=relay_qs,
                fixed_transport_kind=TripTransportKind.RELAYED,
                **dk,
            )
            trip_first = RiderTripEntryFormSet(
                self.request.POST,
                instance=None,
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
            trip_fs_kwargs["queryset"] = RiderTripEntry.objects.none()
            trip_formset = RiderTripEntryFormSet(
                self.request.POST,
                instance=None,
                **trip_fs_kwargs,
            )
            if not trip_formset.is_valid():
                return self.render_to_response(
                    self.get_context_data(form=form, trip_formset=trip_formset)
                )
        fuel_snapshot = (Decimal("0"), Decimal("0"))
        rider_profile = getattr(self.request.user, "rider_profile", None)
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
                apply_week_fuel_distance_rollup(self.object, *fuel_snapshot)
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
            messages.success(
                self.request,
                "Report saved on this device. Cloud sync runs when you are online.",
            )
            if _jwt_remote_sync_enabled():
                url = reverse("operations:rider_reports")
                return redirect(
                    f"{url}?remote_sync_report={self.object.pk}&save_ok=submitted"
                )
            return redirect("operations:role_redirect")
        messages.success(
            self.request,
            "Report saved. Saved trips appear in the table below; add more if needed.",
        )
        edit_url = reverse("operations:report_edit", kwargs={"pk": self.object.pk})
        qs = "save_ok=1&draft_cleared=1"
        if _jwt_remote_sync_enabled():
            qs += "&remote_sync=1"
        return redirect(f"{edit_url}?{qs}")

    def get_success_url(self):
        if _jwt_remote_sync_enabled():
            return (
                reverse("operations:rider_reports")
                + f"?remote_sync_report={self.object.pk}&save_ok=submitted"
            )
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
                "me_reviewed_by",
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
        ctx["me_can_toggle_review"] = can_mark_me_review(user, report)

        week_start = report.week_start
        ctx["week_range_label"] = week_range_label(week_start)
        trips = list(report.trip_entries.all())
        total_distance = Decimal(round_distance_km(report.distance_travelled))
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
            "support_type": loc["pepfar_support_type"],
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
        ctx.update(_sync_enqueue_context(self.request, self.object))
        ctx["form_save_failed"] = self.request.method == "POST"
        return ctx

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["rider_user"] = self.request.user
        return kwargs

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        try:
            role = self.request.user.profile.role
        except UserProfile.DoesNotExist:
            role = None
        if role in (UserProfile.Role.PC, UserProfile.Role.ADMIN):
            return obj
        if not can_edit_report_as_rider(self.request.user, obj):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        return obj

    def dispatch(self, request, *args, **kwargs):
        profile = getattr(request.user, "profile", None)
        role = getattr(profile, "role", None)
        if role in (UserProfile.Role.PC, UserProfile.Role.ADMIN):
            return redirect("operations:pc_report_edit", pk=kwargs.get("pk"))
        return super().dispatch(request, *args, **kwargs)

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
        fuel_alloc, fuel_used = week_fuel_alloc_used_from_report(self.object)
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
                apply_week_fuel_distance_rollup(self.object, fuel_alloc, fuel_used)
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
            messages.success(
                self.request,
                "Report saved on this device. Cloud sync runs when you are online.",
            )
            if _jwt_remote_sync_enabled():
                url = reverse("operations:rider_reports")
                return redirect(
                    f"{url}?remote_sync_report={self.object.pk}&save_ok=submitted"
                )
            return redirect("operations:role_redirect")
        messages.success(
            self.request,
            "Report saved. Saved trips appear in the table below; add more if needed.",
        )
        edit_url = reverse("operations:report_edit", kwargs={"pk": self.object.pk})
        qs = "save_ok=1&draft_cleared=1"
        if _jwt_remote_sync_enabled():
            qs += "&remote_sync=1"
        return redirect(f"{edit_url}?{qs}")


class ReportSubmitView(LoginRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk, rider=request.user)
        if not can_edit_report_as_rider(request.user, report):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        report_service.submit_report(report, request.user)
        messages.success(request, "Report submitted for PC review.")
        url = reverse("operations:report_detail", kwargs={"pk": pk})
        return redirect(f"{url}?save_ok=review")


class ReportMeReviewView(LoginRequiredMixin, MERequiredMixin, View):
    """POST: mark or clear M&E review (locks PC editing when marked)."""

    def post(self, request, pk):
        report = get_object_or_404(RiderWeeklyReport, pk=pk)
        if not can_mark_me_review(request.user, report):
            from django.core.exceptions import PermissionDenied

            raise PermissionDenied
        action = (request.POST.get("action") or "").strip().lower()
        if action == "clear":
            report.me_reviewed_at = None
            report.me_reviewed_by = None
            report.save(update_fields=["me_reviewed_at", "me_reviewed_by", "updated_at"])
            messages.success(
                request,
                "M&E review cleared. PCs may edit this report again when its status allows.",
            )
        elif action == "mark":
            report.me_reviewed_at = timezone.now()
            report.me_reviewed_by = request.user
            report.save(update_fields=["me_reviewed_at", "me_reviewed_by", "updated_at"])
            messages.success(
                request,
                "Marked as reviewed by M&E. PC edits are locked for this report.",
            )
        else:
            messages.error(request, "Unknown action.")
        return redirect("operations:report_detail", pk=pk)


class RiderWeekFuelView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Rider/driver: week fuel totals per calendar week (not tied to report status)."""

    template_name = "operations/reports/rider_week_fuel.html"

    def test_func(self):
        return is_rider_like(self.request.user)

    def _week_start(self, request):
        raw = (request.POST.get("week") or request.GET.get("week") or "").strip()
        if not raw:
            return _monday_of_current_week()
        try:
            d = date.fromisoformat(raw[:10])
        except ValueError:
            return _monday_of_current_week()
        return d - timedelta(days=d.weekday())

    def _context(self, request, *, fuel_errors=None, pc_fuel_post_override=None):
        week_start = self._week_start(request)
        qs = (
            get_reports_queryset(request.user)
            .filter(week_start=week_start)
            .order_by("-updated_at", "-id")
        )
        reports = list(qs)
        target = reports[0] if reports else None
        if pc_fuel_post_override is not None:
            totals = week_fuel_totals_from_pc_post(pc_fuel_post_override)
        else:
            totals = rider_week_fuel_totals_for_user_week(request.user.id, week_start)
        return {
            "week_start": week_start,
            "week_range_label": week_range_label(week_start),
            "report_location": _report_location_for_user(request.user),
            "target_report": target,
            "reports_for_week": reports,
            "multiple_week_reports": len(reports) > 1,
            "pc_fuel_week_totals": totals,
            "can_edit_fuel": True,
            "fuel_errors": list(fuel_errors or []),
            "user_role": getattr(getattr(request.user, "profile", None), "role", None),
        }

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self._context(request))

    def post(self, request, *args, **kwargs):
        week_start = self._week_start(request)
        try:
            fuel_alloc, fuel_used = parse_week_fuel_pc_post(request.POST)
        except ValueError as exc:
            return render(
                request,
                self.template_name,
                self._context(
                    request,
                    fuel_errors=[str(exc)],
                    pc_fuel_post_override=request.POST,
                ),
            )
        if fuel_used > fuel_alloc:
            return render(
                request,
                self.template_name,
                self._context(
                    request,
                    fuel_errors=["Fuel used cannot exceed fuel allocated (week totals)."],
                    pc_fuel_post_override=request.POST,
                ),
            )
        upsert_rider_week_fuel_summary(
            request.user.id, week_start, fuel_alloc, fuel_used
        )
        messages.success(request, "Fuel saved for this week.")
        return redirect(f"{reverse('operations:rider_week_fuel')}?{urlencode({'week': week_start.isoformat()})}")


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


class ReportSyncPayloadView(LoginRequiredMixin, View):
    """GET /reports/<pk>/sync-payload/ — JSON envelope for remote JWT uplink."""

    def get(self, request, pk):
        report = get_object_or_404(get_reports_queryset(request.user), pk=pk)
        if not is_rider_like(request.user):
            return JsonResponse({"error": "forbidden"}, status=403)
        envelope = report_sync_envelope(report)
        if not envelope.get("idempotency_key"):
            return JsonResponse(
                {"error": "report has no client_uuid; save draft once locally first"},
                status=400,
            )
        return JsonResponse(envelope)


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
