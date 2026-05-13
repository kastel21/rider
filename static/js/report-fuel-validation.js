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

  function wirePcWeekStrip(wrap, form) {
    var allocated =
      wrap.querySelector("[data-pc-fuel-allocated]") || form.querySelector("#pc_fuel_allocated_total");
    var used =
      wrap.querySelector("[data-pc-fuel-used]") || form.querySelector("#pc_fuel_used_total");
    var distance =
      wrap.querySelector("[data-pc-distance-travelled]") || form.querySelector("#pc_distance_travelled_total");
    var msg = wrap.querySelector("[data-pc-fuel-live-msg]");
    if (!allocated || !used || !msg) {
      return;
    }

    function validate() {
      var alloc = parseAmount(allocated.value);
      var u = parseAmount(used.value);
      var bad = u > alloc;
      var nonNegativeBad = alloc < 0 || u < 0;
      var distBad = false;
      if (distance) {
        distBad = parseAmount(distance.value) < 0;
      }
      if (bad) {
        var text = "Fuel used cannot exceed fuel allocated.";
        used.setCustomValidity(text);
        msg.textContent = text;
        msg.hidden = false;
        used.setAttribute("aria-invalid", "true");
      } else if (nonNegativeBad) {
        var nonNegativeText = "Fuel totals must be zero or positive.";
        used.setCustomValidity(nonNegativeText);
        msg.textContent = nonNegativeText;
        msg.hidden = false;
        used.setAttribute("aria-invalid", "true");
      } else {
        used.setCustomValidity("");
        msg.textContent = "";
        msg.hidden = true;
        used.removeAttribute("aria-invalid");
      }
      if (distance) {
        if (distBad) {
          distance.setCustomValidity("Distance travelled must be zero or positive.");
          distance.setAttribute("aria-invalid", "true");
        } else {
          distance.setCustomValidity("");
          distance.removeAttribute("aria-invalid");
        }
      }
    }

    allocated.addEventListener("input", validate);
    used.addEventListener("input", validate);
    if (distance) {
      distance.addEventListener("input", validate);
      distance.addEventListener("change", validate);
    }
    allocated.addEventListener("change", validate);
    used.addEventListener("change", validate);
    validate();
  }

  function textValue(el) {
    return (el && el.value ? String(el.value).trim() : "");
  }

  function intValue(el) {
    return parseInt(textValue(el) || "0", 10) || 0;
  }

  function hasTripData(card) {
    var names = [
      "vl_blood_plasma",
      "vl_dbs",
      "eid_blood",
      "eid_dbs",
      "sputum",
      "sputum_culture_dr",
      "hpv",
      "results_vl_blood_plasma",
      "results_vl_dbs",
      "results_eid_blood",
      "results_eid_dbs",
      "results_sputum",
      "results_sputum_culture_dr",
      "results_hpv"
    ];
    for (var i = 0; i < names.length; i += 1) {
      var input = card.querySelector('input[name$="-' + names[i] + '"]');
      if (intValue(input) > 0) {
        return true;
      }
    }
    var txtNames = ["specimens_other_specify", "results_other_specify"];
    for (var j = 0; j < txtNames.length; j += 1) {
      var txt = card.querySelector('input[name$="-' + txtNames[j] + '"]');
      if (textValue(txt)) {
        return true;
      }
    }
    return false;
  }

  function validateTripCard(card) {
    var requiresRoute = hasTripData(card);
    var map = [
      ["visit_purpose", "Visit purpose is required for rows with data."],
      ["route_kind", "Route type is required for rows with data."],
      ["origin_facility", "From facility is required for rows with data."],
      ["destination_facility", "To facility is required for rows with data."]
    ];

    for (var i = 0; i < map.length; i += 1) {
      var field = card.querySelector('[name$="-' + map[i][0] + '"]');
      if (!field) {
        continue;
      }
      if (requiresRoute && !textValue(field)) {
        field.setCustomValidity(map[i][1]);
        field.setAttribute("aria-invalid", "true");
      } else {
        field.setCustomValidity("");
        field.removeAttribute("aria-invalid");
      }
    }

    card.querySelectorAll('input[type="number"]').forEach(function (el) {
      var raw = textValue(el);
      if (!raw) {
        el.setCustomValidity("");
        el.removeAttribute("aria-invalid");
        return;
      }
      if (parseFloat(raw) < 0) {
        el.setCustomValidity("Value must be zero or positive.");
        el.setAttribute("aria-invalid", "true");
      } else {
        el.setCustomValidity("");
        el.removeAttribute("aria-invalid");
      }
    });
  }

  function wireTripCardValidation(form) {
    var cards = form.querySelectorAll("[data-trip-routing-card]");
    if (!cards.length) {
      return;
    }
    cards.forEach(function (card) {
      card.querySelectorAll("input, select, textarea").forEach(function (el) {
        el.addEventListener("input", function () {
          validateTripCard(card);
        });
        el.addEventListener("change", function () {
          validateTripCard(card);
        });
      });
      validateTripCard(card);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var forms = Array.from(
      document.querySelectorAll("form[data-report-form], form[data-bulk-report-form]")
    );
    forms.forEach(function (form) {
      form.querySelectorAll(".fuel-strip").forEach(wireStrip);
      form.querySelectorAll("[data-pc-week-fuel]").forEach(function (wrap) {
        wirePcWeekStrip(wrap, form);
      });
      wireTripCardValidation(form);
      form.addEventListener("submit", function (event) {
        var submitter = event.submitter || null;
        if (
          submitter &&
          submitter.name === "action" &&
          (submitter.value === "review" || submitter.value === "review_all")
        ) {
          return;
        }
        form.querySelectorAll("[data-trip-routing-card]").forEach(validateTripCard);
        if (!form.checkValidity()) {
          event.preventDefault();
          form.reportValidity();
        }
      });
    });
  });
})();
