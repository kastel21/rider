"""Prevent WebView / service worker from caching dynamic HTML (rider home, reports)."""


class NoCacheDynamicHtmlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.method != "GET":
            return response
        content_type = response.get("Content-Type", "")
        if "text/html" not in content_type:
            return response
        if request.path.startswith("/static/"):
            return response
        response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response["Pragma"] = "no-cache"
        return response
