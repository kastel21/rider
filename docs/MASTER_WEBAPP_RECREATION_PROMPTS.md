# Master guide: recreating the dashboard web app (prompts + doc map)

Use this file as the **single entry point** when you (or an AI assistant) need to **rebuild or reproduce** the session-based Django web UI, the rider PWA shell, and related native/desktop packaging. It **does not replace** the other markdown files; it **indexes them** and supplies **ready-to-paste prompts** that embed their requirements.

---

## 1. Documentation map (all first-party Markdown in this repo)

Read these in order for a full picture. Paths are relative to the project root (`dashboard - PWA`).

| Document | Purpose |
|----------|---------|
| **`docs/WEBAPP_REPRODUCTION_CHECKLIST.md`** | Full checklist: Django project layout, `settings.py`, models/migrations, URL wiring, views, templates, static, context processors, optional seed commands, verification commands. |
| **`docs/URL_AND_ROUTE_MATRIX.md`** | Session **browser** routes, URL names, view classes, and template names. **Cross-check** with live `operations/urls.py` — the matrix may describe older stub routes while the codebase uses real `pc_module_views` for PC modules. |
| **`docs/RIDER_PWA_REQUIREMENTS.md`** | Rider offline-first PWA: IndexedDB, service worker scope, `/api/sync/` session sync, `client_uuid`, UI hooks, `manifest.json`, Capacitor pointers. |
| **`docs/ANDROID_DESKTOP_BUILD.md`** | Android (standalone vs server URL), npm scripts, Electron desktop entry. |
| **`docs/SQL_SERVER_AND_DEPLOY.md`** | SQL Server / Postgres env, migrations runbook, HTTPS and `collectstatic`. |
| **`static/icons/README.md`** | Required PWA icon sizes and manifest references. |

**Not covered as separate files in `docs/` (but part of the app):** `requirements.txt`, `config/settings.py`, `operations/models.py`, `manage.py`, `package.json` scripts, `tools/` sync scripts, `electron/main.js`. Treat the **source tree** as the contract; the docs describe what must exist and where.

**Integrity tooling:** `_scan_corruption.py` at repo root — run to detect NUL-byte damage in `.py` / `.html` (and related). If migrations fail with “null bytes” or SQLite errors, see **§7**.

---

## 2. Principles before you prompt

1. **Source of truth:** The **Git/source tree** (or a verified backup) wins over any markdown table. After reproducing, diff `operations/urls.py` against `URL_AND_ROUTE_MATRIX.md` and update the matrix if needed.
2. **Scope:** “Web app” here = **Django session UI** + **same-origin** AJAX/PWA endpoints listed in the checklist and route matrix. **Excluded** from the matrix: JWT rider API under `/api/rider/` (see `operations/api/urls.py`) unless you explicitly add it to scope.
3. **Environments:** `config/settings.py` picks DB by env: MSSQL → PostgreSQL → **SQLite** fallback (`db.sqlite3`). Local dev usually uses SQLite without extra env vars.
4. **PWA:** Rider install/offline behavior depends on **`static/manifest.json`**, **`static/js/service-worker.js`**, **`static/js/offline-sync.js`**, and templates linking the manifest — see `RIDER_PWA_REQUIREMENTS.md`.

---

## 3. Master prompt — full stack (single message)

Copy and adapt the bracketed parts.

```text
You are helping reproduce a Django “operations” logistics dashboard with session auth, PC/rider report flows, optional PC module pages, and a rider offline-first PWA (IndexedDB + service worker + session JSON sync).

Constraints and references (must follow):
- Read and apply: docs/WEBAPP_REPRODUCTION_CHECKLIST.md, docs/URL_AND_ROUTE_MATRIX.md (verify against operations/urls.py), docs/RIDER_PWA_REQUIREMENTS.md, docs/ANDROID_DESKTOP_BUILD.md, static/icons/README.md.
- Django: project package `config/`, app `operations/`, ROOT_URLCONF `config.urls`, templates DIRS include project `templates/` and app templates, context processor `operations.context_processors.operations_nav`.
- Implement or restore URL names and paths so `reverse('operations:…')` matches the matrix; use `operations/urls.py` as the live source of truth if the matrix disagrees.
- Web templates required for core flows: operations/auth/login.html; operations/reports/report_list.html, rider_report_list.html, report_form.html, report_detail.html, report_edit_history.html, report_audit_log_list.html; shared components under templates/components/ and base layouts as used by report templates.
- Static: STATIC_URL / STATICFILES_DIRS per checklist; PWA: static/manifest.json, static/js/offline-sync.js, static/js/service-worker.js, static/css as referenced; icons per static/icons/README.md.
- Data: models in operations/models.py; migrations under operations/migrations/; run python manage.py check && migrate; create superuser and UserProfile roles for testing.
- Optional: management commands under operations/management/commands/ for imports; Android/Electron per ANDROID_DESKTOP_BUILD.md only if building those targets.

Deliverables: [e.g. file tree summary, key settings snippets, migration strategy, test steps: login → role redirect → reports list → create/edit → PC review if applicable → PWA sync smoke test].

Repository root: [path or zip]. Do not invent routes; align with the docs above and the actual urls.py in the tree.
```

---

