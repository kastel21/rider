"""
Chaquopy entry: bind Django WSGI to 127.0.0.1 and run in a background thread.

SQLite: writable DB lives under os.environ["HOME"] (app internal storage). If the
packaged tree contains data/db.sqlite3 (shipped in the APK), it is copied there
once when no DB exists yet — see bundleSeedDatabase in build.gradle.kts.
"""
from __future__ import annotations

import os
import shutil
import socket
import threading
import time

_SERVER_THREAD: threading.Thread | None = None


def _prepare_sqlite_for_android(base: str) -> None:
    """
    Point Django at a writable SQLite file. Optionally seed from bundled data/db.sqlite3.
    Chaquopy sets HOME to the app's files directory; APK assets are not reliably writable.
    """
    home = (os.environ.get("HOME") or "").strip()
    seed = os.path.join(base, "data", "db.sqlite3")

    if home:
        dest_dir = os.path.join(home, "django_data")
        os.makedirs(dest_dir, exist_ok=True)
        dest = os.path.join(dest_dir, "db.sqlite3")
        if os.path.isfile(seed) and not os.path.isfile(dest):
            shutil.copy2(seed, dest)
        os.environ["DJANGO_SQLITE_PATH"] = dest
        return

    # Desktop / tests: keep DB under the project tree
    data_dir = os.path.join(base, "data")
    os.makedirs(data_dir, exist_ok=True)
    dest = os.path.join(data_dir, "db.sqlite3")
    if os.path.isfile(seed) and not os.path.isfile(dest):
        shutil.copy2(seed, dest)
    os.environ["DJANGO_SQLITE_PATH"] = dest


def _wait_tcp(host: str, port: int, timeout_sec: float = 20.0) -> bool:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.25):
                return True
        except OSError:
            time.sleep(0.05)
    return False


def _run_wsgi(
    port: int,
    secret_key: str,
    remote_api_base: str,
    debug_build: bool = False,
    jwt_signing_key: str = "",
    embedded_import_secret: str = "",
) -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    os.environ["DJANGO_BASE_DIR"] = base
    _prepare_sqlite_for_android(base)

    if secret_key:
        os.environ["DJANGO_SECRET_KEY"] = secret_key
    if remote_api_base:
        os.environ["OPS_REMOTE_API_BASE"] = remote_api_base
    if jwt_signing_key:
        os.environ["JWT_SIGNING_KEY"] = jwt_signing_key
    emb = str(embedded_import_secret or "").strip()
    if emb:
        os.environ["OPS_EMBEDDED_IMPORT_SECRET"] = emb
    os.environ.setdefault("OPS_SYNC_MODE", "jwt")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings_android")
    os.environ["DJANGO_DEBUG"] = "1" if debug_build else "0"

    # Chaquopy/Android has no OS zoneinfo database; PyPI `tzdata` backs zoneinfo (TIME_ZONE=UTC).
    import tzdata  # noqa: F401

    import django

    django.setup()

    from django.core.management import call_command

    call_command("migrate", "--noinput")

    from django.core.wsgi import get_wsgi_application
    from socketserver import ThreadingMixIn
    from wsgiref.simple_server import WSGIRequestHandler, WSGIServer, make_server

    application = get_wsgi_application()

    class QuietHandler(WSGIRequestHandler):
        def log_message(self, format: str, *args) -> None:  # noqa: A003
            pass

    class ThreadedWSGIServer(ThreadingMixIn, WSGIServer):
        """WebView loads HTML + assets in parallel; single-thread WSGI can misbehave or stall."""
        daemon_threads = True

    httpd = make_server(
        "127.0.0.1",
        port,
        application,
        server_class=ThreadedWSGIServer,
        handler_class=QuietHandler,
    )
    httpd.serve_forever()


def _truthy_debug(value: object) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value != 0
    return str(value).strip().lower() in ("1", "true", "yes")


def start_server(
    port: int,
    secret_key: str = "",
    remote_api_base: str = "",
    debug_build: object = 0,
    jwt_signing_key: str = "",
    embedded_import_secret: str = "",
) -> int:
    """Start Django on 127.0.0.1:port in a daemon thread; return 1 when the port accepts connections."""
    global _SERVER_THREAD
    if _SERVER_THREAD is not None and _SERVER_THREAD.is_alive():
        return 1

    port = int(port)
    dbg = _truthy_debug(debug_build)
    jwt_key = str(jwt_signing_key or "")
    emb_sec = str(embedded_import_secret or "")

    def target() -> None:
        _run_wsgi(
            port,
            secret_key or "",
            remote_api_base or "",
            debug_build=dbg,
            jwt_signing_key=jwt_key,
            embedded_import_secret=emb_sec,
        )

    _SERVER_THREAD = threading.Thread(target=target, name="django-wsgi", daemon=True)
    _SERVER_THREAD.start()
    return 1 if _wait_tcp("127.0.0.1", port) else 0
