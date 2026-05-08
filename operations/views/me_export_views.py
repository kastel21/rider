from __future__ import annotations

from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.views import View

from ..permissions import MERequiredMixin
from ..services.me_accidents_data import load_me_accidents_incomplete_data, me_accidents_week_start_from_request
from ..services.me_metrics_service import parse_weeks_param
from ..services.me_referred_samples_table import build_me_referred_samples_table
from ..services.me_report_service import build_driver_me_report_table, build_me_report_table
from ..services.me_table_export import (
    matrix_download_stem,
    response_accidents_xlsx,
    response_accidents_zip_csv,
    response_matrix_csv,
    response_matrix_xlsx,
)


class METableExportView(LoginRequiredMixin, MERequiredMixin, View):
    """Download M&E rider / driver / referred matrix or accidents bundle (CSV / Excel)."""

    table: str = ""
    export_format: str = ""

    def get(self, request, *args, **kwargs):
        fmt = (self.export_format or "").lower()
        if fmt not in ("csv", "xlsx"):
            return HttpResponseBadRequest("Unsupported format.")
        table_key = self.table or ""
        if table_key == "riders":
            weeks = parse_weeks_param(request.GET.get("weeks"))
            data = build_me_report_table(weeks=weeks)
            stem = matrix_download_stem(data, prefix="me-rider-weekly")
            if fmt == "csv":
                return response_matrix_csv(table=data, download_stem=stem)
            return response_matrix_xlsx(table=data, download_stem=stem, sheet_title="Rider weekly")
        if table_key == "drivers":
            weeks = parse_weeks_param(request.GET.get("weeks"))
            data = build_driver_me_report_table(weeks=weeks)
            stem = matrix_download_stem(data, prefix="me-driver-weekly")
            if fmt == "csv":
                return response_matrix_csv(table=data, download_stem=stem)
            return response_matrix_xlsx(table=data, download_stem=stem, sheet_title="Driver weekly")
        if table_key == "referred_samples":
            weeks = parse_weeks_param(request.GET.get("weeks"))
            data = build_me_referred_samples_table(weeks=weeks)
            stem = matrix_download_stem(data, prefix="me-referred-samples")
            if fmt == "csv":
                return response_matrix_csv(table=data, download_stem=stem)
            return response_matrix_xlsx(table=data, download_stem=stem, sheet_title="Referred samples")
        if table_key == "accidents_incomplete":
            week_start = me_accidents_week_start_from_request(request)
            bundle = load_me_accidents_incomplete_data(week_start=week_start)
            if fmt == "csv":
                return response_accidents_zip_csv(week_start=week_start, bundle=bundle)
            return response_accidents_xlsx(week_start=week_start, bundle=bundle)
        return HttpResponseBadRequest("Unknown export.")


def me_matrix_export_hrefs(*, name_csv: str, name_xlsx: str, weeks: int) -> dict[str, str]:
    q = urlencode({"weeks": weeks})
    return {
        "export_csv_href": f"{reverse(name_csv)}?{q}",
        "export_xlsx_href": f"{reverse(name_xlsx)}?{q}",
    }


def me_accidents_export_hrefs(*, week_iso: str) -> dict[str, str]:
    q = urlencode({"week": week_iso})
    return {
        "export_csv_href": f"{reverse('operations:me_metrics_accidents_export_csv')}?{q}",
        "export_xlsx_href": f"{reverse('operations:me_metrics_accidents_export_xlsx')}?{q}",
    }
