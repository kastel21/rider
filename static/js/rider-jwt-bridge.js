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

  document.addEventListener("DOMContentLoaded", function () {
    var el = document.getElementById("ops-jwt-bootstrap");
    if (!el || !el.textContent) return;
    try {
      var tokens = JSON.parse(el.textContent);
      storeTokens(tokens);
      el.textContent = "";
    } catch (e) {
      console.warn("ops jwt bootstrap parse failed", e);
    }
  });

  window.OpsJwtBridge = { storeTokens: storeTokens };
})();
