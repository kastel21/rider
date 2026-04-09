/**
 * Switch PC accidents vs incomplete trips: separate panels (separate forms / formsets).
 */
(function () {
  function activate(root, key) {
    root.setAttribute("data-active-tab", key);
    var tabField = document.getElementById("pc-trans-active-tab-field");
    if (tabField) {
      tabField.value = key;
    }
    root.querySelectorAll("[data-pc-trans-tab]").forEach(function (btn) {
      var on = btn.getAttribute("data-pc-trans-tab") === key;
      btn.setAttribute("aria-selected", on ? "true" : "false");
      btn.tabIndex = on ? 0 : -1;
    });
    root.querySelectorAll("[data-pc-trans-panel]").forEach(function (panel) {
      var match = panel.getAttribute("data-pc-trans-panel") === key;
      if (match) {
        panel.removeAttribute("hidden");
      } else {
        panel.setAttribute("hidden", "hidden");
      }
    });
    root.querySelectorAll("[data-pc-trans-hint]").forEach(function (el) {
      var match = el.getAttribute("data-pc-trans-hint") === key;
      if (match) {
        el.removeAttribute("hidden");
      } else {
        el.setAttribute("hidden", "hidden");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector("[data-pc-trans-tabs]");
    if (!root) return;

    var initial = root.getAttribute("data-active-tab") || "accidents";
    activate(root, initial);

    root.querySelectorAll("[data-pc-trans-tab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-pc-trans-tab");
        if (key) activate(root, key);
      });
      btn.addEventListener("keydown", function (ev) {
        var tabs = [].slice.call(root.querySelectorAll("[data-pc-trans-tab]"));
        var i = tabs.indexOf(btn);
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") {
          ev.preventDefault();
          var next = tabs[(i + 1) % tabs.length];
          next.focus();
          activate(root, next.getAttribute("data-pc-trans-tab"));
        } else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") {
          ev.preventDefault();
          var prev = tabs[(i - 1 + tabs.length) % tabs.length];
          prev.focus();
          activate(root, prev.getAttribute("data-pc-trans-tab"));
        }
      });
    });
  });
})();
