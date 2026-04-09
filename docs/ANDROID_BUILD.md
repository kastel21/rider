# Android APK / App Bundle (Chaquopy)

This project ships a standalone Android app under [`android/`](../android/): a **WebView** loads **Django** bound to `127.0.0.1` with **SQLite** on device. For uploading data to the **backend** (Django + **MSSQL** in production), configure the remote API base URL (see below). There is a **single** server-side Django app—see [`BACKEND_DEPLOYMENT.md`](BACKEND_DEPLOYMENT.md).

## Prerequisites

- [Android Studio](https://developer.android.com/studio) (includes Android SDK and Gradle).
- **JDK 17** for Gradle (Android Studio bundles one; command-line builds need a valid install). This repo sets `org.gradle.java.home` in [`android/gradle.properties`](../android/gradle.properties) to `C:/Program Files/Java/jdk-17`. If your JDK lives elsewhere, change that line or set `JAVA_HOME` to your JDK 17 root.
- On the build machine: **Python 3** on `PATH` (`py -3` on Windows) to run `collectstatic` before release builds.

## One-time: static files

After Gradle syncs the Django tree into `android/app/src/main/python/`, collect static assets into `staticfiles/` (required for WhiteNoise when `DEBUG=False`):

**Windows (PowerShell)** from the repository root:

```powershell
cd android\app\src\main\python
$env:DJANGO_BASE_DIR = (Get-Location).Path
$env:DJANGO_SETTINGS_MODULE = "config.settings_android"
py -3 manage.py collectstatic --noinput
```

**macOS / Linux:**

```bash
cd android/app/src/main/python
export DJANGO_BASE_DIR="$(pwd)"
export DJANGO_SETTINGS_MODULE=config.settings_android
python3 manage.py collectstatic --noinput
```

Re-run this when static assets or templates change.

## Pre-populated SQLite (ship your current data in the APK)

The Gradle task **`bundleSeedDatabase`** (in [`android/app/build.gradle.kts`](../android/app/build.gradle.kts)) copies the repository file **`db.sqlite3`** from the project root into `android/app/src/main/python/data/db.sqlite3` before the APK is built, **if that file exists**.

On first launch, [`server.py`](../android/app/src/main/python/server.py) copies that bundled file to **writable app storage** (`HOME/django_data/db.sqlite3`) and sets `DJANGO_SQLITE_PATH` so Django uses it ([`config/settings_android.py`](../config/settings_android.py)). If the device already has a database from a previous install, the copy is **skipped** so user data is not overwritten.

**Workflow**

1. On your machine, use the same SQLite database you want riders to start with (export from MSSQL/import into SQLite if needed, or use your existing dev `db.sqlite3` at the repo root).
2. Ensure **`db.sqlite3`** is present at **`d:\projects\rider app\db.sqlite3`** (the parent of the `android/` folder).
3. Build the APK as usual; `preBuild` runs `bundleSeedDatabase` automatically.

**Caveats**

- The APK size grows with the database.
- Anyone who extracts the APK can read the bundled SQLite; do not ship production secrets or sensitive PII without understanding that risk.
- Schema updates after the ship: `migrate` still runs on startup and will apply new migrations to the copied DB.

## Landing sync + local login (`local.properties`)

The app launcher is **Sync data** ([`LandingActivity`](../android/app/src/main/java/com/operations/rider/LandingActivity.kt)): a **service account** on the backend calls `POST /api/rider/login/`, then `GET /api/rider/bootstrap/` and `GET /api/rider/profile/`, and applies that JSON into the device SQLite via `POST /api/embedded/import-bootstrap/` (protected by a shared secret). Bootstrap scope follows **that service rider’s district**, not every user on the server.

Optionally you can replace those three GETs with **`GET /api/rider/sync-bundle/`** (same JWT) to fetch bootstrap, profile, and district user list in one response; the embedded import steps stay the same.

Then, when a `district_id` can be read from bootstrap/profile, the app calls **`GET /api/rider/mobile-user-export/?district_id=…`** (same JWT) and applies the result with **`POST /api/embedded/import-users/`** so **local `User` rows match backend password hashes** for riders in that district (see [`operations/api/mobile_export_views.py`](../operations/api/mobile_export_views.py)). **Threat model:** anyone who can call that export or read the device DB after sync can reuse password hashes—use HTTPS, least privilege, and treat offline DBs as sensitive.

Add to **`android/local.properties`** (do not commit secrets):

```properties
OPS_REMOTE_API_BASE=https://your-server.example.com
OPS_SYNC_USERNAME=service_rider_username
OPS_SYNC_PASSWORD=service_rider_password
OPS_EMBEDDED_IMPORT_SECRET=a_long_random_shared_secret
```

Optional: `JWT_SIGNING_KEY=...` only if you still use JWT tooling against the embedded API.

**Local WebView login** (`/login/`) uses Django’s normal session auth against **local** SQLite. After user import, riders can log in with the **same credentials as the backend** for that district (subject to export scope).

### Device → backend (SQLite app state → MSSQL)

The device **never** opens a SQL connection to MSSQL. Authoritative **uplink** of offline work (e.g. weekly reports) is **`POST /api/rider/apply-sync/`** (JWT) or session **`POST /api/sync/`**, which runs [`apply_sync_batch`](../operations/services/sync_service.py) on the server and persists to whatever database `default` uses (**MSSQL** in production). That is the normal path for operational sync.

**Bulk** one-off copy of a whole SQLite file into MSSQL is a **server-side admin** workflow only: [`import_sqlite_data`](../operations/management/commands/import_sqlite_data.py) with `DJANGO_SQLITE_IMPORT_PATH` and `DJANGO_DB_ENGINE=mssql`—not used by the APK at runtime.

## Remote API base (JWT sync to backend / MSSQL)

Set the public **HTTPS base URL of the single Django backend** (MSSQL in production) so riders can call `POST /api/rider/apply-sync/` when online.

In [`android/app/build.gradle.kts`](../android/app/build.gradle.kts), set `buildConfigField` for **both** `debug` and `release` (or use `defaultConfig` only):

```kotlin
buildConfigField("String", "OPS_REMOTE_API_BASE", "\"https://ops.example.com\"")
```

Rebuild. The value is passed into Python as `OPS_REMOTE_API_BASE` and exposed to templates as `ops-api-base` / JWT sync mode (see [`docs/RIDER_PWA_REQUIREMENTS.md`](RIDER_PWA_REQUIREMENTS.md)).

## Build a debug APK

Open the `android` folder in Android Studio, let Gradle sync, then:

- **Build > Build Bundle(s) / APK(s) > Build APK(s)**, or
- From a shell (with `ANDROID_HOME` set):

```bash
cd android
./gradlew :app:assembleDebug
```

APK output: `android/app/build/outputs/apk/debug/app-debug.apk`.

## Release signing

1. Create a keystore (once), for example:

```bash
keytool -genkey -v -keystore operations-release.jks -keyalg RSA -keysize 2048 -validity 10000 -alias operations
```

2. Create `android/keystore.properties` (do **not** commit):

```properties
storePassword=...
keyPassword=...
keyAlias=operations
storeFile=C:\\path\\to\\operations-release.jks
```

3. Wire signing in `android/app/build.gradle.kts` (standard Android pattern):

```kotlin
val keystorePropertiesFile = rootProject.file("keystore.properties")
val keystoreProperties = java.util.Properties()
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(keystorePropertiesFile.inputStream())
}
android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String?
            keyPassword = keystoreProperties["keyPassword"] as String?
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String?
        }
    }
    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

4. Build:

```bash
./gradlew :app:assembleRelease
```

Release APK: `android/app/build/outputs/apk/release/app-release.apk`.

## Google Play App Bundle (AAB)

```bash
./gradlew :app:bundleRelease
```

Output: `android/app/build/outputs/bundle/release/app-release.aab`.

## Internal distribution

- **Sideload**: distribute the signed APK and enable “Install unknown apps” for your installer per OEM instructions.
- **Managed MDM**: upload the signed APK/AAB per your device policy.
- **Play Console**: use the AAB with an internal or closed testing track.

## Install on a USB-connected device

From `android/` (PowerShell):

```powershell
$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"
.\gradlew.bat :app:installDebug
```

Requires [USB debugging](https://developer.android.com/studio/run/device) enabled. The wrapper uses Gradle **8.9** ([`gradle-wrapper.properties`](../android/gradle/wrapper/gradle-wrapper.properties)); Android Gradle Plugin 8.7.x requires it.

Create [`android/local.properties`](../android/local.properties) if Android Studio has not already, with:

```properties
sdk.dir=C:/Users/YOUR_USER/AppData/Local/Android/Sdk
```

## Monitor runtime errors (logcat)

Python logs use tags **`python.stdout`** and **`python.stderr`** (see [Chaquopy docs](https://chaquo.com/chaquopy/doc/current/android.html#sys)).

```powershell
& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" logcat -v time python.stdout:V python.stderr:V AndroidRuntime:E *:S
```

Or filter by package after launching the app:

```powershell
adb logcat -v time | Select-String "operations.rider|python\.|FATAL"
```

## Troubleshooting

- **“Server Error (500)” / `ZoneInfoNotFoundError` / `No module named 'tzdata'`**: Embedded Python on Android has no system IANA timezone database. The app depends on the **`tzdata`** package ([`requirements-android.txt`](../requirements-android.txt)); [`server.py`](../android/app/src/main/python/server.py) imports it before Django starts so `TIME_ZONE = UTC` works.
- **Other 500s in the WebView**: Debug builds turn on Django **`DEBUG`** (`BuildConfig.DEBUG` → `server.py`), so you often get the **yellow error page** with a traceback. Check logcat: `adb logcat --pid=$(adb shell pidof -s com.operations.rider) python.stderr:V *:S`. Also: run `collectstatic`, SQLite (busy timeout / WAL / threaded WSGI) as documented elsewhere.
- **`JAVA_HOME` is set to an invalid directory** (e.g. literally `%JAVA_HOME%\bin`): fix the system/user `JAVA_HOME` to your JDK 17 root, or set `$env:JAVA_HOME = "C:\Program Files\Java\jdk-17"` for the session before `gradlew`. [`gradle.properties`](../android/gradle.properties) also sets `org.gradle.java.home` for Gradle itself; `gradlew.bat` still checks `JAVA_HOME` first.
- **White / unstyled UI**: run `collectstatic` (see above) so `staticfiles/` exists under `android/app/src/main/python/`.
- **Port already in use**: the app uses port `8765` by default ([`MainActivity.kt`](../android/app/src/main/java/com/operations/rider/MainActivity.kt)); change `PORT` if another tool conflicts during development.
- **Large APK**: embedded Python + Django + dependencies are expected to be tens of megabytes.
- **Django `RemovedInDjango51Warning` about `STATICFILES_STORAGE`**: informational; can be silenced later by migrating to `STORAGES` in `settings_android.py`.
