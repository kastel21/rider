from pathlib import Path

from django.conf import settings
from django.http import FileResponse, Http404


def service_worker(request):
    path = Path(settings.BASE_DIR) / "static" / "js" / "service-worker.js"
    if not path.is_file():
        raise Http404()
    return FileResponse(path.open("rb"), content_type="application/javascript")
