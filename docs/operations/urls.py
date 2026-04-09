"""Operations URL routes (web + session API + rider REST include)."""
from django.urls import include, path

from operations.views.auth_views import LoginView, LogoutView, RoleRedirectView
from operations.views.pc_report_views import PCReportEditView
from operations.views.report_export_views import ReportExportView
from operations.views.report_views import (
    ReportAuditLogListView,
    ReportEditHistoryView,
    ReportFacilitiesAjaxView,
    ReportReviewGroupView,
    ReportReviewView,
    ReportStartReviewGroupView,
    ReportStartReviewView,
    ReportSubmitView,
    RiderRegisterDeviceView,
    RiderReportCreateView,
    RiderReportDetailView,
    RiderReportEditView,
    RiderReportListView,
    RiderSyncView,
)
from operations.views.pc_module_views import (
    IncompleteTripCaptureModuleView,
    PCBikeFunctionalityUpdateView,
    PCBikeFunctionalityView,
    PCBikeRiderManagementView,
    PCRidersListView,
    ProvincialDriverWeeklyModuleView,
    ReferredSamplesModuleView,
    RiderAccidentCaptureModuleView,
    TransportIncidentsModuleView,
)

app_name = 'operations'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', RoleRedirectView.as_view(), name='role_redirect'),
    path('api/rider/', include('operations.api.urls')),
    path('ajax/report-facilities/', ReportFacilitiesAjaxView.as_view(), name='report_facilities_ajax'),
    path('api/register-device/', RiderRegisterDeviceView.as_view(), name='rider_register_device'),
    path('api/sync/', RiderSyncView.as_view(), name='rider_session_sync'),
    path('reports/', RiderReportListView.as_view(), name='rider_reports'),
    path('reports/create/', RiderReportCreateView.as_view(), name='report_create'),
    path('reports/export/', ReportExportView.as_view(), name='report_export'),
    path('reports/<int:pk>/', RiderReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:pk>/edit/', RiderReportEditView.as_view(), name='report_edit'),
    path('reports/<int:pk>/submit/', ReportSubmitView.as_view(), name='report_submit'),
    path('pc/reports/', RiderReportListView.as_view(), name='pc_reports'),
    path('pc/reports/<int:pk>/edit/', PCReportEditView.as_view(), name='pc_report_edit'),
    path('pc/reports/<int:pk>/edit-history/', ReportEditHistoryView.as_view(), name='report_edit_history'),
    path('pc/reports/<int:pk>/review/start/', ReportStartReviewView.as_view(), name='report_start_review'),
    path('pc/reports/<int:pk>/review/complete/', ReportReviewView.as_view(), name='report_review'),
    path(
        'pc/reports/rider/<int:rider_id>/week/<str:week_str>/review/start/',
        ReportStartReviewGroupView.as_view(),
        name='report_start_review_group',
    ),
    path(
        'pc/reports/rider/<int:rider_id>/week/<str:week_str>/review/complete/',
        ReportReviewGroupView.as_view(),
        name='report_review_group',
    ),
    path('pc/reports/audit-log/', ReportAuditLogListView.as_view(), name='report_audit_log_list'),
    path('me/reports/', RiderReportListView.as_view(), name='me_reports'),
    path('pc/bike-functionality/', PCBikeFunctionalityView.as_view(), name='pc_bike_functionality'),
    path('pc/bikes/<int:pk>/edit/', PCBikeFunctionalityUpdateView.as_view(), name='pc_bike_edit'),
    path('pc/bike-rider-management/', PCBikeRiderManagementView.as_view(), name='pc_bike_rider_management'),
    path('pc/riders/', PCRidersListView.as_view(), name='pc_riders'),
    path('pc/driver-weekly/', ProvincialDriverWeeklyModuleView.as_view(), name='pc_driver_weekly_list'),
    path('pc/referred-samples/', ReferredSamplesModuleView.as_view(), name='pc_referred_samples_list'),
    path('pc/incidents/', TransportIncidentsModuleView.as_view(), name='pc_incidents_list'),
    path('pc/accident-capture/', RiderAccidentCaptureModuleView.as_view(), name='pc_accident_capture'),
    path('pc/incomplete-trip-capture/', IncompleteTripCaptureModuleView.as_view(), name='pc_incomplete_trip_capture'),
]

