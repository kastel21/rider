/* eslint-disable no-restricted-globals */
const CACHE = "ops-rider-v4";
const PRECACHE = [
  "/static/css/standalone-shell.css",
  "/static/css/dashboard-record.css",
  "/static/css/app-chrome.css",
  "/static/js/offline-sync.js",
  "/static/js/sidebar.js",
  "/static/js/report-trip-routing.js",
  "/static/js/report-fuel-validation.js",
  "/static/js/driver-trip-tabs.js",
  "/static/js/rejection-table.js",
  "/static/js/rider-home-charts.js",
  "/static/js/pc-accidents-incomplete-tabs.js",
  "/static/js/pc-trans-stats-add-row.js",
  "/static/js/vendor/chart.umd.min.js",
  "/static/manifest.json",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE).then((cache) => cache.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((key) => key !== CACHE).map((key) => caches.delete(key)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  const isStaticAsset = url.pathname.startsWith("/static/");

  if (isStaticAsset) {
    event.respondWith(
      caches.match(req).then((cached) => {
        if (cached) return cached;
        return fetch(req).then((response) => {
          // Cache fetched static files so future offline visits keep styling/scripts.
          if (response && response.ok) {
            const copy = response.clone();
            caches.open(CACHE).then((cache) => cache.put(req, copy));
          }
          return response;
        });
      })
    );
    return;
  }

  event.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).catch(() => caches.match("/reports/"));
    })
  );
});
