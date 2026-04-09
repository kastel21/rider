from django.contrib import admin
from django.urls import include, path

from operations.api.embedded_views import EmbeddedImportBootstrapView, EmbeddedImportUsersView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rider/", include("operations.api.urls")),
    path(
        "api/embedded/import-bootstrap/",
        EmbeddedImportBootstrapView.as_view(),
        name="embedded_import_bootstrap",
    ),
    path(
        "api/embedded/import-users/",
        EmbeddedImportUsersView.as_view(),
        name="embedded_import_users",
    ),
    path("", include("operations.urls")),
]
