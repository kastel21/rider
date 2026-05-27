"""CORS for /api/rider/* so the embedded APK WebView can call a remote API from 127.0.0.1:8765."""
import os

from django.http import HttpResponse


def _allowed_origins():
    raw = os.environ.get(
        "OPS_CORS_ALLOWED_ORIGINS",
        "http://127.0.0.1:8765,http://localhost:8765",
    )
    return {o.strip() for o in raw.split(",") if o.strip()}


class RiderApiCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/rider/"):
            return self.get_response(request)

        origin = request.META.get("HTTP_ORIGIN", "")
        allowed = _allowed_origins()

        if request.method == "OPTIONS":
            resp = HttpResponse(status=204)
            if origin and origin in allowed:
                _apply_cors(resp, origin)
            return resp

        response = self.get_response(request)
        if origin and origin in allowed:
            _apply_cors(response, origin)
        return response


def _apply_cors(response, origin):
    response["Access-Control-Allow-Origin"] = origin
    response["Access-Control-Allow-Credentials"] = "true"
    response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
    response["Vary"] = "Origin"
