"""
Django settings for operations dashboard.
DB: MSSQL (production) → PostgreSQL → SQLite fallback via env.
"""
import os
import sys
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv


def _resolve_base_and_data() -> Tuple[Path, Path]:
    """Dev: one tree. PyInstaller: read-only bundle + writable folder beside the exe."""
    if getattr(sys, "frozen", False):
        bundle = Path(getattr(sys, "_MEIPASS", Path(sys.executable).parent))
        data = Path(os.environ.get("DJANGO_DATA_DIR", Path(sys.executable).parent))
        return bundle, data
    override = os.environ.get("DJANGO_BASE_DIR", "").strip()
    if override:
        p = Path(override).resolve()
        return p, p
    p = Path(__file__).resolve().parent.parent
    return p, p


BASE_DIR, DATA_DIR = _resolve_base_and_data()
load_dotenv(DATA_DIR / ".env")

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY", "dad9363ac7d3a69bbb46b53e74b54410ec35337a625f1128bf4913507fe6e54d9362474b761370f3433df53d46bf3165"
)

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

_allowed = os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,https://pythonclusters-208233-0.cloudclusters.net")
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "operations",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "operations.middleware.rider_api_cors.RiderApiCorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "operations.middleware.no_cache_html.NoCacheDynamicHtmlMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "operations.context_processors.operations_nav",
                "operations.context_processors.ops_sync_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database (env-driven) ---
_db_engine = os.environ.get("DJANGO_DB_ENGINE", "").lower()

if _db_engine == "mssql":
    DATABASES = {
        "default": {
            "ENGINE": "mssql",
            "NAME": os.environ.get("MSSQL_DATABASE", ""),
            "USER": os.environ.get("MSSQL_USER", ""),
            "PASSWORD": os.environ.get("MSSQL_PASSWORD", ""),
            "HOST": os.environ.get("MSSQL_HOST", "localhost"),
            "PORT": os.environ.get("MSSQL_PORT", "1433"),
            "OPTIONS": {
                "driver": os.environ.get("ODBC_DRIVER", "ODBC Driver 18 for SQL Server"),
                "extra_params": os.environ.get("MSSQL_EXTRA_PARAMS", "Encrypt=yes;TrustServerCertificate=yes;"),
            },
            "ATOMIC_REQUESTS": True,
        }
    }
elif _db_engine == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "operations"),
            "USER": os.environ.get("POSTGRES_USER", "postgres"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
            "ATOMIC_REQUESTS": True,
        }
    }
else:
    # Default SQLite path is under the project tree; on many hosts (e.g. PaaS) that path is not writable.
    # Set DJANGO_SQLITE_PATH to an absolute path in a writable directory if you must use SQLite.
    _sqlite_name = os.environ.get("DJANGO_SQLITE_PATH", "").strip()
    if _sqlite_name:
        _sqlite_path = Path(_sqlite_name).expanduser().resolve()
    else:
        _sqlite_path = DATA_DIR / "db.sqlite3"
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(_sqlite_path),
            "ATOMIC_REQUESTS": True,
        }
    }

# Second DB alias for one-off imports: copy legacy SQLite into default (e.g. MSSQL).
# Set DJANGO_SQLITE_IMPORT_PATH to an absolute path of db.sqlite3, reload, then run:
#   python manage.py import_sqlite_data --flush-target
_sqlite_import = os.environ.get("DJANGO_SQLITE_IMPORT_PATH", "").strip()
if _sqlite_import:
    _sqlite_path = Path(_sqlite_import)
    if _sqlite_path.is_file() and DATABASES["default"]["ENGINE"] != "django.db.backends.sqlite3":
        DATABASES["sqlite"] = {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": str(_sqlite_path.resolve()),
            "ATOMIC_REQUESTS": True,
        }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
WHITENOISE_USE_FINDERS = DEBUG

LOGIN_URL = "operations:login"
LOGIN_REDIRECT_URL = "operations:role_redirect"
LOGOUT_REDIRECT_URL = "operations:login"

# Session / cookies (tighten in production behind HTTPS)
SESSION_COOKIE_SECURE = os.environ.get("DJANGO_SESSION_COOKIE_SECURE", "0") == "1"
CSRF_COOKIE_SECURE = os.environ.get("DJANGO_CSRF_COOKIE_SECURE", "0") == "1"
SESSION_COOKIE_SAMESITE = os.environ.get("DJANGO_SESSION_COOKIE_SAMESITE", "Lax")
CSRF_COOKIE_SAMESITE = os.environ.get("DJANGO_CSRF_COOKIE_SAMESITE", "Lax")
_csrf_origins = os.environ.get("DJANGO_CSRF_TRUSTED_ORIGINS", "")
CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf_origins.split(",") if o.strip()]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# Optional: rider PWA JWT sync to a remote API (e.g. central MSSQL deployment). Used in templates/base.html.
OPS_SYNC_MODE = os.environ.get("OPS_SYNC_MODE", "").strip()
OPS_REMOTE_API_BASE = os.environ.get("OPS_REMOTE_API_BASE", "").strip()
OPS_ALLOW_LOCAL_JWT_MINT = os.environ.get("OPS_ALLOW_LOCAL_JWT_MINT", "0") == "1"
