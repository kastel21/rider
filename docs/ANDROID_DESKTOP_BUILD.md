# Android (Capacitor) and desktop (Electron)

## Prerequisites

- **Node.js** 18+ and npm (for Capacitor CLI and Electron).
- **Android Studio** with SDKs for `npx cap open android` / Gradle builds.
- Django backend reachable over HTTPS in production (session cookies + CSRF).

## Environment

| Variable | Purpose |
|----------|---------|
| `DJANGO_APP_URL` | Electron [`electron/main.js`](../electron/main.js) loads this URL (default `http://127.0.0.1:8000/`). |
| `CAPACITOR_SERVER_URL` | **Document-only:** set the same URL inside [`capacitor.config.json`](../capacitor.config.json) → `server.url` so the WebView loads your deployed API. Do not commit secrets. |

### Android emulator vs device

- **Emulator → host Django:** `server.url` can be `http://10.0.2.2:8000` (already set in repo config for local dev).
- **Physical device:** use your PC’s LAN IP, e.g. `http://192.168.1.10:8000`, and allow the host in `DJANGO_ALLOWED_HOSTS`.

Update `server.url`, then:

```bash
npm run android:sync
npm run android:open
```

## npm scripts

| Script | Action |
|--------|--------|
| `npm run android:sync` | `cap sync android` — copy web assets and config |
| `npm run android:open` | Open Android Studio |
| `npm run android:install:debug` | `cap run android` — debug install |
| `npm run android:bundle` | Windows: `gradlew.bat bundleRelease` (run from repo root; requires Android project) |
| `npm run desktop:start` | Launch Electron against `DJANGO_APP_URL` |
| `npm run desktop:dist` | Package with electron-builder (see [`package.json`](../package.json) `build`) |

## Cleartext HTTP

Local dev may use `cleartext: true` in Capacitor config. **Production** should use HTTPS and turn cleartext off.
