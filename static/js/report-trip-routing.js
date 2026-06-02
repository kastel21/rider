/**
 * Populate From/To facility dropdowns from report_facilities_ajax when route_kind changes.
 */
(function () {
  var RELAY_PURPOSE = "relay";
  var RELAY_ROUTE_KIND = "hub_to_hub";

  function facilitiesUrl() {
    var root = document.getElementById("report-form");
    return root && root.getAttribute("data-facilities-url");
  }

  function populateSelect(select, facilities, selectedId) {
    if (!select) return;
    var cur =
      selectedId != null && selectedId !== ""
        ? String(selectedId)
        : select.value || "";
    select.innerHTML = "";
    var blank = document.createElement("option");
    blank.value = "";
    blank.textContent = "—";
    select.appendChild(blank);
    (facilities || []).forEach(function (f) {
      var o = document.createElement("option");
      o.value = String(f.id);
      o.textContent = f.name + " (" + f.kind + ")";
      if (String(f.id) === cur) o.selected = true;
      select.appendChild(o);
    });
    if (cur && ![].some.call(select.options, function (opt) { return opt.value === cur; })) {
      var orphan = document.createElement("option");
      orphan.value = cur;
      orphan.textContent = "#" + cur + " (not in list — pick route)";
      orphan.selected = true;
      select.appendChild(orphan);
    }
  }

  function setEndpointsEnabled(card, enabled) {
    var fromSel = card.querySelector(".trip-origin-facility");
    var toSel = card.querySelector(".trip-destination-facility");
    if (fromSel) fromSel.disabled = !enabled;
    if (toSel) toSel.disabled = !enabled;
  }

  function loadSlot(card, routeKind, slot, selectedId) {
    var base = facilitiesUrl();
    if (!base || !routeKind) return Promise.resolve();

    var url = new URL(base, window.location.origin);
    url.searchParams.set("route_kind", routeKind);
    url.searchParams.set("slot", slot);

    return fetch(url.toString(), { credentials: "same-origin" })
      .then(function (r) {
        return r.json();
      })
      .then(function (data) {
        var list = (data && data.facilities) || [];
        var sel =
          slot === "from"
            ? card.querySelector(".trip-origin-facility")
            : card.querySelector(".trip-destination-facility");
        populateSelect(sel, list, selectedId);
      })
      .catch(function () {
        /* keep existing options */
      });
  }

  function refreshCard(card) {
    enforceRelayRoute(card);
    var rkInput = card.querySelector(".trip-route-kind");
    var rk = rkInput ? rkInput.value : "";
    var fromSel = card.querySelector(".trip-origin-facility");
    var toSel = card.querySelector(".trip-destination-facility");
    var fromId = fromSel ? fromSel.value : "";
    var toId = toSel ? toSel.value : "";

    if (!rk) {
      setEndpointsEnabled(card, false);
      return;
    }
    setEndpointsEnabled(card, true);
    return Promise.all([
      loadSlot(card, rk, "from", fromId),
      loadSlot(card, rk, "to", toId),
    ]);
  }

  function enforceRelayRoute(card) {
    var purposeInput = card.querySelector(".trip-visit-purpose");
    var routeInput = card.querySelector(".trip-route-kind");
    if (!purposeInput || !routeInput) return;
    if (purposeInput.value === RELAY_PURPOSE) {
      routeInput.value = RELAY_ROUTE_KIND;
      routeInput.disabled = true;
      routeInput.setAttribute("aria-readonly", "true");
      return;
    }
    routeInput.disabled = false;
    routeInput.removeAttribute("aria-readonly");
  }

  function bindCard(card) {
    var rkInput = card.querySelector(".trip-route-kind");
    var purposeInput = card.querySelector(".trip-visit-purpose");
    if (!rkInput || !purposeInput) return;
    rkInput.addEventListener("change", function () {
      refreshCard(card);
    });
    purposeInput.addEventListener("change", function () {
      refreshCard(card);
    });
    if (rkInput.value) {
      refreshCard(card);
    } else {
      setEndpointsEnabled(card, false);
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!facilitiesUrl()) return;
    document.querySelectorAll("[data-trip-routing-card]").forEach(bindCard);
  });
})();
