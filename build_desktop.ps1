# Build standalone Windows desktop app (PyInstaller onedir). Requires Python 3.10+ and Microsoft Edge WebView2 Runtime.
# Optional: .\build_desktop.ps1 -BundledSqlitePath "D:\path\to\snapshot.sqlite3"  (defaults to .\db.sqlite3)
param(
    [string]$BundledSqlitePath = ""
)
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$seedSrc = if ($BundledSqlitePath -ne "") { $BundledSqlitePath } else { Join-Path $PSScriptRoot "db.sqlite3" }
$seedDstDir = Join-Path $PSScriptRoot "desktop_seed"
$seedDst = Join-Path $seedDstDir "db.sqlite3"
New-Item -ItemType Directory -Force -Path $seedDstDir | Out-Null
if (-not (Test-Path -LiteralPath $seedSrc)) {
    Write-Error "Missing db.sqlite3 at project root. Use SQLite locally (empty DJANGO_DB_ENGINE), run migrations and load your data, then build again."
    exit 1
}
Copy-Item -LiteralPath $seedSrc -Destination $seedDst -Force
Write-Host "Bundled database snapshot: desktop_seed\db.sqlite3 (from project db.sqlite3)"

python -m pip install -r requirements.txt
python -m pip install pyinstaller
python manage.py collectstatic --noinput
python -m PyInstaller --noconfirm rider_desktop.spec

Write-Host ""
Write-Host "Done. Run: dist\RiderOperations\RiderOperations.exe"
Write-Host "First launch copies the bundled DB beside the exe if db.sqlite3 is not there yet."
Write-Host "Place .env next to the exe for MSSQL/Postgres or other overrides (bundled seed is SQLite-only)."
