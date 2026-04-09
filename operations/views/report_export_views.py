from django.http import HttpResponse
from django.views import View


class ReportExportView(View):
    def get(self, request):
        return HttpResponse("Report export not implemented.", status=501, content_type="text/plain")
