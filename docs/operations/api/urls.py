from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .rider_views import (
    RiderLoginView,
    RiderProfileView,
    RiderBootstrapView,
    RiderConfigView,
    RiderRegisterDeviceView,
    RiderSubmitReportView,
    RiderSyncView,
)

app_name = 'rider_api'

urlpatterns = [
    path('login/', RiderLoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', RiderProfileView.as_view(), name='profile'),
    path('register-device/', RiderRegisterDeviceView.as_view(), name='register-device'),
    path('config/', RiderConfigView.as_view(), name='config'),
    path('bootstrap/', RiderBootstrapView.as_view(), name='bootstrap'),
    path('submit-report/', RiderSubmitReportView.as_view(), name='submit-report'),
    path('sync/', RiderSyncView.as_view(), name='sync'),
]
