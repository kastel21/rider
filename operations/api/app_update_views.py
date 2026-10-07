"""Public update check, APK download, and a browser page for the first install."""

from django.http import FileResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.services.app_update import (
    download_path_for,
    latest_releases,
    offerable_release,
    release_label,
    request_application_id,
    request_version_code,
    status_payload,
    valid_application_id,
)


class RiderAppUpdateView(APIView):
    """GET /api/rider/app-update/?version_code=&application_id="""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        version_code = request_version_code(request)
        application_id = request_application_id(request)
        return Response(status_payload(version_code, application_id))


class RiderAppDownloadView(APIView):
    """GET /api/rider/app-download/?application_id="""

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        raw_id = (request.GET.get("application_id") or "").strip()
        if not valid_application_id(raw_id):
            return HttpResponseBadRequest("application_id is required")
        release = offerable_release(raw_id)
        if release is None or not release.apk:
            return HttpResponseNotFound("No update file is available for this app.")
        filename = f"rider-update-{release.version_code}.apk"
        response = FileResponse(
            release.apk.open("rb"),
            content_type="application/vnd.android.package-archive",
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Content-Encoding"] = "identity"
        return response


class AppUpdatePageView(TemplateView):
    """GET /app/update/ — open in the phone browser when the installed app cannot update itself."""

    template_name = "operations/app_update.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        rows = []
        for release in latest_releases():
            if offerable_release(release.application_id) is None:
                continue
            rows.append(
                {
                    "label": release_label(release.application_id),
                    "application_id": release.application_id,
                    "version_name": release.version_name or str(release.version_code),
                    "version_code": release.version_code,
                    "download_path": download_path_for(release.application_id),
                }
            )
        ctx["releases"] = rows
        return ctx
