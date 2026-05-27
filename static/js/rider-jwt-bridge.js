/**
 * Store remote JWT tokens in localStorage for OpsOffline JWT sync mode.
 */
(function () {
  function storeTokens(tokens) {
    if (!tokens || !tokens.access) return;
    try {
      localStorage.setItem("ops_jwt_access", tokens.access);
      if (tokens.refresh) {
        localStorage.setItem("ops_jwt_refresh", tokens.refresh);
      }
    } catch (e) {
      console.warn("ops jwt store failed", e);
    }
    if (window.OpsOffline && typeof window.OpsOffline.configure === "function") {
      var apiMeta = document.querySelector("meta[name='ops-api-base']");
      var modeMeta = document.querySelector("meta[name='ops-sync-mode']");
      if (modeMeta && modeMeta.getAttribute("content") === "jwt") {
        window.OpsOffline.configure({
          mode: "jwt",
          apiBase: apiMeta ? apiMeta.getAttribute("content") || "" : "",
        });
      }
    }
  }

  function ensureJwtFromServer() {
    var modeMeta = document.querySelector("meta[name='ops-sync-mode']");
    if (!modeMeta || modeMeta.getAttribute("content") !== "jwt") {
      return Promise.resolve();
    }
    try {
      if (localStorage.getItem("ops_jwt_access")) {
        return Promise.resolve();
      }
    } catch (e) {
      return Promise.resolve();
    }
    return fetch("/api/rider/jwt-bootstrap/", {
      credentials: "same-origin",
      headers: { Accept: "application/json" },
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (out) {
        if (out.ok && out.data && out.data.access) {
          storeTokens(out.data);
        }
      })
      .catch(function (e) {
        console.warn("ops jwt bootstrap fetch failed", e);
      });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById("ops-jwt-bootstrap");
    if (el && el.textContent) {
      try {
        storeTokens(JSON.parse(el.textContent));
        el.textContent = "";
      } catch (e) {
        console.warn("ops jwt bootstrap parse failed", e);
      }
    }
    ensureJwtFromServer();
  });

  window.OpsJwtBridge = { storeTokens: storeTokens, ensureJwtFromServer: ensureJwtFromServer };
})();
