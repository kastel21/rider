/**
 * Create report: clear default zero values on focus so users do not type "05".
 * Restores zero on blur/submit only if the field was not edited.
 */
(function () {
  var ZERO_RE = /^0+(?:\.0+)?$/;
  var INPUT_SEL =
    '#report-form input[type="number"], #report-form .report-num-input';

  function isZeroPlaceholder(val) {
    return ZERO_RE.test(String(val || "").trim());
  }

  function isEmpty(val) {
    return String(val || "").trim() === "";
  }

  function matchesInput(el) {
    return el && el.matches && el.matches(INPUT_SEL);
  }

  function restoreIfPending(el) {
    var saved = el.getAttribute("data-zero-restore");
    if (saved === null) return;
    if (isEmpty(el.value)) {
      el.value = saved;
    }
    el.removeAttribute("data-zero-restore");
  }

  function bindForm(form) {
    form.addEventListener("focusin", function (e) {
      var el = e.target;
      if (!matchesInput(el)) return;
      if (!isZeroPlaceholder(el.value)) return;
      el.setAttribute("data-zero-restore", el.value);
      el.value = "";
    });

    form.addEventListener("input", function (e) {
      var el = e.target;
      if (!matchesInput(el)) return;
      el.removeAttribute("data-zero-restore");
    });

    form.addEventListener("focusout", function (e) {
      var el = e.target;
      if (!matchesInput(el)) return;
      restoreIfPending(el);
    });

    form.addEventListener(
      "submit",
      function () {
        form.querySelectorAll(INPUT_SEL).forEach(restoreIfPending);
      },
      true,
    );
  }

  function init() {
    var form = document.getElementById("report-form");
    if (!form || form.hasAttribute("data-report-pk")) return;
    bindForm(form);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
