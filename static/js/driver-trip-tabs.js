/**
 * Toggle driver weekly report trip stacks (both formsets stay in the DOM for one POST).
 */
(function () {
  function activate(root, key) {
    var tabs = root.querySelectorAll("[data-driver-tab]");
    var panels = root.querySelectorAll("[data-driver-tab-panel]");
    tabs.forEach(function (btn) {
      var on = btn.getAttribute("data-driver-tab") === key;
      btn.setAttribute("aria-selected", on ? "true" : "false");
      btn.tabIndex = on ? 0 : -1;
    });
    panels.forEach(function (panel) {
      var match = panel.getAttribute("data-driver-tab-panel") === key;
      if (match) {
        panel.removeAttribute("hidden");
      } else {
        panel.setAttribute("hidden", "hidden");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var root = document.querySelector("[data-driver-trip-tabs]");
    if (!root) return;

    root.querySelectorAll("[data-driver-tab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-driver-tab");
        if (key) activate(root, key);
      });
      btn.addEventListener("keydown", function (ev) {
        var tabs = [].slice.call(root.querySelectorAll("[data-driver-tab]"));
        var i = tabs.indexOf(btn);
        if (ev.key === "ArrowRight" || ev.key === "ArrowDown") {
          ev.preventDefault();
          var next = tabs[(i + 1) % tabs.length];
          next.focus();
          activate(root, next.getAttribute("data-driver-tab"));
        } else if (ev.key === "ArrowLeft" || ev.key === "ArrowUp") {
          ev.preventDefault();
          var prev = tabs[(i - 1 + tabs.length) % tabs.length];
          prev.focus();
          activate(root, prev.getAttribute("data-driver-tab"));
        }
      });
    });
  });
})();
