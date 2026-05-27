/**
 * Save feedback + reliable redirect to rider home (/reports/) after Save and submit.
 * WebView often ignores POST redirect responses; we POST via fetch and follow Location.
 */
(function () {
  var TOAST_ID = "ops-save-toast";
  var SESSION_KEY = "ops_save_pending_ui";
  var RIDER_HOME = "/reports/";

  function showToast(text, kind, durationMs) {
    if (!text) return;
    var el = document.getElementById(TOAST_ID);
    if (!el) {
      el = document.createElement("div");
      el.id = TOAST_ID;
      el.setAttribute("role", "status");
      el.setAttribute("aria-live", "polite");
      document.body.appendChild(el);
    }
    el.className = "ops-save-toast ops-save-toast--" + (kind || "success");
    el.textContent = text;
    el.hidden = false;
    clearTimeout(showToast._timer);
    var ms = durationMs || (kind === "pending" ? 120000 : 10000);
    showToast._timer = setTimeout(function () {
      el.hidden = true;
    }, ms);
  }

  function stashSaveIntent(action) {
    try {
      sessionStorage.setItem(
        SESSION_KEY,
        JSON.stringify({ at: Date.now(), action: action || "submit" }),
      );
    } catch (e) {}
  }

  function clearStaleSaveIntent() {
    try {
      sessionStorage.removeItem(SESSION_KEY);
    } catch (e) {}
  }

  function messageFromPage() {
    var nodes = document.querySelectorAll(".messages .msg-success, .messages .msg-info");
    if (nodes.length) return nodes[0].textContent.trim();
    return "";
  }

  function messageFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var ok = params.get("save_ok");
    if (ok === "submitted") {
      return "Report saved on this device. Cloud sync runs when you tap Sync now (online).";
    }
    if (ok === "review") {
      return "Report submitted for PC review.";
    }
    if (ok === "1" || params.get("draft_cleared") === "1") {
      return "Report saved on this device.";
    }
    return "";
  }

  function isReportFormPage() {
    return /\/reports\/create\/?$/.test(window.location.pathname) ||
      /\/reports\/\d+\/edit\/?$/.test(window.location.pathname);
  }

  function isRiderHomePage() {
    return window.location.pathname === "/reports/" || window.location.pathname === "/reports";
  }

  function messageFromSession() {
    if (!isRiderHomePage()) {
      clearStaleSaveIntent();
      return "";
    }
    try {
      var raw = sessionStorage.getItem(SESSION_KEY);
      if (!raw) return "";
      var o = JSON.parse(raw);
      if (!o || Date.now() - (o.at || 0) > 120000) {
        clearStaleSaveIntent();
        return "";
      }
      clearStaleSaveIntent();
      if (o.action === "review") {
        return "Report submitted for PC review.";
      }
      return "Report saved on this device. Cloud sync runs when you tap Sync now (online).";
    } catch (e) {
      return "";
    }
  }

  function collectValidationErrors() {
    var parts = [];
    document.querySelectorAll(".messages .msg-error").forEach(function (el) {
      var t = el.textContent.trim();
      if (t) parts.push(t);
    });
    document.querySelectorAll(".errorlist li").forEach(function (el) {
      var t = el.textContent.trim();
      if (t) parts.push(t);
    });
    if (document.getElementById("ops-form-save-failed")) {
      parts.push("Check the form fields below.");
    }
    return parts;
  }

  function showPendingSaveFeedback() {
    var urlMsg = messageFromUrl();
    var pageMsg = messageFromPage();
    var errs = collectValidationErrors();
    var saveFailedMarker = document.getElementById("ops-form-save-failed");

    if (saveFailedMarker || (isReportFormPage() && errs.length && !urlMsg && !pageMsg)) {
      clearStaleSaveIntent();
      var detail = errs[0] || "Check the form fields below.";
      console.log("[OpsSave] validation failed: " + detail);
      showToast("Could not save — " + detail, "error", 12000);
      return;
    }

    var text = urlMsg || messageFromSession();
    if (!text && !isReportFormPage()) {
      text = pageMsg;
    }
    if (text) {
      console.log("[OpsSave] " + text);
      showToast(text, "success", 10000);
    }
  }

  function isEmbeddedLocalApp() {
    try {
      var h = window.location.hostname;
      return h === "127.0.0.1" || h === "localhost";
    } catch (e) {
      return false;
    }
  }

  function isRiderHomePath(pathname) {
    return pathname === "/reports" || pathname === "/reports/";
  }

  /** True only when Django re-rendered the form with validation errors. */
  function isFormValidationErrorHtml(html) {
    if (!html) return false;
    if (html.indexOf("ops-form-save-failed") >= 0) return true;
    if (html.indexOf('class="msg-error"') >= 0) return true;
    if (/<ul class="errorlist">\s*<li[^>]*>/.test(html)) return true;
    return false;
  }

  function riderHomeAfterSubmit(form, resUrl) {
    var qs = "save_ok=submitted";
    var pk =
      (form && form.getAttribute("data-report-pk")) ||
      "";
    if (!pk && resUrl) {
      var m = String(resUrl).match(/\/reports\/(\d+)(?:\/|$)/);
      if (m) pk = m[1];
    }
    if (pk) qs += "&remote_sync_report=" + encodeURIComponent(pk);
    qs += "&_fresh=" + Date.now();
    return RIDER_HOME + "?" + qs;
  }

  function navigateToRiderHome(target) {
    if (!target) {
      target = RIDER_HOME + "?save_ok=submitted";
    } else {
      try {
        var path = new URL(target, window.location.origin).pathname;
        if (!isRiderHomePath(path)) {
          target = RIDER_HOME + "?save_ok=submitted";
        } else {
          target = new URL(target, window.location.origin).href;
        }
      } catch (e) {
        if (target.indexOf("/reports/") !== 0 && target.indexOf("reports/") !== 0) {
          target = RIDER_HOME + "?save_ok=submitted";
        }
      }
    }
    console.log("[OpsSave] navigating to home: " + target);
    window.location.replace(target);
  }

  function buildSubmitFormData(form, submitter) {
    var fd;
    try {
      fd = new FormData(form, submitter || undefined);
    } catch (e) {
      fd = new FormData(form);
    }
    if (!fd.has("action")) {
      fd.append("action", "submit");
    }
    return fd;
  }

  function scheduleNavigateFallback() {
    setTimeout(function () {
      if (!isReportFormPage()) return;
      if (document.querySelector(".errorlist li") || document.getElementById("ops-form-save-failed")) {
        console.log("[OpsSave] fallback skipped — validation errors on form");
        return;
      }
      console.log("[OpsSave] fallback navigate — still on report form after save");
      var form = document.getElementById("report-form");
      navigateToRiderHome(form ? riderHomeAfterSubmit(form, window.location.href) : null);
    }, 600);
  }

  function replaceDocumentHtml(html) {
    document.open();
    document.write(html);
    document.close();
    onPageReady();
  }

  function submitReportFormViaFetch(form, submitter) {
    var action = form.getAttribute("action") || window.location.pathname;
    var fd = buildSubmitFormData(form, submitter);
    var embedded = isEmbeddedLocalApp();
    console.log(
      "[OpsSave] fetch POST " +
        action +
        " action_field=" +
        (fd.get("action") || "") +
        " redirect=follow online=" +
        navigator.onLine,
    );
    return fetch(action, {
      method: "POST",
      body: fd,
      credentials: "same-origin",
      redirect: "follow",
    }).then(function (res) {
      console.log(
        "[OpsSave] response status=" +
          res.status +
          " url=" +
          (res.url || "") +
          " redirected=" +
          res.redirected,
      );
      return res.text().then(function (html) {
        if (isFormValidationErrorHtml(html)) {
          console.log("[OpsSave] validation errors in HTML — staying on form");
          replaceDocumentHtml(html);
          return;
        }
        var home = riderHomeAfterSubmit(form, res.url);
        console.log("[OpsSave] save OK — going home: " + home);
        navigateToRiderHome(home);
        scheduleNavigateFallback();
      });
    });
  }

  function getSubmitter(ev, form) {
    if (ev.submitter) return ev.submitter;
    return form.querySelector('button[name="action"][value="submit"]');
  }

  function bindReportForm(form) {
    if (!form || form.getAttribute("data-save-feedback-bound")) return;
    form.setAttribute("data-save-feedback-bound", "1");
    form.addEventListener(
      "submit",
      function (ev) {
        var sub = getSubmitter(ev, form);
        var isSubmit =
          sub &&
          sub.name === "action" &&
          String(sub.value || "").toLowerCase() === "submit";
        var isReview =
          sub && (sub.getAttribute("formaction") || "").indexOf("/submit") >= 0;

        if (isReview) {
          stashSaveIntent("review");
          showToast("Submitting for review…", "pending", 120000);
          return;
        }

        if (!isSubmit) {
          return;
        }

        ev.preventDefault();
        ev.stopPropagation();
        stashSaveIntent("submit");
        console.log("[OpsSave] submit via fetch");
        showToast("Saving your report…", "pending", 120000);

        submitReportFormViaFetch(form, sub).catch(function (err) {
          console.warn("[OpsSave] fetch submit failed", err);
          clearStaleSaveIntent();
          showToast("Save failed: " + (err && err.message ? err.message : String(err)), "error", 12000);
        });
      },
      true,
    );
  }

  function cleanSaveQueryParams() {
    if (!isRiderHomePage()) return;
    var params = new URLSearchParams(window.location.search);
    if (!params.has("save_ok") && !params.has("draft_cleared")) return;
    params.delete("save_ok");
    params.delete("draft_cleared");
    params.delete("_fresh");
    var qs = params.toString();
    var next = window.location.pathname + (qs ? "?" + qs : "") + window.location.hash;
    window.history.replaceState({}, "", next);
  }

  function onPageReady() {
    var form = document.getElementById("report-form");
    if (form) bindReportForm(form);
    showPendingSaveFeedback();
    setTimeout(cleanSaveQueryParams, 500);
  }

  document.addEventListener("DOMContentLoaded", onPageReady);
  window.addEventListener("pageshow", function (ev) {
    if (ev.persisted) onPageReady();
  });

  window.OpsSaveFeedback = {
    showToast: showToast,
    showPendingSaveFeedback: showPendingSaveFeedback,
    onPageReady: onPageReady,
    navigateToRiderHome: navigateToRiderHome,
  };
})();
