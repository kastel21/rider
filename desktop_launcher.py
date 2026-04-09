"""
Windows desktop entry: local Waitress server + pywebview shell.
Set env before Django loads. PyInstaller entry: `pyinstaller rider_desktop.spec`.
"""
from __future__ import annotations

import os
import shutil
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path


def _pick_port(host: str) -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, 0))
    port = int(s.getsockname()[1])
    s.close()
    return port


def _bootstrap_runtime_env() -> tuple[str, int]:
    host = "127.0.0.1"
    port = _pick_port(host)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    os.environ["RIDER_DESKTOP_PORT"] = str(port)
    os.environ["DJANGO_CSRF_TRUSTED_ORIGINS"] = f"http://{host}:{port}"
    if getattr(sys, "frozen", False):
        os.environ.setdefault("DJANGO_DATA_DIR", str(Path(sys.executable).parent))
    os.environ.setdefault("DJANGO_DEBUG", "0")
    os.environ.setdefault("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
    return host, port


def _seed_bundled_sqlite() -> None:
    """First run: copy pre-built DB from the PyInstaller bundle beside the exe (SQLite only)."""
    if not getattr(sys, "frozen", False):
        return
    data_dir = Path(os.environ.get("DJANGO_DATA_DIR", Path(sys.executable).parent))
    try:
        from dotenv import load_dotenv

        load_dotenv(data_dir / ".env")
    except Exception:
        pass
    engine = os.environ.get("DJANGO_DB_ENGINE", "").strip().lower()
    if engine in ("mssql", "postgresql"):
        return
    target = data_dir / "db.sqlite3"
    if target.exists():
        return
    meipass = Path(getattr(sys, "_MEIPASS", ""))
    seed = meipass / "desktop_seed" / "db.sqlite3"
    if not seed.is_file():
        return
    data_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(seed, target)


def _wait_for_http(url: str, timeout_s: float = 30.0) -> None:
    deadline = time.monotonic() + timeout_s
    last_err: Exception | None = None
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1.0)
            return
        except (urllib.error.URLError, OSError) as e:
            last_err = e
            time.sleep(0.1)
    raise RuntimeError(f"Server did not respond at {url!r}") from last_err


def _run_waitress(app, host: str, port: int) -> None:
    from waitress import serve

    serve(app, host=host, port=port, threads=6)


def main() -> None:
    host, port = _bootstrap_runtime_env()
    _seed_bundled_sqlite()

    import django

    django.setup()

    from django.core.management import call_command
    from config.wsgi import application

    call_command("migrate", "--noinput", verbosity=0)

    url = f"http://{host}:{port}/"
    thread = threading.Thread(target=_run_waitress, args=(application, host, port), daemon=True)
    thread.start()
    _wait_for_http(url)

    import webview

    webview.create_window("Operations", url, width=1400, height=900)
    webview.start()
    sys.exit(0)


if __name__ == "__main__":
    main()
