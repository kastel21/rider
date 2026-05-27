"""Forward /api/rider-remote/* to OPS_REMOTE_API_BASE (embedded APK only; avoids WebView CORS)."""
import logging
import urllib.error
import urllib.request

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

_ALLOWED_PREFIXES = (
    "health/",
    "login/",
    "refresh/",
    "register-device/",
    "apply-sync/",
    "profile/",
    "bootstrap/",
)


@method_decorator(csrf_exempt, name="dispatch")
class RiderRemoteProxyView(View):
    def dispatch(self, request, subpath=""):
        if not getattr(settings, "OPS_RIDER_REMOTE_PROXY", False):
            return JsonResponse({"error": "proxy disabled"}, status=404)

        base = (getattr(settings, "OPS_REMOTE_API_BASE", "") or "").strip().rstrip("/")
        if not base:
            return JsonResponse({"error": "OPS_REMOTE_API_BASE not set"}, status=503)

        subpath = (subpath or "").lstrip("/")
        if not subpath or not any(subpath.startswith(p) for p in _ALLOWED_PREFIXES):
            return JsonResponse({"error": "path not allowed"}, status=403)

        url = f"{base}/api/rider/{subpath}"
        query = request.META.get("QUERY_STRING", "")
        if query:
            url = f"{url}?{query}"

        headers = {"Accept": "application/json"}
        auth = request.META.get("HTTP_AUTHORIZATION")
        if auth:
            headers["Authorization"] = auth
        content_type = request.META.get("CONTENT_TYPE")
        if content_type:
            headers["Content-Type"] = content_type

        body = request.body if request.method not in ("GET", "HEAD") else None
        upstream = urllib.request.Request(url, data=body, headers=headers, method=request.method)
        try:
            with urllib.request.urlopen(upstream, timeout=30) as resp:
                payload = resp.read()
                status = resp.status
                resp_ct = resp.headers.get("Content-Type", "application/json")
        except urllib.error.HTTPError as e:
            payload = e.read()
            status = e.code
            resp_ct = e.headers.get("Content-Type", "application/json")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            logger.warning("rider remote proxy %s: %s", subpath, e)
            return JsonResponse(
                {"error": "offline or unreachable", "detail": str(e)},
                status=503,
            )

        return HttpResponse(payload, status=status, content_type=resp_ct)
