/**
 * Instant validation: fuel used cannot exceed fuel allocated (per trip row).
 */
(function () {
  function parseAmount(val) {
    if (val == null || String(val).trim() === "") {
      return 0;
    }
    var n = parseFloat(String(val).replace(/,/g, "."));
    return Number.isFinite(n) ? n : 0;
  }

  function wireStrip(strip) {
    var allocated = strip.querySelector('input[name$="-fuel_allocated"]');
    var used = strip.querySelector('input[name$="-fuel_used"]');
    var msg = strip.querySelector("[data-fuel-live-msg]");
    if (!allocated || !used || !msg) {
      return;
    }

    function validate() {
      var alloc = parseAmount(allocated.value);
      var u = parseAmount(used.value);
      var bad = u > alloc;
      if (bad) {
        var text = "Fuel used cannot exceed fuel allocated.";
        used.setCustomValidity(text);
        msg.textContent = text;
        msg.hidden = false;
        used.setAttribute("aria-invalid", "true");
      } else {
        used.setCustomValidity("");
        msg.textContent = "";
        msg.hidden = true;
        used.removeAttribute("aria-invalid");
      }
    }

    allocated.addEventListener("input", validate);
    used.addEventListener("input", validate);
    allocated.addEventListener("change", validate);
    used.addEventListener("change", validate);
    validate();
  }

  function wirePcWeekStrip(form) {
    var wrap = form.querySelector("[data-pc-week-fuel]");
    if (!wrap) {
      return;
    }
    var allocated = form.querySelector("#pc_fuel_allocated_total");
    var used = form.querySelector("#pc_fuel_used_total");
    var msg = wrap.querySelector("[data-pc-fuel-live-msg]");
    if (!allocated || !used || !msg) {
      return;
    }

    function validate() {
      var alloc = parseAmount(allocated.value);
      var u = parseAmount(used.value);
      var bad = u > alloc;
      if (bad) {
        var text = "Fuel used cannot exceed fuel allocated.";
        used.setCustomValidity(text);
        msg.textContent = text;
        msg.hidden = false;
        used.setAttribute("aria-invalid", "true");
      } else {
        used.setCustomValidity("");
        msg.textContent = "";
        msg.hidden = true;
        used.removeAttribute("aria-invalid");
      }
    }

    allocated.addEventListener("input", validate);
    used.addEventListener("input", validate);
    allocated.addEventListener("change", validate);
    used.addEventListener("change", validate);
    validate();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("report-form");
    if (!form) {
      return;
    }
    form.querySelectorAll(".fuel-strip").forEach(wireStrip);
    wirePcWeekStrip(form);
  });
})();
