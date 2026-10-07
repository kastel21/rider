"""Refuse sign-in and sync from Android builds older than the configured minimum."""

from django.http import JsonResponse

from operations.services.app_update import rejection_payload


class AppVersionGateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        payload = rejection_payload(request)
        if payload is not None:
            return JsonResponse(payload, status=426)
        return self.get_response(request)
