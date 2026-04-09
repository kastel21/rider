"""
Embedded Android-only endpoints (loopback; protected by shared secret header).
"""

import os

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from operations.services.embedded_bootstrap_import import apply_embedded_bootstrap
from operations.services.embedded_user_import import apply_embedded_user_import

_EMBEDDED_HEADER = "HTTP_X_OPS_EMBEDDED_SECRET"


class EmbeddedImportBootstrapView(APIView):
    """
    POST /api/embedded/import-bootstrap/
    Body: { "bootstrap": {...}, "profile": {...} } from remote rider APIs.
    Header: X-Ops-Embedded-Secret — must match OPS_EMBEDDED_IMPORT_SECRET env (set by Chaquopy).
    """

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        expected = (os.environ.get("OPS_EMBEDDED_IMPORT_SECRET") or "").strip()
        if not expected:
            return Response(
                {"error": "embedded import not configured"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        got = (request.META.get(_EMBEDDED_HEADER) or "").strip()
        if got != expected:
            return Response({"error": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        if not isinstance(request.data, dict):
            return Response(
                {"error": "expected JSON object"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            stats = apply_embedded_bootstrap(request.data)
        except Exception as exc:  # noqa: BLE001
            return Response(
                {"ok": False, "error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"ok": True, "stats": stats}, status=status.HTTP_200_OK)


class EmbeddedImportUsersView(APIView):
    """
    POST /api/embedded/import-users/
    Body: { "users": [ ... ] } from GET /api/rider/mobile-user-export/
    Header: X-Ops-Embedded-Secret
    """

    authentication_classes: list = []
    permission_classes = [AllowAny]

    def post(self, request):
        expected = (os.environ.get("OPS_EMBEDDED_IMPORT_SECRET") or "").strip()
        if not expected:
            return Response(
                {"error": "embedded import not configured"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        got = (request.META.get(_EMBEDDED_HEADER) or "").strip()
        if got != expected:
            return Response({"error": "forbidden"}, status=status.HTTP_403_FORBIDDEN)

        if not isinstance(request.data, dict):
            return Response(
                {"error": "expected JSON object"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            stats = apply_embedded_user_import(request.data)
        except Exception as exc:  # noqa: BLE001
            return Response(
                {"ok": False, "error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"ok": True, "stats": stats}, status=status.HTTP_200_OK)
