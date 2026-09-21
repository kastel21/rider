"""Weekly rider submissions and PC-review coverage by province (PC / M&E)."""

from __future__ import annotations

import csv
from datetime import timedelta
from io import StringIO
from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.views.generic import TemplateView, View

from ..permissions import ProgramReportingMixin
from ..selectors import get_provinces_queryset, week_start_from_request
from ..services.me_table_export import filename_safe, week_download_stem
from ..services.rider_week_submission_report import (
    build_rider_week_submission_report,
    parse_province_id_from_request,
    pc_review_csv_rows,
    province_summary_csv_rows,
    rider_detail_csv_rows,
)


def _csv_query(*, week_iso: str, province_id: int | None) -> str:
    params: dict[str, str] = {"week": week_iso}
    if province_id:
        params["province"] = str(province_id)
    return urlencode(params)


def _csv_hrefs(*, week_iso: str, province_id: int | None) -> dict[str, str]:
    q = _csv_query(week_iso=week_iso, province_id=province_id)
    return {
        "summary_csv_href": f"{reverse('operations:rider_week_submissions_summary_csv')}?{q}",
        "riders_csv_href": f"{reverse('operations:rider_week_submissions_riders_csv')}?{q}",
        "pc_reviews_csv_href": f"{reverse('operations:rider_week_submissions_pc_reviews_csv')}?{q}",
    }


def _report_for_request(request):
    week_start = week_start_from_request(request)
    province_id = parse_province_id_from_request(request, request.user)
    data = build_rider_week_submission_report(
        user=request.user,
        week_start=week_start,
        province_id=province_id,
    )
    return week_start, province_id, data


def _csv_response(*, headers: list[str], rows: list[list[str]], download_stem: str) -> HttpResponse:
    buf = StringIO()
    writer = csv.writer(buf, lineterminator="\r\n")
    writer.writerow(headers)
    writer.writerows(rows)
    resp = HttpResponse(buf.getvalue().encode("utf-8-sig"), content_type="text/csv; charset=utf-8")
    resp["Content-Disposition"] = f'attachment; filename="{filename_safe(download_stem)}.csv"'
    return resp


class RiderWeekSubmissionsView(LoginRequiredMixin, ProgramReportingMixin, TemplateView):
    template_name = "operations/reports/rider_week_submissions.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        week_start, province_id, data = _report_for_request(self.request)
        week_iso = week_start.isoformat()
        ctx["report"] = data
        ctx["selected_week_start"] = week_start
        ctx["selected_province_id"] = province_id
        ctx["provinces"] = get_provinces_queryset(self.request.user).order_by("name")
        ctx["week_range_label"] = data["week_range_label"]
        nav_params: dict[str, str] = {}
        if province_id:
            nav_params["province"] = str(province_id)
        prev = {"week": (week_start - timedelta(days=7)).isoformat(), **nav_params}
        nxt = {"week": (week_start + timedelta(days=7)).isoformat(), **nav_params}
        ctx["prev_week_href"] = f"?{urlencode(prev)}"
        ctx["next_week_href"] = f"?{urlencode(nxt)}"
        ctx.update(_csv_hrefs(week_iso=week_iso, province_id=province_id))
        return ctx


class RiderWeekSubmissionsCsvView(LoginRequiredMixin, ProgramReportingMixin, View):
    table: str = ""

    def get(self, request, *args, **kwargs):
        table_key = (self.table or "").lower()
        week_start, province_id, data = _report_for_request(request)
        if table_key == "summary":
            headers, rows = province_summary_csv_rows(data)
            prefix = "rider-week-submissions-summary"
        elif table_key == "riders":
            headers, rows = rider_detail_csv_rows(data)
            prefix = "rider-week-submissions-riders"
        elif table_key == "pc_reviews":
            headers, rows = pc_review_csv_rows(data)
            prefix = "rider-week-pc-reviews"
        else:
            return HttpResponseBadRequest("Unknown export.")
        stem = week_download_stem(week_start=week_start, prefix=prefix)
        if province_id:
            stem = f"{stem}-province-{province_id}"
        return _csv_response(headers=headers, rows=rows, download_stem=stem)