## 4. Phased prompts (smaller chunks)

Use these when you want incremental AI or human steps.

### Phase A — Django skeleton and settings

```text
Using docs/WEBAPP_REPRODUCTION_CHECKLIST.md sections 1–3 and 9, create or verify: manage.py, config/settings.py (INSTALLED_APPS including operations, rest_framework, simplejwt if present, TEMPLATES DIRS, DATABASES env logic, STATIC_*, AUTH redirects, MIDDLEWARE), and config/urls.py including admin and path('', include('operations.urls')). Match naming and structure to the checklist; do not omit operations.context_processors.operations_nav.
```

### Phase B — Models and migrations

```text
Using docs/WEBAPP_REPRODUCTION_CHECKLIST.md section 4, align operations/models.py with the domain (provinces, facilities, bikes, RiderWeeklyReport, audit, PC modules, etc.). Ensure operations/migrations/ are consistent with models; run migrations on a fresh SQLite DB. If the migration history was lost or corrupted, document whether you regenerated a single initial migration (dev-only) or restored files from backup — see MASTER doc §7.
```

### Phase C — URLs and views (session web)

```text
Using docs/URL_AND_ROUTE_MATRIX.md and the live operations/urls.py, implement views in operations/views/ (auth_views, report_views, pc_report_views, report_export_views, pc_module_views or stubs as in repo). Preserve URL names for reverse(). Implement permissions per operations/permissions.py and querysets per operations/selectors.py as in the checklist section 6. If the matrix still lists NotRestoredView for PC paths but urls.py uses real module views, follow urls.py.
```

### Phase D — Templates and static

```text
Using WEBAPP_REPRODUCTION_CHECKLIST.md section 7–8 and URL_AND_ROUTE_MATRIX.md “Templates used by the web app”, ensure every template path listed exists and extends the correct base/components. Add static/css/standalone-shell.css or equivalents referenced by templates. Run template lint / Django check.
```

### Phase E — Rider PWA

```text
Implement per docs/RIDER_PWA_REQUIREMENTS.md: IndexedDB schema and offline-sync.js behavior; service-worker.js scope and caches; session POST endpoints for register-device and sync in operations/urls.py; client_uuid idempotency on RiderWeeklyReport; sync status UI IDs in rider_report_list.html and report_form.html; link manifest.json on rider pages; icons per static/icons/README.md.
```

### Phase F — Android / desktop (optional)

```text
Follow docs/ANDROID_DESKTOP_BUILD.md: Node version, npm scripts (android:sync, android:install:debug, android:bundle, server-backed variants), Electron desktop:start / desktop:dist. Do not bundle secrets; document CAPACITOR_SERVER_URL when using server mode.
```

### Phase G — Verification

```text
Execute the checklist’s verification section: python manage.py check; migrate; log in at /login/; follow role_redirect; open /reports/, /reports/create/, /pc/reports/ as appropriate roles; test POST review actions and /ajax/report-facilities/ if the UI uses them; for PWA, test offline queue and sync per RIDER_PWA_REQUIREMENTS.md.
```

---

## 5. Prompt — integrity and corruption recovery

```text
Run python _scan_corruption.py from the repo root. For any file flagged with NUL bytes in operations/migrations/, operations/views/, operations/templates/, or operations/services/, replace from a known-good backup or regenerate (e.g. makemigrations after models match, only for fresh dev DBs). Strip accidental UTF-8 BOM from Python modules if compile/import fails. If db.sqlite3 errors with “file is not a database”, rename it aside and run migrate to recreate. Document what was restored vs regenerated.
```

---

## 6. Prompt — align documentation after code changes

```text
If operations/urls.py or templates changed during implementation, update docs/URL_AND_ROUTE_MATRIX.md and any affected sections of WEBAPP_REPRODUCTION_CHECKLIST.md so the next reproduction attempt does not rely on stale route or template names. Do not delete historical notes; add a short “Last aligned with commit/date” line if the team uses version control.
```

---

## 7. Migration and database caveats (read once)

- **Production:** Never replace a live database’s migration history with a single new `0001_initial` without a migration plan. The checklist allows **full migration history** from `operations/migrations/` when files are valid.
- **Damaged trees:** NUL-corrupted `.py` files cannot be imported. Restore from backup or regenerate; then `manage.py migrate`.
- **Fresh dev SQLite:** A single consolidated initial migration may be acceptable only when there is **no** existing data depending on old migration names.
- **Corrupt `db.sqlite3`:** Rename the file and run `migrate` again.

---

## 8. One-line “what to open” summary

| Goal | Open first |
|------|------------|
| Server-rendered web parity | `WEBAPP_REPRODUCTION_CHECKLIST.md` + `URL_AND_ROUTE_MATRIX.md` + `operations/urls.py` |
| Rider PWA / offline | `RIDER_PWA_REQUIREMENTS.md` + `static/js/*.js` + `static/manifest.json` |
| Android / Windows `.exe` | `ANDROID_DESKTOP_BUILD.md` + `package.json` |
| Icons / install | `static/icons/README.md` + `static/manifest.json` |
| Suspect file damage | `_scan_corruption.py` |

---

*This master file should be updated when new first-party `docs/*.md` files are added so §1 and the prompts stay complete.*
