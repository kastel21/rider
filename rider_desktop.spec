# -*- mode: python ; coding: utf-8 -*-
# Build: pip install pyinstaller && python manage.py collectstatic --noinput && pyinstaller rider_desktop.spec
import os
import sys
from pathlib import Path

from PyInstaller.building.api import COLLECT, EXE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.utils.hooks import collect_all, collect_submodules

_spec_parent = Path(SPECPATH).resolve().parent
_cwd = Path.cwd().resolve()
PROJECT = _spec_parent if (_spec_parent / "manage.py").is_file() else _cwd
if not (PROJECT / "manage.py").is_file():
    raise SystemExit(
        f"rider_desktop.spec: project root not found (SPECPATH={SPECPATH!r}, tried {_spec_parent} and {_cwd})"
    )

sys.path.insert(0, str(PROJECT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django

django.setup()

datas = []
binaries = []
hiddenimports = []

# Avoid collect_all(openpyxl/reportlab): it pulls optional stacks (pandas/matplotlib) and duplicate Qt bindings.
for pkg in (
    "django",
    "rest_framework",
    "rest_framework_simplejwt",
    "whitenoise",
    "waitress",
    "webview",
):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception:
        pass

hiddenimports += [
    "reportlab",
    "openpyxl",
    "mssql",
    "mssql_django",
    "pyodbc",
]

datas.append((str(PROJECT / "templates"), "templates"))
datas.append((str(PROJECT / "operations"), "operations"))
datas.append((str(PROJECT / "config"), "config"))
datas.append((str(PROJECT / "static"), "static"))
if (PROJECT / "staticfiles").is_dir():
    datas.append((str(PROJECT / "staticfiles"), "staticfiles"))

_bundled_db = PROJECT / "desktop_seed" / "db.sqlite3"
if _bundled_db.is_file():
    datas.append((str(_bundled_db), "desktop_seed"))

hiddenimports += collect_submodules("operations")
hiddenimports += [
    "config.settings",
    "config.wsgi",
    "config.urls",
]

block_cipher = None

a = Analysis(
    [str(PROJECT / "desktop_launcher.py")],
    pathex=[str(PROJECT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "pandas",
        "scipy",
        "matplotlib",
        "IPython",
        "jupyter",
        "pytest",
        "PySide6",
        "PySide2",
        "PyQt5",
        "PyQt6",
        "tkinter",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RiderOperations",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="RiderOperations",
)
