# SQL Server production and deployment runbook

## Environment variables (Django)

Set `DJANGO_DB_ENGINE=mssql` and provide:

| Variable | Description |
|----------|-------------|
| `MSSQL_DATABASE` | Database name |
| `MSSQL_USER` / `MSSQL_PASSWORD` | Credentials |
| `MSSQL_HOST` / `MSSQL_PORT` | Server (default port `1433`) |
| `ODBC_DRIVER` | e.g. `ODBC Driver 18 for SQL Server` |
| `MSSQL_EXTRA_PARAMS` | e.g. `Encrypt=yes;TrustServerCertificate=yes;` for dev |

Alternatively use `DJANGO_DB_ENGINE=postgresql` with `POSTGRES_*` variables, or omit for **SQLite** (`db.sqlite3`) for local dev.

## Migrations

1. Take a **backup** of any existing database before applying migrations.
2. On a staging SQL Server instance: `python manage.py migrate`.
3. Verify with `python manage.py check` and smoke-test login + reports.
4. Apply to production during a maintenance window if needed.

Never replace live migration history with a single squashed `0001_initial` without a data migration plan.

## HTTPS, CSRF, cookies

For production behind HTTPS:

```text
DJANGO_DEBUG=0
DJANGO_SESSION_COOKIE_SECURE=1
DJANGO_CSRF_COOKIE_SECURE=1
DJANGO_CSRF_TRUSTED_ORIGINS=https://your.domain
DJANGO_ALLOWED_HOSTS=your.domain
```

Generate a strong `DJANGO_SECRET_KEY` and store it outside the repo.

## Static files

```bash
python manage.py collectstatic --noinput
```

Serve `STATIC_ROOT` via your reverse proxy or WhiteNoise.
