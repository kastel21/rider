"""
Django settings for embedded Android (Chaquopy + WebView + local SQLite).

Set DJANGO_BASE_DIR to the extracted app root (directory containing config/, operations/, templates/)
before importing Django. Optional: OPS_REMOTE_API_BASE, OPS_SYNC_MODE, DJANGO_SECRET_KEY.
DJANGO_SQLITE_PATH is set by android/app/src/main/python/server.py to a writable db file.
"""
import os
from pathlib import Path

if not os.environ.get("DJANGO_BASE_DIR", "").strip():
    raise RuntimeError("DJANGO_BASE_DIR must be set before loading config.settings_android")

os.environ["DJANGO_DB_ENGINE"] = ""
os.environ.setdefault("DJANGO_DEBUG", "0")

from .settings import *  # noqa: E402, F403, F405

# server.py / MainActivity set DJANGO_DEBUG=1 on debug APKs so the yellow error page shows the real exception.
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

# server.py sets this to a writable path on Android (under HOME/django_data/)
_sqlite_path = os.environ.get("DJANGO_SQLITE_PATH", "").strip()
_sqlite_opts = {"timeout": 30}  # reduce "database is locked" under WebView + parallel requests
if _sqlite_path:
    DATA_DIR = Path(_sqlite_path).parent
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": _sqlite_path,
            "OPTIONS": _sqlite_opts,
            "ATOMIC_REQUESTS": True,
        }
    }
else:
    DATA_DIR = BASE_DIR / "data"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DATA_DIR / "db.sqlite3",
            "OPTIONS": _sqlite_opts,
            "ATOMIC_REQUESTS": True,
        }
    }

# Surface view exceptions in adb logcat (tags python.stderr / django)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "stderr": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["stderr"],
            "level": "ERROR",
            "propagate": False,
        },
    },
    "root": {"handlers": ["stderr"], "level": "INFO"},
}

_mw = list(MIDDLEWARE)
if "whitenoise.middleware.WhiteNoiseMiddleware" not in _mw:
    _mw.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
MIDDLEWARE = _mw

STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

WSGI_APPLICATION = "config.wsgi.application"

OPS_SYNC_MODE = os.environ.get("OPS_SYNC_MODE", "jwt").strip()
OPS_REMOTE_API_BASE = os.environ.get("OPS_REMOTE_API_BASE", "").strip()
OPS_RIDER_REMOTE_PROXY = os.environ.get("OPS_RIDER_REMOTE_PROXY", "0") == "1"
OPS_ALLOW_LOCAL_JWT_MINT = os.environ.get("OPS_ALLOW_LOCAL_JWT_MINT", "1") == "1"

# Helps SQLite when the threaded WSGI server handles parallel static + HTML requests.
from django.db.backends.signals import connection_created  # noqa: E402


def _sqlite_wal(sender, connection, **_kwargs):
    if getattr(connection, "vendor", None) != "sqlite":
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA journal_mode=WAL;")
    except Exception:
        pass


connection_created.connect(_sqlite_wal)

# Validate remote JWTs minted by the central server (must match that server's signing key).
_jwt_signing = os.environ.get("JWT_SIGNING_KEY", "").strip()
if _jwt_signing:
    _sj = dict(SIMPLE_JWT)
    _sj["SIGNING_KEY"] = _jwt_signing
    SIMPLE_JWT = _sj
