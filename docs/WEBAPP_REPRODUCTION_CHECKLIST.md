# Web app reproduction checklist

Use this with **`docs/URL_AND_ROUTE_MATRIX.md`** (routes + template names per URL). Together they describe what to copy or rebuild for a working **session-based browser UI**.

**Reality check:** Many report templates are **referenced in code** but may be **missing or corrupted on disk** in a damaged tree—restore them from backup or rebuild to match the names in the route doc.

---

## 1. Project skeleton

| Item | Location / notes |
|------|------------------|
| Django project package | `config/` — `settings.py`, `urls.py`, `wsgi.py` |
| Main app | `operations/` |
| Entry point | `manage.py`, `requirements.txt` |
| Root URL | `config/urls.py` → `admin/`, `include('operations.urls')` at `''` |

---

## 2. Dependencies (Python)

Install from `requirements.txt` at minimum: **Django**, **DRF + SimpleJWT** (settings import them even for web-only runs), **psycopg2** / **mssql-django + pyodbc** if not using SQLite, **openpyxl**, **reportlab**, **django-tailwind**, **django-browser-reload** (if you use Tailwind tooling).

---

## 3. Settings (`config/settings.py`)

| Area | What to match |
|------|----------------|
| `INSTALLED_APPS` | `admin`, `auth`, `sessions`, `messages`, `staticfiles`, `rest_framework`, `rest_framework_simplejwt`, `operations` |
| `ROOT_URLCONF` | `config.urls` |
| `TEMPLATES` | `DIRS`: `[BASE_DIR / 'templates']`, `APP_DIRS: True`, context processors including **`operations.context_processors.operations_nav`** |
| `DATABASES` | Same env-driven logic (MSSQL → Postgres → SQLite); `ATOMIC_REQUESTS` |
| `MIDDLEWARE` | As in repo (Security, GZip, Session, Common, Csrf, Auth, Messages, XFrame) |
| `STATIC_URL` / `STATICFILES_DIRS` / `STATIC_ROOT` | `/static/`, project `static/`, `staticfiles` |
| Auth redirects | `LOGIN_URL = 'operations:login'`, `LOGIN_REDIRECT_URL = 'operations:role_redirect'`, `LOGOUT_REDIRECT_URL = 'operations:login'` |
| `DEFAULT_AUTO_FIELD` | `BigAutoField` |
| `TIME_ZONE` / `USE_TZ` | e.g. `UTC`, `True` |

REST/JWT blocks can stay if you keep one settings file; they do not affect pure server-rendered pages beyond `INSTALLED_APPS`.

---

## 4. Data layer

| Item | Location |
|------|----------|
| Models | `operations/models.py` — geography, bikes, profiles, `RiderWeeklyReport`, rejections, audit, PC modules, etc. |
| Migrations | `operations/migrations/` — apply full history; this repo may have a **partial** set (verify with `showmigrations` vs model state) |
| Admin | `operations/admin.py` — user + inline `UserProfile`, registered models |

After migrate: create **superuser**, then **User** + **UserProfile** (role), **PCProfile** + provinces, **RiderProfile** + district/facility/bike as needed for tests.

---

## 5. URL routing (web only)

| Item | Location |
|------|----------|
| App routes | `operations/urls.py` — names and paths must match **`URL_AND_ROUTE_MATRIX.md`** |
| Do not skip | Stub routes (`NotRestoredView`) if you need `reverse()` to work everywhere; replace with real views when you restore features |

---

## 6. Behavior layer (Python, not URLs)

| Concern | Files |
|---------|--------|
| Login / logout / role redirect | `operations/views/auth_views.py` |
| Report CRUD, PC review, AJAX facilities, session sync JSON | `operations/views/report_views.py` |
| PC full-form edit | `operations/views/pc_report_views.py` |
| Export stub | `operations/views/report_export_views.py` |
| Placeholder PC pages | `operations/views/stub_views.py` |
| Permissions mixins + `can_edit_report` | `operations/permissions.py` |
| Role-scoped querysets | `operations/selectors.py` |
| Forms + sample rejection formset | `operations/forms.py` |
| Report state + audit helpers | `operations/services/report_service.py`, `report_edit_service.py` |
| Package exports (optional) | `operations/views/__init__.py` |

---

## 7. Templates

**Search paths:** `templates/` (project) then `operations/templates/` (app).

### 7.1 Referenced by web views (must exist for those pages to render)

| Template path | Typical use |
|---------------|-------------|
| `operations/auth/login.html` | Login |
| `operations/reports/report_list.html` | PC/ME report list |
| `operations/reports/rider_report_list.html` | Rider/driver list |
| `operations/reports/report_form.html` | Create / rider edit / PC edit |
| `operations/reports/report_detail.html` | Report detail |
| `operations/reports/report_edit_history.html` | PC edit history |
| `operations/reports/report_audit_log_list.html` | PC audit log |

### 7.2 Shared components (project `templates/`)

Examples in repo: `templates/components/` — `form_field.html`, `form_section_*.html`, `card_kpi.html`, `filter_toolbar.html`, etc. Base layouts may live in `templates/` or extend from app templates—match whatever your restored `report_*.html` extend.

### 7.3 Other app templates (if features restored)

Examples present on disk: `operations/dashboards/pc_incidents_list.html`, `operations/settings/district_form.html`, `operations/settings/facility_form.html`, `operations/dashboards/province_kpi_fragment.html` — wire only if you restore the corresponding views/URLs (not all are in the current stub URL table).

---

## 8. Static files

| Item | Notes |
|------|--------|
| `static/` | Project static dir when present (`STATICFILES_DIRS`) |
| `static/css/standalone-shell.css` | Example stylesheet in repo |
| `static/manifest.json` | PWA manifest if you load the app as PWA from same origin |
| `static/icons/` | Icons referenced by manifest (see `README` in icons folder) |

Run `collectstatic` for production.

---

## 9. Context & UX glue

| Item | Location |
|------|----------|
| Nav role | `operations/context_processors.py` → `user_role` in templates |
| CSRF | Enabled; forms POST to same-origin routes |

---

## 10. Data import / seed (optional but typical)

| Command | Purpose |
|---------|---------|
| `import_site_excel`, `import_hubs_csv` | Geography / facilities (see `operations/management/commands/`) |
| `prepare_mobile_seed` | Mobile seed + Capacitor workflow (not strictly required for server-only browser testing) |

---

## 11. Verification (webapp)

1. `python manage.py check`
2. `python manage.py migrate`
3. Log in at `/login/` — redirected by `/` (`role_redirect`) to a reports list.
4. Open `/reports/`, `/reports/create/`, `/pc/reports/` as appropriate role.
5. Exercise POST actions (submit, PC review) and `/ajax/report-facilities/?...` in browser devtools if the UI uses them.

---

## 12. If files were corrupted

Run `python _scan_corruption.py` (repo root) to find NUL bytes or junk in `.py` / `.html`. Replace from backup using this checklist and **`URL_AND_ROUTE_MATRIX.md`** as the contract for routes and template names.

---

## Summary

| Enough alone? | Document |
|----------------|----------|
| **Routes + template names** | `URL_AND_ROUTE_MATRIX.md` |
| **Full webapp clone** | This checklist + **all** code, templates, static, migrations, and seed data above |

Neither doc replaces the **source tree**; they tell you **what must exist** and **where it belongs**.
