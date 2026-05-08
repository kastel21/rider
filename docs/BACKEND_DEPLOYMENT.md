# Backend deployment (single Django app)

**Track A (chosen):** The repository root is the **only** server-side Django project: [`manage.py`](../manage.py), [`config/`](../config/), [`operations/`](../operations/). Deploy this tree with **`DJANGO_DB_ENGINE=mssql`** and the usual MSSQL environment variables ([`config/settings.py`](../config/settings.py)).

**CloudClusters / PaaS:** Set database variables in the **hosting control panel** (environment variables for `uwsgi`), not only in a local `.env` file. If `DJANGO_DB_ENGINE` is missing, Django falls back to SQLite under the app directory; that path is often **not writable**, which surfaces as `OperationalError: unable to open database file`. Fix by setting `DJANGO_DB_ENGINE=mssql` plus `MSSQL_*` (and ensure the Linux image has ODBC + FreeTDS or Microsoft ODBC for SQL Server, and `pyodbc`). For a temporary SQLite-only deploy, create a writable directory on the server and set `DJANGO_SQLITE_PATH` to an absolute path like `/cloudclusters/data/db.sqlite3` (and run migrations there).

There is **no** separate “Operations” server process and **no** standalone `sync_gateway` service in front of it. The former [`sync_gateway/`](../sync_gateway/) package was a thin HTTP proxy to a second deployment; that layout is **retired**. Mobile and web clients use **one public HTTPS base URL** (see [`docs/ANDROID_BUILD.md`](ANDROID_BUILD.md) `OPS_REMOTE_API_BASE`).

**MSSQL** is reached only through this Django app’s ORM (`DATABASES["default"]`).

Optional one-shot: `GET /api/rider/sync-bundle/` returns bootstrap, profile, and district user export in a single JSON payload for offline seeding flows.
