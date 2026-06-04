(function () {
  "use strict";

  function initReliefPanel() {
    var checkbox = document.getElementById("id_is_relief_submission");
    var details = document.getElementById("relief-details");
    if (!checkbox || !details) {
      return;
    }

    function setVisible(show) {
      if (show) {
        details.removeAttribute("hidden");
      } else {
        details.setAttribute("hidden", "hidden");
        details.querySelectorAll("select").forEach(function (el) {
          el.selectedIndex = 0;
        });
      }
    }

    setVisible(checkbox.checked);
    checkbox.addEventListener("change", function () {
      setVisible(checkbox.checked);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initReliefPanel);
  } else {
    initReliefPanel();
  }
})();
