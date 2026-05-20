from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .mobile_export_views import MobileUserExportView
from .sync_bundle_views import RiderSyncBundleView
from .rider_views import (
    RiderApplySyncView,
    RiderBootstrapView,
    RiderConfigView,
    RiderHealthView,
    RiderLocalSessionView,
    RiderLoginView,
    RiderProfileView,
    RiderRegisterDeviceView,
    RiderSyncView,
)

app_name = "rider_api"

urlpatterns = [
    path("health/", RiderHealthView.as_view(), name="health"),
    path("login/", RiderLoginView.as_view(), name="login"),
    path("local-session/", RiderLocalSessionView.as_view(), name="local-session"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", RiderProfileView.as_view(), name="profile"),
    path("register-device/", RiderRegisterDeviceView.as_view(), name="register-device"),
    path("config/", RiderConfigView.as_view(), name="config"),
    path("bootstrap/", RiderBootstrapView.as_view(), name="bootstrap"),
    path("mobile-user-export/", MobileUserExportView.as_view(), name="mobile-user-export"),
    path("sync-bundle/", RiderSyncBundleView.as_view(), name="sync-bundle"),
    path("apply-sync/", RiderApplySyncView.as_view(), name="apply-sync"),
    path("sync/", RiderSyncView.as_view(), name="sync"),
]
