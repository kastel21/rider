"""Report export (CSV/XLSX) — minimal stub until full export is restored."""
from django.http import HttpResponse
from django.views import View

from operations.permissions import OperationsLoginRequiredMixin


class ReportExportView(OperationsLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            'Report export is not fully restored. Use database or backup export.',
            content_type='text/plain',
            status=501,
        )
