/**
 * Instant validation: when rejected_total > 0, reason columns must sum to total.
 */
(function () {
  var REASON_SUFFIXES = [
    "rejected_too_old",
    "rejected_patient_info_mismatch",
    "rejected_request_form_missing",
    "rejected_sample_missing",
    "rejected_other",
  ];

  function intVal(el) {
    if (!el) {
      return 0;
    }
    var n = parseInt(String(el.value || "0").trim(), 10);
    return Number.isFinite(n) && n >= 0 ? n : 0;
  }

  function rowDeleted(tr) {
    var del = tr.querySelector('input[type="checkbox"][name$="-DELETE"]');
    return del && del.checked;
  }

  function getField(tr, suffix) {
    return tr.querySelector('input[name$="-' + suffix + '"]');
  }

  function ensureLiveMsg(tr) {
    var msg = tr.querySelector("[data-rejection-live-msg]");
    if (msg) {
      return msg;
    }
    msg = document.createElement("p");
    msg.className = "rejection-live-error";
    msg.setAttribute("data-rejection-live-msg", "");
    msg.setAttribute("aria-live", "polite");
    msg.hidden = true;
    var totalCell =
      tr.querySelector('input[name$="-rejected_total"]') &&
      tr.querySelector('input[name$="-rejected_total"]').closest("td");
    if (totalCell) {
      totalCell.appendChild(msg);
    }
    return msg;
  }

  function clearRowValidity(tr) {
    ["rejected_total"].concat(REASON_SUFFIXES).forEach(function (suffix) {
      var el = getField(tr, suffix);
      if (el) {
        el.setCustomValidity("");
        el.removeAttribute("aria-invalid");
      }
    });
    var msg = tr.querySelector("[data-rejection-live-msg]");
    if (msg) {
      msg.textContent = "";
      msg.hidden = true;
    }
  }

  function validateRow(tr) {
    if (!tr.querySelector('input[name$="-rejected_total"]')) {
      return true;
    }
    if (rowDeleted(tr)) {
      clearRowValidity(tr);
      return true;
    }

    var totalEl = getField(tr, "rejected_total");
    var total = intVal(totalEl);
    var sum = 0;
    REASON_SUFFIXES.forEach(function (suffix) {
      sum += intVal(getField(tr, suffix));
    });

    var msg = ensureLiveMsg(tr);
    var bad = total > 0 && sum !== total;

    if (bad) {
      var text =
        "Sum of rejection reasons (" +
        sum +
        ") must equal total rejected (" +
        total +
        ").";
      [totalEl].concat(
        REASON_SUFFIXES.map(function (suffix) {
          return getField(tr, suffix);
        })
      ).forEach(function (el) {
        if (el) {
          el.setCustomValidity(text);
          el.setAttribute("aria-invalid", "true");
        }
      });
      if (msg) {
        msg.textContent = text;
        msg.hidden = false;
      }
      return false;
    }

    clearRowValidity(tr);
    return true;
  }

  function wireRow(tr) {
    if (tr.getAttribute("data-rejection-validation-wired") === "1") {
      return;
    }
    tr.setAttribute("data-rejection-validation-wired", "1");

    var run = function () {
      validateRow(tr);
    };

    tr.querySelectorAll(
      "input.rejection-num, input[name$='-rejected_total'], input[name$='-rejected_too_old'], input[name$='-rejected_patient_info_mismatch'], input[name$='-rejected_request_form_missing'], input[name$='-rejected_sample_missing'], input[name$='-rejected_other']"
    ).forEach(function (el) {
      el.addEventListener("input", run);
      el.addEventListener("change", run);
    });

    var del = tr.querySelector('input[type="checkbox"][name$="-DELETE"]');
    if (del) {
      del.addEventListener("change", run);
    }

    validateRow(tr);
  }

  function wireRejectionRows(root) {
    var scope = root || document;
    scope.querySelectorAll("[data-rejection-row]").forEach(wireRow);
    scope.querySelectorAll(".rejection-data-table tbody tr").forEach(function (tr) {
      if (tr.querySelector('input[name$="-rejected_total"]')) {
        wireRow(tr);
      }
    });
  }

  function initForm(form) {
    form.querySelectorAll("[data-rejection-tbody], .rejection-table-wrap").forEach(function (wrap) {
      wireRejectionRows(wrap);
    });

    form.addEventListener("submit", function (event) {
      var submitter = event.submitter || null;
      if (
        submitter &&
        submitter.name === "action" &&
        (submitter.value === "review" || submitter.value === "review_all")
      ) {
        return;
      }

      var ok = true;
      form.querySelectorAll("[data-rejection-row], .rejection-data-table tbody tr").forEach(function (tr) {
        if (tr.querySelector('input[name$="-rejected_total"]') && !validateRow(tr)) {
          ok = false;
        }
      });
      if (!ok || !form.checkValidity()) {
        event.preventDefault();
        form.reportValidity();
      }
    });
  }

  window.wireRejectionRow = wireRow;
  window.wireRejectionRows = wireRejectionRows;

  document.addEventListener("DOMContentLoaded", function () {
    document
      .querySelectorAll("form[data-report-form], form[data-bulk-report-form]")
      .forEach(initForm);
  });
})();
