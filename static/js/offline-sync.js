/**
 * Offline queue (IndexedDB) + sync:
 * - Session: POST /api/sync/ (CSRF cookie)
 * - JWT: POST {apiBase}/api/rider/apply-sync/ (Bearer + device_id in body)
 *
 * Per-operation ack: only removes outbox rows explicitly marked ok in results.
 */
(function () {
  const DB_NAME = "ops_rider_sync";
  const DB_VER = 2;
  const OUTBOX = "outbox";
  const DRAFTS = "drafts";

  const DEFAULT_BACKOFF_MS = 2000;
  const MAX_BACKOFF_MS = 120000;

  /** @type {{ mode: 'session'|'jwt', apiBase: string, getAccessToken: () => string|null, getRefreshToken: () => string|null }} */
  let syncConfig = {
    mode: "session",
    apiBase: "",
    getAccessToken: function () {
      return localStorage.getItem("ops_jwt_access") || "";
    },
    getRefreshToken: function () {
      return localStorage.getItem("ops_jwt_refresh") || "";
    },
  };

  function openDb() {
    return new Promise(function (resolve, reject) {
      const req = indexedDB.open(DB_NAME, DB_VER);
      req.onerror = function () {
        reject(req.error);
      };
      req.onsuccess = function () {
        resolve(req.result);
      };
      req.onupgradeneeded = function (ev) {
        const db = ev.target.result;
        if (!db.objectStoreNames.contains(OUTBOX)) {
          db.createObjectStore(OUTBOX, { keyPath: "id", autoIncrement: true });
        }
        if (!db.objectStoreNames.contains(DRAFTS)) {
          db.createObjectStore(DRAFTS, { keyPath: "client_uuid" });
        }
      };
    });
  }

  function getCookie(name) {
    const m = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
    return m ? decodeURIComponent(m[2]) : "";
  }

  function configure(opts) {
    if (!opts || typeof opts !== "object") return;
    if (opts.mode === "session" || opts.mode === "jwt") syncConfig.mode = opts.mode;
    if (typeof opts.apiBase === "string") syncConfig.apiBase = opts.apiBase.replace(/\/$/, "");
    if (typeof opts.getAccessToken === "function") syncConfig.getAccessToken = opts.getAccessToken;
    if (typeof opts.getRefreshToken === "function") syncConfig.getRefreshToken = opts.getRefreshToken;
  }

  function deviceId() {
    let id = localStorage.getItem("ops_device_id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("ops_device_id", id);
    }
    return id;
  }

  async function jwtRefreshIfNeeded() {
    const access = syncConfig.getAccessToken();
    if (access) return access;
    const refresh = syncConfig.getRefreshToken();
    if (!refresh) return "";
    const base = syncConfig.apiBase || "";
    const res = await fetch(base + "/api/rider/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refresh }),
    });
    const data = await res.json().catch(function () {
      return {};
    });
    if (!res.ok || !data.access) return "";
    try {
      localStorage.setItem("ops_jwt_access", data.access);
    } catch (e) {}
    return data.access;
  }

  async function enqueue(op) {
    const db = await openDb();
    return new Promise(function (resolve, reject) {
      const tx = db.transaction(OUTBOX, "readwrite");
      tx.objectStore(OUTBOX).add({
        op: op.op,
        idempotency_key: op.idempotency_key,
        payload: op.payload || {},
        created_at: new Date().toISOString(),
        attempts: 0,
        next_retry_at: null,
        last_error: null,
      });
      tx.oncomplete = function () {
        resolve();
      };
      tx.onerror = function () {
        reject(tx.error);
      };
    });
  }

  function resultIsAcked(res) {
    if (!res || typeof res !== "object") return false;
    if (res.ok === true) return true;
    if (res.skipped === true) return true;
    return false;
  }

  async function deleteOutboxIds(ids) {
    if (!ids.length) return;
    const db = await openDb();
    return new Promise(function (resolve, reject) {
      const tx = db.transaction(OUTBOX, "readwrite");
      const store = tx.objectStore(OUTBOX);
      ids.forEach(function (id) {
        store.delete(id);
      });
      tx.oncomplete = function () {
        resolve();
      };
      tx.onerror = function () {
        reject(tx.error);
      };
    });
  }

  async function updateOutboxRetry(row, errMsg) {
    const db = await openDb();
    const attempts = (row.attempts || 0) + 1;
    const backoff = Math.min(MAX_BACKOFF_MS, DEFAULT_BACKOFF_MS * Math.pow(2, Math.min(attempts, 6)));
    const next = new Date(Date.now() + backoff).toISOString();
    return new Promise(function (resolve, reject) {
      const tx = db.transaction(OUTBOX, "readwrite");
      const store = tx.objectStore(OUTBOX);
      const u = Object.assign({}, row, {
        attempts: attempts,
        next_retry_at: next,
        last_error: String(errMsg || "").slice(0, 500),
      });
      store.put(u);
      tx.oncomplete = function () {
        resolve();
      };
      tx.onerror = function () {
        reject(tx.error);
      };
    });
  }

  async function getOutboxRowsEligible() {
    const db = await openDb();
    const rows = await new Promise(function (resolve, reject) {
      const tx = db.transaction(OUTBOX, "readonly");
      const req = tx.objectStore(OUTBOX).getAll();
      req.onsuccess = function () {
        resolve(req.result || []);
      };
      req.onerror = function () {
        reject(req.error);
      };
    });
    const now = Date.now();
    return rows.filter(function (r) {
      if (!r.next_retry_at) return true;
      const t = Date.parse(r.next_retry_at);
      return !Number.isFinite(t) || t <= now;
    });
  }

  async function countPendingOutbox() {
    const db = await openDb();
    const all = await new Promise(function (resolve, reject) {
      const tx = db.transaction(OUTBOX, "readonly");
      const req = tx.objectStore(OUTBOX).getAll();
      req.onsuccess = function () {
        resolve(req.result || []);
      };
      req.onerror = function () {
        reject(req.error);
      };
    });
    return all.length;
  }

  async function syncSessionBatch(rows) {
    const operations = rows.map(function (r) {
      return {
        op: r.op,
        idempotency_key: r.idempotency_key,
        payload: r.payload,
      };
    });
    const csrftoken = getCookie("csrftoken");
    const res = await fetch("/api/sync/", {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ operations: operations }),
    });
    const data = await res.json().catch(function () {
      return {};
    });
    return { res: res, data: data, rows: rows, operations: operations };
  }

  async function syncJwtBatch(rows) {
    let token = syncConfig.getAccessToken() || (await jwtRefreshIfNeeded());
    if (!token) {
      throw new Error("JWT access token missing; set ops_jwt_access or configure getAccessToken");
    }
    const operations = rows.map(function (r) {
      return {
        op: r.op,
        idempotency_key: r.idempotency_key,
        payload: r.payload,
      };
    });
    const base = syncConfig.apiBase || "";
    const url = base + "/api/rider/apply-sync/";
    const body = {
      device_id: deviceId(),
      operations: operations,
    };
    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
      body: JSON.stringify(body),
    });
    const data = await res.json().catch(function () {
      return {};
    });
    return { res: res, data: data, rows: rows, operations: operations };
  }

  async function applySyncResponse(bundle) {
    const res = bundle.res;
    const data = bundle.data;
    const rows = bundle.rows;

    if (!res.ok) {
      const msg = (data && data.error) || res.statusText || String(res.status);
      for (let i = 0; i < rows.length; i++) {
        await updateOutboxRetry(rows[i], msg);
      }
      return { ok: false, error: msg, partial: 0 };
    }

    if (data && data.ok === false && !Array.isArray(data.results)) {
      const msg = data.error || "sync failed";
      for (let i = 0; i < rows.length; i++) {
        await updateOutboxRetry(rows[i], msg);
      }
      return { ok: false, error: msg, partial: 0 };
    }

    const results = data.results;
    if (!Array.isArray(results)) {
      const msg = "invalid response: missing results[]";
      for (let i = 0; i < rows.length; i++) {
        await updateOutboxRetry(rows[i], msg);
      }
      return { ok: false, error: msg, partial: 0 };
    }

    const toDelete = [];
    const failed = [];

    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      const idx = typeof r.index === "number" ? r.index : i;
      const row = rows[idx];
      if (!row) continue;
      if (resultIsAcked(r)) {
        toDelete.push(row.id);
      } else {
        failed.push({ row: row, err: (r && r.error) || "not acknowledged" });
      }
    }

    await deleteOutboxIds(toDelete);

    for (let j = 0; j < failed.length; j++) {
      await updateOutboxRetry(failed[j].row, failed[j].err);
    }

    const synced = toDelete.length;
    if (synced === 0 && rows.length > 0 && failed.length === 0) {
      const msg = "no rows acked";
      for (let k = 0; k < rows.length; k++) {
        await updateOutboxRetry(rows[k], msg);
      }
      return { ok: false, error: msg, partial: 0 };
    }

    return {
      ok: failed.length === 0,
      synced: synced,
      failed: failed.length,
      error: failed.length ? failed[0].err : null,
    };
  }

  async function syncNow() {
    const rows = await getOutboxRowsEligible();
    if (!rows.length) {
      setStatus("online · nothing to sync");
      return { ok: true, synced: 0 };
    }

    if (!navigator.onLine) {
      setStatus("offline · " + rows.length + " pending");
      return { ok: false, error: "offline" };
    }

    setStatus("syncing…");
    let bundle;
    try {
      if (syncConfig.mode === "jwt") {
        bundle = await syncJwtBatch(rows);
      } else {
        bundle = await syncSessionBatch(rows);
      }
    } catch (e) {
      const msg = e && e.message ? e.message : String(e);
      for (let i = 0; i < rows.length; i++) {
        await updateOutboxRetry(rows[i], msg);
      }
      setStatus("error: " + msg);
      return { ok: false, error: msg };
    }

    const out = await applySyncResponse(bundle);
    if (out.ok && out.synced > 0) {
      setStatus("synced " + out.synced);
    } else if (out.partial !== undefined && out.synced > 0) {
      setStatus("partial: " + out.synced + " ok, some failed");
    } else if (out.error) {
      setStatus("pending · " + (rows.length - (out.synced || 0)) + " (" + out.error + ")");
    } else {
      setStatus("online · pending " + rows.length);
    }
    refreshPendingUi();
    return out;
  }

  /** @deprecated use syncNow */
  async function drainOutbox() {
    return syncNow();
  }

  function setStatus(text) {
    const el = document.getElementById("sync-state");
    if (el) el.textContent = text;
  }

  async function registerSw() {
    if (!("serviceWorker" in navigator)) return;
    try {
      await navigator.serviceWorker.register("/service-worker.js", {
        scope: "/",
      });
    } catch (e) {
      console.warn("SW register failed", e);
    }
  }

  async function registerDeviceOnce() {
    let id = deviceId();
    const csrftoken = getCookie("csrftoken");
    try {
      await fetch("/api/register-device/", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
          device_id: id,
          platform: navigator.userAgentData ? "web" : "browser",
          user_agent: navigator.userAgent || "",
        }),
      });
    } catch (e) {
      console.warn("register-device failed", e);
    }
  }

  async function saveDraft(clientUuid, payload) {
    if (!clientUuid) return;
    const db = await openDb();
    return new Promise(function (resolve, reject) {
      const tx = db.transaction(DRAFTS, "readwrite");
      tx.objectStore(DRAFTS).put({
        client_uuid: clientUuid,
        payload: payload,
        saved_at: new Date().toISOString(),
      });
      tx.oncomplete = function () {
        resolve();
      };
      tx.onerror = function () {
        reject(tx.error);
      };
    });
  }

  function serializeReportForm(form) {
    const fd = new FormData(form);
    const entries = {};
    fd.forEach(function (v, k) {
      if (entries[k] !== undefined) {
        if (!Array.isArray(entries[k])) entries[k] = [entries[k]];
        entries[k].push(v);
      } else {
        entries[k] = v;
      }
    });
    const ds = (form.getAttribute("data-week-start") || "").trim().slice(0, 10);
    const weekRaw = entries.week_start || entries.week || "";
    let weekStart = ds;
    if (!weekStart && typeof weekRaw === "string") weekStart = weekRaw.slice(0, 10);
    const idemInput = form.querySelector('input[name="client_uuid"], #id_client_uuid');
    const idem = (idemInput && idemInput.value) || "";
    return {
      week_start: weekStart,
      title: (entries.title || "").toString(),
      notes: (entries.notes || "").toString(),
      samples_collected: parseInt(entries.samples_collected, 10) || 0,
      extra_data: {
        offline_form_snapshot: entries,
      },
      trip_rows: [],
      rejections: [],
    };
  }

  function bindReportFormOffline(form) {
    if (!form || form.getAttribute("data-offline-bound")) return;
    form.setAttribute("data-offline-bound", "1");
    form.addEventListener(
      "submit",
      function (ev) {
        if (navigator.onLine) return;
        ev.preventDefault();
        const payload = serializeReportForm(form);
        const idemInput = form.querySelector('input[name="client_uuid"], #id_client_uuid');
        const idem = (idemInput && idemInput.value) || crypto.randomUUID();
        if (idemInput && !idemInput.value) idemInput.value = idem;
        queueReportUpsert(payload, idem)
          .then(function () {
            return saveDraft(idem, payload);
          })
          .then(function () {
            setStatus("offline · queued (not synced)");
            refreshPendingUi();
            alert(
              "You appear to be offline. A copy was queued to sync when you are back online. Keep this tab and try Sync now.",
            );
          })
          .catch(function (e) {
            console.warn(e);
            alert("Could not save offline queue: " + (e && e.message));
          });
      },
      true,
    );
  }

  async function refreshPendingUi() {
    const n = await countPendingOutbox();
    const badge = document.getElementById("sync-pending-count");
    if (badge) badge.textContent = n ? String(n) : "";
    const listState = document.getElementById("sync-state");
    if (listState && document.querySelector("[data-sync-root]")) {
      if (!navigator.onLine) {
        listState.textContent = "offline · " + n + " pending";
      } else if (n > 0) {
        listState.textContent = "online · " + n + " pending";
      }
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    registerSw();
    const meta = document.querySelector("meta[name='ops-sync-mode']");
    if (meta && meta.getAttribute("content") === "jwt") {
      configure({ mode: "jwt" });
    }
    const apiMeta = document.querySelector("meta[name='ops-api-base']");
    if (apiMeta && apiMeta.getAttribute("content")) {
      configure({ apiBase: apiMeta.getAttribute("content") });
    }

    const root = document.querySelector("[data-sync-root]");
    if (root) {
      registerDeviceOnce();
      setStatus(navigator.onLine ? "online" : "offline");
      const btn = document.getElementById("sync-now-btn");
      if (btn) {
        btn.addEventListener("click", function () {
          syncNow().catch(function (e) {
            console.warn(e);
          });
        });
      }
      window.addEventListener("online", function () {
        setStatus("online");
        syncNow().catch(function (e) {
          console.warn(e);
        });
      });
      window.addEventListener("offline", function () {
        setStatus("offline");
      });
      syncNow().catch(function () {});
      refreshPendingUi();
    }

    const reportForm = document.getElementById("report-form");
    if (reportForm) bindReportFormOffline(reportForm);
  });

  function queueReportUpsert(payload, idempotencyKey) {
    const key = idempotencyKey || crypto.randomUUID();
    return enqueue({
      op: "upsert_report",
      idempotency_key: key,
      payload: payload,
    });
  }

  window.OpsOffline = {
    configure: configure,
    enqueue: enqueue,
    syncNow: syncNow,
    drainOutbox: drainOutbox,
    countPendingOutbox: countPendingOutbox,
    queueReportUpsert: queueReportUpsert,
    saveDraft: saveDraft,
    serializeReportForm: serializeReportForm,
    bindReportFormOffline: bindReportFormOffline,
    refreshPendingUi: refreshPendingUi,
    deviceId: deviceId,
  };
})();
