# Rider offline-first PWA

## Assets

| File | Role |
|------|------|
| [`static/manifest.json`](../static/manifest.json) | Installability, theme |
| [`static/js/service-worker.js`](../static/js/service-worker.js) | Precache + offline fallback (served at `/service-worker.js`) |
| [`static/js/offline-sync.js`](../static/js/offline-sync.js) | IndexedDB outbox, session + JWT sync, `/api/register-device/` |
| [`static/icons/`](../static/icons/README.md) | Manifest icons |

## IndexedDB

- Database name: `ops_rider_sync` (v2)
- Store: `outbox` — queued operations with auto-increment `id`, fields `op`, `idempotency_key`, `payload`, `created_at`, optional `attempts`, `next_retry_at`, `last_error`
- Store: `drafts` — keyed by `client_uuid` for last saved draft snapshot (optional)

## Ack rules (no duplicate drops)

- The server returns `results[]` with one entry per queued operation (`index` aligned with the request).
- The client **removes an outbox row only when** `results[i].ok === true` or `skipped === true`.
- Failed operations stay in the outbox with exponential backoff; retries use the same `idempotency_key`, so SQL Server does not get duplicate rows.

## Session API (same-origin cookie)

### `POST /api/register-device/`

JSON body:

```json
{
  "device_id": "uuid-stable-per-browser",
  "platform": "browser",
  "user_agent": "..."
}
```

Requires session (rider/driver). Upserts [`RegisteredDevice`](../operations/models.py).

### `POST /api/sync/`

JSON body:

```json
{
  "operations": [
    {
      "op": "upsert_report",
      "idempotency_key": "client-uuid",
      "payload": {
        "week_start": "2026-04-06",
        "title": "",
        "notes": "",
        "samples_collected": 0,
        "extra_data": {}
      }
    }
  ]
}
```

Response: `{ "ok": true, "results": [ { "ok": true, "report_id": 1, ... }, ... ] }`

Idempotency uses `idempotency_key` as `client_uuid` on [`RiderWeeklyReport`](../operations/models.py). Approved reports are not overwritten (**server-wins**).

### Uplink vs bulk SQLite import

- **Runtime uplink** to the backend (MSSQL-backed in production) is these APIs: session **`POST /api/sync/`** or JWT **`POST /api/rider/apply-sync/`**, which apply [`apply_sync_batch`](../operations/services/sync_service.py) on the server. This is what offline clients should use for queued operations.
- **Bulk** loading an entire `db.sqlite3` into SQL Server is a separate **admin** process: [`import_sqlite_data`](../operations/management/commands/import_sqlite_data.py) (see [`ANDROID_BUILD.md`](ANDROID_BUILD.md))—not a substitute for per-operation sync.

## JWT API (Bearer token; Capacitor / native)

Mount: `/api/rider/` (see [`config/urls.py`](../config/urls.py)).

- Register device: `POST /api/rider/register-device/` (same body as session register; uses [`RiderDevice`](../operations/models.py)).
- **Apply sync (same semantics as `/api/sync/`)**: `POST /api/rider/apply-sync/` with header `Authorization: Bearer <access>` and body:

```json
{
  "device_id": "<registered device id>",
  "operations": [ ... same shape as /api/sync/ ... ]
}
```

`POST /api/rider/sync/` is the same handler as `apply-sync/` (alias).

The server calls [`apply_sync_batch`](../operations/services/sync_service.py) with the authenticated **user** (not a separate report schema).

Optional page hints:

```html
<meta name="ops-sync-mode" content="jwt">
<meta name="ops-api-base" content="https://your.api.host">
```

Tokens can be stored as `localStorage.ops_jwt_access` / `ops_jwt_refresh`, or supply `OpsOffline.configure({ mode: 'jwt', apiBase, getAccessToken, getRefreshToken })`.

## UI hooks

- [`rider_report_list.html`](../operations/templates/operations/reports/rider_report_list.html): `data-sync-root`, `#sync-state`, `#sync-pending-count`, `#sync-now-btn`.
- [`report_form.html`](../operations/templates/operations/reports/report_form.html): same; hidden `client_uuid`; `data-week-start` for offline payload.

## Client helper

`window.OpsOffline`:

- `queueReportUpsert(payload, idempotencyKey)` — enqueue
- `syncNow()` — flush outbox (replaces `drainOutbox()`)
- `configure({ mode: 'session'|'jwt', apiBase, getAccessToken, getRefreshToken })`
