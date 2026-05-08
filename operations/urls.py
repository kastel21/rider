from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView

from . import views
from .views.referred_samples_views import ReferredSamplesModuleView

app_name = "operations"

urlpatterns = [
    path("service-worker.js", views.service_worker, name="service_worker"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "accounts/password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url=reverse_lazy("operations:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "accounts/password/change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html",
        ),
        name="password_change_done",
    ),
    path("", views.RoleRedirectView.as_view(), name="role_redirect"),
    path("ajax/report-facilities/", views.ReportFacilitiesAjaxView.as_view(), name="report_facilities_ajax"),
    path("api/register-device/", views.RiderRegisterDeviceView.as_view(), name="rider_register_device"),
    path("api/sync/", views.RiderSyncView.as_view(), name="rider_session_sync"),
    path("reports/", views.RiderReportListView.as_view(), name="rider_reports"),
    path("reports/create/", views.RiderReportCreateView.as_view(), name="report_create"),
    path("reports/export/", views.ReportExportView.as_view(), name="report_export"),
    path("reports/<int:pk>/", views.RiderReportDetailView.as_view(), name="report_detail"),
    path("reports/<int:pk>/edit/", views.RiderReportEditView.as_view(), name="report_edit"),
    path("reports/<int:pk>/submit/", views.ReportSubmitView.as_view(), name="report_submit"),
    path("pc/reports/", views.RiderReportListView.as_view(), name="pc_reports"),
    path("pc/reports/<int:pk>/edit/", views.PCReportEditView.as_view(), name="pc_report_edit"),
    path(
        "pc/reports/<int:pk>/edit-history/",
        views.ReportEditHistoryView.as_view(),
        name="report_edit_history",
    ),
    path(
        "pc/reports/<int:pk>/review/start/",
        views.ReportStartReviewView.as_view(),
        name="report_start_review",
    ),
    path(
        "pc/reports/<int:pk>/review/complete/",
        views.ReportReviewView.as_view(),
        name="report_review",
    ),
    path(
        "pc/reports/rider/<int:rider_id>/week/<week_str>/review/start/",
        views.ReportStartReviewGroupView.as_view(),
        name="report_start_review_group",
    ),
    path(
        "pc/reports/rider/<int:rider_id>/week/<week_str>/review/complete/",
        views.ReportReviewGroupView.as_view(),
        name="report_review_group",
    ),
    path("pc/reports/audit-log/", views.ReportAuditLogListView.as_view(), name="report_audit_log_list"),
    path("me/reports/", views.RiderReportListView.as_view(), name="me_reports"),
    path(
        "me/reports/<int:pk>/me-review/",
        views.ReportMeReviewView.as_view(),
        name="report_me_review",
    ),
    path("me/metrics/", views.MEMetricsOverviewView.as_view(), name="me_metrics"),
    path("me/metrics/riders/", views.MEMetricsRidersView.as_view(), name="me_metrics_riders"),
    path("me/metrics/drivers/", views.MEMetricsDriversView.as_view(), name="me_metrics_drivers"),
    path(
        "me/metrics/referred-samples/",
        views.MEMetricsReferredSamplesView.as_view(),
        name="me_metrics_referred_samples",
    ),
    path(
        "me/metrics/accidents-incomplete/",
        views.MEAccidentsIncompleteView.as_view(),
        name="me_metrics_accidents_incomplete",
    ),
    path(
        "me/metrics/riders/export.csv/",
        views.METableExportView.as_view(table="riders", export_format="csv"),
        name="me_metrics_riders_export_csv",
    ),
    path(
        "me/metrics/riders/export.xlsx/",
        views.METableExportView.as_view(table="riders", export_format="xlsx"),
        name="me_metrics_riders_export_xlsx",
    ),
    path(
        "me/metrics/drivers/export.csv/",
        views.METableExportView.as_view(table="drivers", export_format="csv"),
        name="me_metrics_drivers_export_csv",
    ),
    path(
        "me/metrics/drivers/export.xlsx/",
        views.METableExportView.as_view(table="drivers", export_format="xlsx"),
        name="me_metrics_drivers_export_xlsx",
    ),
    path(
        "me/metrics/referred-samples/export.csv/",
        views.METableExportView.as_view(table="referred_samples", export_format="csv"),
        name="me_metrics_referred_samples_export_csv",
    ),
    path(
        "me/metrics/referred-samples/export.xlsx/",
        views.METableExportView.as_view(table="referred_samples", export_format="xlsx"),
        name="me_metrics_referred_samples_export_xlsx",
    ),
    path(
        "me/metrics/accidents-incomplete/export.csv/",
        views.METableExportView.as_view(table="accidents_incomplete", export_format="csv"),
        name="me_metrics_accidents_export_csv",
    ),
    path(
        "me/metrics/accidents-incomplete/export.xlsx/",
        views.METableExportView.as_view(table="accidents_incomplete", export_format="xlsx"),
        name="me_metrics_accidents_export_xlsx",
    ),
    path("pc/manage/", views.PCManageIndexView.as_view(), name="pc_manage"),
    path("pc/manage/bikes/", views.BikeListView.as_view(), name="pc_manage_bikes"),
    path("pc/manage/bikes/add/", views.BikeCreateView.as_view(), name="pc_manage_bike_add"),
    path("pc/manage/bikes/<int:pk>/edit/", views.BikeUpdateView.as_view(), name="pc_manage_bike_edit"),
    path("pc/manage/bikes/<int:pk>/delete/", views.BikeDeleteView.as_view(), name="pc_manage_bike_delete"),
    path("pc/manage/cars/", views.CarListView.as_view(), name="pc_manage_cars"),
    path("pc/manage/cars/add/", views.CarCreateView.as_view(), name="pc_manage_car_add"),
    path("pc/manage/cars/<int:pk>/edit/", views.CarUpdateView.as_view(), name="pc_manage_car_edit"),
    path("pc/manage/cars/<int:pk>/delete/", views.CarDeleteView.as_view(), name="pc_manage_car_delete"),
    path("pc/manage/facilities/", views.FacilityListView.as_view(), name="pc_manage_facilities"),
    path("pc/manage/facilities/add/", views.FacilityCreateView.as_view(), name="pc_manage_facility_add"),
    path("pc/manage/facilities/<int:pk>/edit/", views.FacilityUpdateView.as_view(), name="pc_manage_facility_edit"),
    path("pc/manage/facilities/<int:pk>/delete/", views.FacilityDeleteView.as_view(), name="pc_manage_facility_delete"),
    path("pc/manage/hubs/", views.HubListView.as_view(), name="pc_manage_hubs"),
    path("pc/manage/hubs/add/", views.HubCreateView.as_view(), name="pc_manage_hub_add"),
    path("pc/manage/hubs/<int:pk>/edit/", views.HubUpdateView.as_view(), name="pc_manage_hub_edit"),
    path("pc/manage/hubs/<int:pk>/delete/", views.HubDeleteView.as_view(), name="pc_manage_hub_delete"),
    path("pc/manage/riders/", views.RiderListView.as_view(), name="pc_manage_riders"),
    path("pc/manage/riders/add/", views.RiderCreateView.as_view(), name="pc_manage_rider_add"),
    path("pc/manage/riders/<int:pk>/edit/", views.RiderUpdateView.as_view(), name="pc_manage_rider_edit"),
    path("pc/manage/riders/<int:pk>/deactivate/", views.RiderDeactivateView.as_view(), name="pc_manage_rider_deactivate"),
    path("pc/manage/drivers/", views.DriverListView.as_view(), name="pc_manage_drivers"),
    path("pc/manage/drivers/add/", views.DriverCreateView.as_view(), name="pc_manage_driver_add"),
    path("pc/manage/drivers/<int:pk>/edit/", views.DriverUpdateView.as_view(), name="pc_manage_driver_edit"),
    path("pc/manage/drivers/<int:pk>/deactivate/", views.DriverDeactivateView.as_view(), name="pc_manage_driver_deactivate"),
    path("pc/bike-functionality/", views.NotRestoredView.as_view(), name="pc_bike_functionality"),
    path(
        "pc/bike-rider-management/",
        RedirectView.as_view(pattern_name="operations:pc_manage", permanent=False),
        name="pc_bike_rider_management",
    ),
    path(
        "pc/riders/",
        RedirectView.as_view(pattern_name="operations:pc_manage_riders", permanent=False),
        name="pc_riders",
    ),
    path("pc/driver-weekly/", views.NotRestoredView.as_view(), name="pc_driver_weekly_list"),
    path(
        "pc/referred-samples/",
        ReferredSamplesModuleView.as_view(),
        name="pc_referred_samples_list",
    ),
    path("pc/incidents/", views.NotRestoredView.as_view(), name="pc_incidents_list"),
    path(
        "pc/accidents-incomplete/",
        views.PCDistrictWeeklyTransportStatView.as_view(),
        name="pc_accidents_incomplete",
    ),
    path(
        "pc/accident-capture/",
        RedirectView.as_view(pattern_name="operations:pc_accidents_incomplete", permanent=False),
        name="pc_accident_capture",
    ),
    path(
        "pc/incomplete-trip-capture/",
        RedirectView.as_view(pattern_name="operations:pc_accidents_incomplete", permanent=False),
        name="pc_incomplete_trip_capture",
    ),
]
