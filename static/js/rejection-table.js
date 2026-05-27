/**
 * Scrollable rejection table: append rows and keep Django inline formset indices in sync.
 */
(function () {
  function getPrefix(tbody) {
    return tbody.getAttribute("data-rejection-prefix") || "rejections";
  }

  function totalFormsInput(prefix) {
    return document.querySelector(
      'input[name="' + prefix + '-TOTAL_FORMS"]'
    );
  }

  function maxFormsInput(prefix) {
    return document.querySelector(
      'input[name="' + prefix + '-MAX_NUM_FORMS"]'
    );
  }

  function reindexRow(tr, newIndex, prefix) {
    var nameRe = new RegExp("^" + prefix + "-\\d+-");
    var idRe = new RegExp("^id_" + prefix + "-\\d+-");

    tr.querySelectorAll("*").forEach(function (el) {
      if (el.name) {
        el.name = el.name.replace(nameRe, prefix + "-" + newIndex + "-");
      }
      if (el.id) {
        el.id = el.id.replace(idRe, "id_" + prefix + "-" + newIndex + "-");
      }
    });
    tr.querySelectorAll("label[for]").forEach(function (el) {
      var f = el.getAttribute("for");
      if (f) {
        el.setAttribute("for", f.replace(idRe, "id_" + prefix + "-" + newIndex + "-"));
      }
    });
  }

  function clearNewRow(tr) {
    tr.querySelectorAll('input[type="hidden"][name$="-id"]').forEach(function (el) {
      el.value = "";
    });
    tr.querySelectorAll('input[type="checkbox"][name$="-DELETE"]').forEach(function (el) {
      el.checked = false;
    });
    tr.querySelectorAll('input[type="number"]').forEach(function (el) {
      el.value = "0";
    });
    tr.querySelectorAll("select").forEach(function (el) {
      el.selectedIndex = 0;
    });
  }

  function refreshRowNumbers(tbody) {
    tbody.querySelectorAll("[data-rejection-row] .rejection-row-num").forEach(function (el, i) {
      el.textContent = String(i + 1);
    });
  }

  function syncAddButton(btn, prefix) {
    var totalEl = totalFormsInput(prefix);
    var maxEl = maxFormsInput(prefix);
    if (!btn || !totalEl) return;
    var total = parseInt(totalEl.value, 10) || 0;
    var maxNum = maxEl ? parseInt(maxEl.value, 10) : 1000;
    btn.disabled = total >= maxNum;
  }

  function bindAddButton() {
    var btn = document.getElementById("rejection-add-row");
    var tbody = document.querySelector("[data-rejection-tbody]");
    if (!btn || !tbody) return;

    var prefix = getPrefix(tbody);
    syncAddButton(btn, prefix);

    btn.addEventListener("click", function () {
      var totalEl = totalFormsInput(prefix);
      if (!totalEl) return;
      var maxEl = maxFormsInput(prefix);
      var total = parseInt(totalEl.value, 10) || 0;
      var maxNum = maxEl ? parseInt(maxEl.value, 10) : 1000;
      if (total >= maxNum) return;

      var rows = tbody.querySelectorAll("[data-rejection-row]");
      if (!rows.length) return;
      var templateRow = rows[rows.length - 1];
      var clone = templateRow.cloneNode(true);
      clone.querySelectorAll(".errorlist").forEach(function (n) {
        n.remove();
      });

      reindexRow(clone, total, prefix);
      clearNewRow(clone);
      tbody.appendChild(clone);
      totalEl.value = String(total + 1);
      refreshRowNumbers(tbody);

      if (typeof window.wireRejectionRow === "function") {
        window.wireRejectionRow(clone);
      }

      syncAddButton(btn, prefix);
    });
  }

  document.addEventListener("DOMContentLoaded", bindAddButton);
})();
