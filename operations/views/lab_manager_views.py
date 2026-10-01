from datetime import date, timedelta
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from ..models import RiderWeeklyReport, UserProfile
from ..permissions import LabManagerRequiredMixin
from ..selectors import (
    lab_manager_district_id,
    monday_of_week_containing,
    reports_in_lab_manager_scope,
    week_range_label,
    week_start_from_request,
)
from ..services import report_service
from ..services.trip_analysis import specimens_from_entries


class LabManagerQueueView(LoginRequiredMixin, LabManagerRequiredMixin, View):
    """One list for the district: approve into the PC queue, or send back with a reason."""

    template_name = "operations/reports/lab_manager_queue.html"

    def get(self, request):
        return self._render(request)

    def post(self, request):
        week_start = self._week_start(request)
        action = (request.POST.get("action") or "").strip().lower()
        pending = self._pending(request, week_start)
        if action == "approve_all":
            released = 0
            for report in pending:
                if report_service.release_report_to_pc(report, request.user):
                    released += 1
            if released:
                messages.success(
                    request,
                    f"Approved {released} report(s). They are now with the PC.",
                )
            else:
                messages.info(request, "Nothing was waiting for approval.")
        elif action in ("approve", "send_back"):
            rider_id = request.POST.get("rider_id")
            try:
                rider_id = int(rider_id)
            except (TypeError, ValueError):
                rider_id = None
            rows = [r for r in pending if r.rider_id == rider_id] if rider_id else []
            if not rows:
                messages.error(request, "That report is no longer waiting.")
            elif action == "approve":
                released = 0
                for report in rows:
                    if report_service.release_report_to_pc(report, request.user):
                        released += 1
                if released:
                    messages.success(request, "Approved. The PC can review it now.")
            else:
                reason = request.POST.get("lab_notes") or ""
                if not reason.strip():
                    messages.error(
                        request,
                        "Enter a reason so the rider knows what to fix before they resend.",
                    )
                else:
                    sent = 0
                    for report in rows:
                        if report_service.send_report_back_to_rider(
                            report, request.user, reason
                        ):
                            sent += 1
                    if sent:
                        messages.success(
                            request,
                            "Sent back. The rider can edit it and resend.",
                        )
        url = reverse("operations:lab_manager_queue")
        return redirect(f"{url}?{urlencode({'week': week_start.isoformat()})}")

    def _week_start(self, request):
        raw = ""
        if request.method == "POST":
            raw = (request.POST.get("week") or "").strip()
        if raw:
            try:
                return monday_of_week_containing(date.fromisoformat(raw[:10]))
            except ValueError:
                pass
        return week_start_from_request(request)

    def _pending(self, request, week_start):
        return list(
            reports_in_lab_manager_scope(request.user)
            .filter(
                week_start=week_start,
                status=RiderWeeklyReport.Status.SUBMITTED,
                lab_cleared_at__isnull=True,
            )
            .select_related(
                "rider",
                "rider__profile",
                "rider__rider_profile",
            )
            .prefetch_related("trip_entries")
            .annotate(week_trip_count=Count("trip_entries"))
            .order_by("rider__first_name", "rider__last_name", "rider__username", "pk")
        )

    def _render(self, request):
        week_start = week_start_from_request(request)
        district_id = lab_manager_district_id(request.user)
        district_name = ""
        if district_id:
            profile = getattr(request.user, "lab_manager_profile", None)
            if profile and profile.district_id:
                district_name = profile.district.name
        rows = []
        grouped: dict[int, list] = {}
        for report in self._pending(request, week_start):
            grouped.setdefault(report.rider_id, []).append(report)
        for reports in grouped.values():
            latest = max(reports, key=lambda r: (r.updated_at, r.pk))
            role = getattr(getattr(latest.rider, "profile", None), "role", None)
            rows.append(
                {
                    "report": latest,
                    "rider_name": latest.rider.get_full_name() or latest.rider.username,
                    "is_driver": role == UserProfile.Role.DRIVER,
                    "samples_total": sum(
                        specimens_from_entries(r.trip_entries.all()) for r in reports
                    ),
                    "trip_total": sum((r.week_trip_count or 0) for r in reports),
                    "submitted_at": max(
                        (r.submitted_at for r in reports if r.submitted_at),
                        default=None,
                    ),
                }
            )
        return render(
            request,
            self.template_name,
            {
                "district_name": district_name,
                "has_district": bool(district_id),
                "queue_rows": rows,
                "selected_week_start": week_start,
                "week_range_label": week_range_label(week_start),
                "prev_week": (week_start - timedelta(days=7)).isoformat(),
                "next_week": (week_start + timedelta(days=7)).isoformat(),
            },
        )
