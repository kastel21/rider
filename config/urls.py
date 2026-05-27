from django.contrib import admin
from django.urls import include, path

from operations.api.embedded_views import EmbeddedImportBootstrapView, EmbeddedImportUsersView
from operations.api.remote_proxy_views import RiderRemoteProxyView
from operations.views.auth_views import RiderJwtBootstrapView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/rider/", include("operations.api.urls")),
    path("api/rider/jwt-bootstrap/", RiderJwtBootstrapView.as_view(), name="rider_jwt_bootstrap"),
    path(
        "api/rider-remote/<path:subpath>",
        RiderRemoteProxyView.as_view(),
        name="rider_remote_proxy",
    ),
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
