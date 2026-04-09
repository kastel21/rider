"""Placeholder routes not yet restored from backup."""
from django.http import HttpResponse
from django.views import View


class NotRestoredView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            '<p>This page is not restored from disk corruption.</p>',
            content_type='text/html',
        )
