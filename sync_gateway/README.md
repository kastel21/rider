# Sync gateway (retired)

This folder previously held a **separate** small Django service that proxied HTTP to another deployment.

The project now uses a **single backend** at the repository root (`manage.py`, `config/`, `operations/`) with MSSQL via [`config/settings.py`](../config/settings.py). See **[`docs/BACKEND_DEPLOYMENT.md`](../docs/BACKEND_DEPLOYMENT.md)**.

Bundled sync for clients is provided by **`GET /api/rider/sync-bundle/`** on that same app (bootstrap + profile + district users).

Do not deploy a second Django process from this directory—the standalone code has been removed.
