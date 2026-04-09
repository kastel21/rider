# Web app route matrix (Django session UI)

For a **full reproduction checklist** (settings, models, templates, static, verification), see **`WEBAPP_REPRODUCTION_CHECKLIST.md`**.

Session-authenticated **browser** routes only: HTML pages, form POSTs, redirects, and same-origin endpoints the web UI calls (AJAX, offline PWA sync with session cookie). **Not included:** JWT REST API under `/api/rider/` (native/mobile clients).

Mount: `config.urls` → `path('', include('operations.urls'))` — **no URL prefix**.

**Reverse:** all names use the `operations` namespace, e.g. `reverse('operations:login')` → `/login/`.

---

## Site root

| Path | Name | Methods | View | Template / response |
|------|------|---------|------|---------------------|
| `/admin/` | *(Django admin)* | GET, POST, … | Admin site | Admin templates |
| Everything below | — | — | `operations.urls` | — |

---

## `operations` routes

| Path | Name | Methods | View class | Template / notes |
|------|------|---------|------------|------------------|
| `/login/` | `login` | GET, POST | `LoginView` | `operations/auth/login.html` |
| `/logout/` | `logout` | GET | `LogoutView` | Redirect to login |
| `/` | `role_redirect` | GET | `RoleRedirectView` | Redirect by role to a reports list |
| `/ajax/report-facilities/` | `report_facilities_ajax` | GET | `ReportFacilitiesAjaxView` | JSON (facilities / hubs / labs) |
| `/api/register-device/` | `rider_register_device` | POST | `RiderRegisterDeviceView` | JSON (session auth; PWA device registration) |
| `/api/sync/` | `rider_session_sync` | POST | `RiderSyncView` | JSON (session auth; PWA batch sync) |
| `/reports/` | `rider_reports` | GET | `RiderReportListView` | `operations/reports/report_list.html` or `rider_report_list.html` for rider/driver |
| `/reports/create/` | `report_create` | GET, POST | `RiderReportCreateView` | `operations/reports/report_form.html` |
| `/reports/export/` | `report_export` | GET | `ReportExportView` | Stub plain text (501) until export is implemented |
| `/reports/<pk>/` | `report_detail` | GET | `RiderReportDetailView` | `operations/reports/report_detail.html` |
| `/reports/<pk>/edit/` | `report_edit` | GET, POST | `RiderReportEditView` | `operations/reports/report_form.html` |
| `/reports/<pk>/submit/` | `report_submit` | POST | `ReportSubmitView` | Redirect |
| `/pc/reports/` | `pc_reports` | GET | `RiderReportListView` | Same list templates as above |
| `/pc/reports/<pk>/edit/` | `pc_report_edit` | GET, POST | `PCReportEditView` | `operations/reports/report_form.html` |
| `/pc/reports/<pk>/edit-history/` | `report_edit_history` | GET | `ReportEditHistoryView` | `operations/reports/report_edit_history.html` |
| `/pc/reports/<pk>/review/start/` | `report_start_review` | POST | `ReportStartReviewView` | Redirect |
| `/pc/reports/<pk>/review/complete/` | `report_review` | POST | `ReportReviewView` | Redirect |
| `/pc/reports/rider/<rider_id>/week/<week_str>/review/start/` | `report_start_review_group` | POST | `ReportStartReviewGroupView` | Redirect (`week_str` e.g. `2025-04-06`) |
| `/pc/reports/rider/<rider_id>/week/<week_str>/review/complete/` | `report_review_group` | POST | `ReportReviewGroupView` | Redirect |
| `/pc/reports/audit-log/` | `report_audit_log_list` | GET | `ReportAuditLogListView` | `operations/reports/report_audit_log_list.html` |
| `/me/reports/` | `me_reports` | GET | `RiderReportListView` | Same list templates |
| `/pc/bike-functionality/` | `pc_bike_functionality` | GET | `NotRestoredView` | Stub HTML (restore from backup) |
| `/pc/bike-rider-management/` | `pc_bike_rider_management` | GET | `NotRestoredView` | Stub |
| `/pc/riders/` | `pc_riders` | GET | `NotRestoredView` | Stub |
| `/pc/driver-weekly/` | `pc_driver_weekly_list` | GET | `NotRestoredView` | Stub |
| `/pc/referred-samples/` | `pc_referred_samples_list` | GET | `NotRestoredView` | Stub |
| `/pc/incidents/` | `pc_incidents_list` | GET | `NotRestoredView` | Stub |
| `/pc/accident-capture/` | `pc_accident_capture` | GET | `NotRestoredView` | Stub |
| `/pc/incomplete-trip-capture/` | `pc_incomplete_trip_capture` | GET | `NotRestoredView` | Stub |

---

## Templates used by the web app

| Template path | Used by |
|---------------|---------|
| `operations/auth/login.html` | Login |
| `operations/reports/report_list.html` | PC / ME list |
| `operations/reports/rider_report_list.html` | Rider / driver list |
| `operations/reports/report_form.html` | Create, rider edit, PC edit |
| `operations/reports/report_detail.html` | Report detail |
| `operations/reports/report_edit_history.html` | PC edit history |
| `operations/reports/report_audit_log_list.html` | PC audit log list |

Global templates directory: `templates/` (project-level). Context: `operations_nav` adds `user_role` for nav.

---

## Auth-related settings

| Setting | Value |
|---------|--------|
| `LOGIN_URL` | `operations:login` |
| `LOGIN_REDIRECT_URL` | `operations:role_redirect` |
| `LOGOUT_REDIRECT_URL` | `operations:login` |

---

## Source files

- URLconf: `operations/urls.py`
- Views: `operations/views/auth_views.py`, `report_views.py`, `pc_report_views.py`, `report_export_views.py`, `stub_views.py`

---

*Excludes `/api/rider/…` JWT API (`operations/api/urls.py`).*
