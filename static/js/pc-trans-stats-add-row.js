/**
 * Append rows to a PC district weekly transport formset (accidents or incomplete).
 * Each tab has its own form; Add row only affects that form's tbody and TOTAL_FORMS.
 */
(function () {
  function totalFormsInput(prefix) {
    return document.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
  }

  function maxFormsInput(prefix) {
    return document.querySelector('input[name="' + prefix + '-MAX_NUM_FORMS"]');
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
    tr.querySelectorAll('input[type="number"]').forEach(function (el) {
      el.value = "0";
    });
    tr.querySelectorAll("select").forEach(function (el) {
      el.selectedIndex = 0;
    });
    tr.querySelectorAll("textarea").forEach(function (el) {
      el.value = "";
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

  function bindOneAddButton(btn) {
    var form = btn.closest("form");
    if (!form) return;
    var tbody = form.querySelector("[data-pc-trans-tbody]");
    if (!tbody) return;
    var prefix = tbody.getAttribute("data-pc-trans-prefix");
    if (!prefix) return;

    syncAddButton(btn, prefix);

    btn.addEventListener("click", function () {
      var totalEl = totalFormsInput(prefix);
      if (!totalEl) return;
      var maxEl = maxFormsInput(prefix);
      var total = parseInt(totalEl.value, 10) || 0;
      var maxNum = maxEl ? parseInt(maxEl.value, 10) : 1000;
      if (total >= maxNum) return;

      var rows = tbody.querySelectorAll("[data-pc-trans-row]");
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

      syncAddButton(btn, prefix);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-pc-trans-add-row]").forEach(bindOneAddButton);
  });
})();
