/**
 * Collapsible sidebar: desktop collapse + localStorage; mobile drawer + backdrop.
 */
(function () {
  var STORAGE_KEY = "sidebarCollapsed";
  var MOBILE_MAX = 900;

  function isMobile() {
    return window.matchMedia("(max-width: " + MOBILE_MAX + "px)").matches;
  }

  function applyStoredCollapse() {
    if (isMobile()) return;
    try {
      if (localStorage.getItem(STORAGE_KEY) === "1") {
        document.body.classList.add("sidebar-collapsed");
        var btn = document.getElementById("sidebar-collapse-toggle");
        if (btn) {
          btn.setAttribute("aria-expanded", "false");
          btn.setAttribute("title", "Expand sidebar");
        }
      }
    } catch (e) {
      /* ignore */
    }
  }

  function setMobileOpen(open) {
    var layout = document.getElementById("app-layout");
    var toggle = document.getElementById("sidebar-mobile-toggle");
    var backdrop = document.getElementById("app-sidebar-backdrop");
    if (!layout) return;
    layout.classList.toggle("app-layout--sidebar-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    }
    if (backdrop) {
      backdrop.hidden = !open;
      backdrop.setAttribute("aria-hidden", open ? "false" : "true");
    }
    if (open) {
      document.body.classList.add("sidebar-mobile-open");
    } else {
      document.body.classList.remove("sidebar-mobile-open");
    }
  }

  function init() {
    var collapseBtn = document.getElementById("sidebar-collapse-toggle");
    var mobileBtn = document.getElementById("sidebar-mobile-toggle");
    var backdrop = document.getElementById("app-sidebar-backdrop");

    applyStoredCollapse();
    // Reset mobile drawer state on load to avoid stale overlay/tap blocking.
    setMobileOpen(false);

    if (collapseBtn) {
      collapseBtn.addEventListener("click", function (e) {
        if (isMobile()) {
          e.preventDefault();
          return;
        }
        var collapsed = document.body.classList.toggle("sidebar-collapsed");
        collapseBtn.setAttribute("aria-expanded", collapsed ? "false" : "true");
        collapseBtn.setAttribute("title", collapsed ? "Expand sidebar" : "Collapse sidebar");
        try {
          localStorage.setItem(STORAGE_KEY, collapsed ? "1" : "0");
        } catch (e) {
          /* ignore */
        }
      });
    }

    if (mobileBtn) {
      mobileBtn.addEventListener("click", function () {
        var layout = document.getElementById("app-layout");
        var open = layout && !layout.classList.contains("app-layout--sidebar-open");
        setMobileOpen(!!open);
      });
    }

    if (backdrop) {
      backdrop.addEventListener("click", function () {
        setMobileOpen(false);
      });
    }

    window.addEventListener(
      "resize",
      function () {
        if (!isMobile()) {
          setMobileOpen(false);
        }
      },
      { passive: true }
    );
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
