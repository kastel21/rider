/**
 * National program charts for ME metrics. Expects JSON in #me-metrics-chart-data
 * and #me-metrics-chart-delivery (json_script).
 */
(function () {
  function shortWeekLabel(iso) {
    var p = String(iso).split("-");
    if (p.length < 3) {
      return iso;
    }
    var d = new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
    return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
  }

  function readJsonScript(id) {
    var el = document.getElementById(id);
    if (!el) {
      return null;
    }
    try {
      return JSON.parse(el.textContent);
    } catch (e) {
      return null;
    }
  }

  function destroyChartIfAny(canvas) {
    if (!canvas || typeof Chart === "undefined" || typeof Chart.getChart !== "function") {
      return;
    }
    var existing = Chart.getChart(canvas);
    if (existing) {
      existing.destroy();
    }
  }

  function initReportsSamplesChart(raw) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    var labels = (raw.labels || []).map(shortWeekLabel);
    var gridColor = "rgba(148, 163, 184, 0.35)";
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var titleText = wk ? "Reports & samples by week (" + wk + "-week window)" : "Reports & samples by week";

    var c1 = document.getElementById("me-chart-reports-samples");
    if (c1 && raw.reports && raw.samples) {
      destroyChartIfAny(c1);
      new Chart(c1, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Weekly reports",
              data: raw.reports,
              borderColor: "#1d4ed8",
              backgroundColor: "rgba(29, 78, 216, 0.12)",
              fill: true,
              tension: 0.25,
              yAxisID: "y",
            },
            {
              label: "Samples collected",
              data: raw.samples,
              borderColor: "#15803d",
              backgroundColor: "transparent",
              borderDash: [4, 3],
              tension: 0.25,
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: "index", intersect: false },
          plugins: {
            legend: { labels: { font: font } },
            title: {
              display: true,
              text: titleText,
              font: Object.assign({ size: 14, weight: "600" }, font),
            },
          },
          scales: {
            x: {
              ticks: { font: font, maxRotation: 45, minRotation: 0 },
              grid: { display: false },
            },
            y: {
              type: "linear",
              position: "left",
              title: { display: true, text: "Reports", font: font },
              ticks: { font: font, stepSize: 1 },
              grid: { color: gridColor },
              beginAtZero: true,
            },
            y1: {
              type: "linear",
              position: "right",
              title: { display: true, text: "Samples", font: font },
              ticks: { font: font },
              grid: { drawOnChartArea: false },
              beginAtZero: true,
            },
          },
        },
      });
    }
  }

  function initFuelDistanceChart(raw) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    if (!raw.labels || !raw.fuel_allocated || !raw.fuel_used) {
      return;
    }
    var c = document.getElementById("me-chart-fuel-distance");
    if (!c) {
      return;
    }
    destroyChartIfAny(c);
    var labels = (raw.labels || []).map(shortWeekLabel);
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var titleText = wk
      ? "Fuel & distance by week (" + wk + "-week window, week fuel capture)"
      : "Fuel & distance by week";

    new Chart(c, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            type: "bar",
            label: "Fuel allocated",
            data: raw.fuel_allocated,
            backgroundColor: "rgba(29, 78, 216, 0.45)",
            borderColor: "#1d4ed8",
            borderWidth: 1,
            yAxisID: "y",
          },
          {
            type: "bar",
            label: "Fuel used",
            data: raw.fuel_used,
            backgroundColor: "rgba(21, 128, 61, 0.45)",
            borderColor: "#15803d",
            borderWidth: 1,
            yAxisID: "y",
          },
          {
            type: "line",
            label: "Distance (km)",
            data: raw.distance || [],
            borderColor: "#a16207",
            backgroundColor: "transparent",
            tension: 0.2,
            yAxisID: "y1",
            borderWidth: 2,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { font: font } },
          title: {
            display: true,
            text: titleText,
            font: Object.assign({ size: 14, weight: "600" }, font),
          },
        },
        scales: {
          x: {
            ticks: { font: font, maxRotation: 45, minRotation: 0 },
            grid: { display: false },
          },
          y: {
            position: "left",
            title: { display: true, text: "Fuel (units)", font: font },
            ticks: { font: font },
            beginAtZero: true,
          },
          y1: {
            position: "right",
            title: { display: true, text: "Distance (km)", font: font },
            ticks: { font: font },
            grid: { drawOnChartArea: false },
            beginAtZero: true,
          },
        },
      },
    });
  }

  function doughnutFromBlock(canvasId, block, title) {
    var canvas = document.getElementById(canvasId);
    if (!canvas || !block || typeof Chart === "undefined") {
      return;
    }
    destroyChartIfAny(canvas);
    var labels = block.labels || [];
    var values = (block.values || []).map(function (v) {
      return Number(v) || 0;
    });
    var fl = [];
    var fv = [];
    var sum = 0;
    for (var i = 0; i < labels.length; i++) {
      sum += values[i];
      if (values[i] > 0) {
        fl.push(labels[i]);
        fv.push(values[i]);
      }
    }
    if (sum === 0) {
      fl = ["No data in period"];
      fv = [1];
    }
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var colors = [
      "#1d4ed8",
      "#15803d",
      "#a16207",
      "#7c3aed",
      "#dc2626",
      "#0d9488",
      "#ea580c",
    ];
    var bg = fl.map(function (_, i) {
      return colors[i % colors.length] + "99";
    });
    new Chart(canvas, {
      type: "doughnut",
      data: {
        labels: fl,
        datasets: [
          {
            data: fv,
            backgroundColor: bg,
            borderColor: "#fff",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { font: font, boxWidth: 12 } },
          title: {
            display: true,
            text: title,
            font: Object.assign({ size: 13, weight: "600" }, font),
          },
        },
      },
    });
  }

  function initDeliveryCharts(raw) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var suffix = wk ? " (" + wk + "-week window)" : "";
    if (raw.specimens) {
      doughnutFromBlock("me-chart-delivery-specimens", raw.specimens, "Specimens by type" + suffix);
    }
    if (raw.results) {
      doughnutFromBlock("me-chart-delivery-results", raw.results, "Results by type" + suffix);
    }
  }

  function sumSeries(arr) {
    if (!arr || !arr.length) {
      return 0;
    }
    var n = 0;
    for (var i = 0; i < arr.length; i++) {
      n += Number(arr[i]) || 0;
    }
    return n;
  }

  function initSpecimenResultTrendChart(canvasId, raw, programLabel) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    var canvas = document.getElementById(canvasId);
    if (!canvas || !Array.isArray(raw.specimens) || !Array.isArray(raw.results)) {
      return;
    }
    destroyChartIfAny(canvas);
    var weekLabels = raw.labels || [];
    var labels = weekLabels.map(shortWeekLabel);
    var specimens = raw.specimens.map(function (v) {
      return Number(v) || 0;
    });
    var results = raw.results.map(function (v) {
      return Number(v) || 0;
    });
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var gridColor = "rgba(148, 163, 184, 0.35)";
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var titleText = wk
      ? programLabel + " transported by week (" + wk + "-week window)"
      : programLabel + " transported by week";
    var hasData = sumSeries(specimens) + sumSeries(results) > 0;
    var noDataNote = hasData ? "" : " — no trip-row data in period";

    new Chart(canvas, {
      type: "line",
      data: {
        labels: labels.length ? labels : ["—"],
        datasets: [
          {
            label: "Specimens",
            data: labels.length ? specimens : [0],
            borderColor: "#1d4ed8",
            backgroundColor: "rgba(29, 78, 216, 0.12)",
            fill: true,
            tension: 0.25,
          },
          {
            label: "Results",
            data: labels.length ? results : [0],
            borderColor: "#15803d",
            backgroundColor: "transparent",
            borderDash: [4, 3],
            tension: 0.25,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { font: font } },
          title: {
            display: true,
            text: titleText + noDataNote,
            font: Object.assign({ size: 14, weight: "600" }, font),
          },
        },
        scales: {
          x: {
            ticks: { font: font, maxRotation: 45, minRotation: 0 },
            grid: { display: false },
          },
          y: {
            ticks: { font: font, precision: 0 },
            grid: { color: gridColor },
            beginAtZero: true,
            title: { display: true, text: "Count", font: font },
          },
        },
      },
    });
  }

  function initStackedProvinceChart(canvasId, block, title) {
    if (!block || typeof Chart === "undefined") {
      return;
    }
    var canvas = document.getElementById(canvasId);
    if (!canvas) {
      return;
    }
    destroyChartIfAny(canvas);
    var labels = block.labels || [];
    var plasma = (block.vl_plasma || []).map(function (v) {
      return Number(v) || 0;
    });
    var dbs = (block.vl_dbs || []).map(function (v) {
      return Number(v) || 0;
    });
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var gridColor = "rgba(148, 163, 184, 0.35)";
    var wk = block.weeks != null ? String(block.weeks) : "";
    var suffix = wk ? " (" + wk + "-week window)" : "";
    var hasData = sumSeries(plasma) + sumSeries(dbs) > 0;
    var noDataNote = hasData ? "" : " — no data in period";

    new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels.length ? labels : ["—"],
        datasets: [
          {
            label: "VL plasma",
            data: labels.length ? plasma : [0],
            backgroundColor: "rgba(29, 78, 216, 0.75)",
            borderColor: "#1d4ed8",
            borderWidth: 1,
            stack: "stack",
          },
          {
            label: "VL DBS",
            data: labels.length ? dbs : [0],
            backgroundColor: "rgba(124, 58, 237, 0.75)",
            borderColor: "#7c3aed",
            borderWidth: 1,
            stack: "stack",
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { font: font } },
          title: {
            display: true,
            text: title + suffix + noDataNote,
            font: Object.assign({ size: 13, weight: "600" }, font),
          },
        },
        scales: {
          x: {
            stacked: true,
            ticks: { font: font, maxRotation: 45, minRotation: 0 },
            grid: { display: false },
          },
          y: {
            stacked: true,
            ticks: { font: font, precision: 0 },
            grid: { color: gridColor },
            beginAtZero: true,
            title: { display: true, text: "Count", font: font },
          },
        },
      },
    });
  }

  function initGroupedProvinceChart(canvasId, raw, title) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    var canvas = document.getElementById(canvasId);
    if (!canvas) {
      return;
    }
    destroyChartIfAny(canvas);
    var labels = raw.labels || [];
    var specimens = (raw.specimens || []).map(function (v) {
      return Number(v) || 0;
    });
    var results = (raw.results || []).map(function (v) {
      return Number(v) || 0;
    });
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var gridColor = "rgba(148, 163, 184, 0.35)";
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var suffix = wk ? " (" + wk + "-week window)" : "";
    var hasData = sumSeries(specimens) + sumSeries(results) > 0;
    var noDataNote = hasData ? "" : " — no data in period";

    new Chart(canvas, {
      type: "bar",
      data: {
        labels: labels.length ? labels : ["—"],
        datasets: [
          {
            label: "Specimens",
            data: labels.length ? specimens : [0],
            backgroundColor: "rgba(29, 78, 216, 0.65)",
            borderColor: "#1d4ed8",
            borderWidth: 1,
          },
          {
            label: "Results",
            data: labels.length ? results : [0],
            backgroundColor: "rgba(21, 128, 61, 0.65)",
            borderColor: "#15803d",
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: { mode: "index", intersect: false },
        plugins: {
          legend: { labels: { font: font } },
          title: {
            display: true,
            text: title + suffix + noDataNote,
            font: Object.assign({ size: 13, weight: "600" }, font),
          },
        },
        scales: {
          x: {
            ticks: { font: font, maxRotation: 45, minRotation: 0 },
            grid: { display: false },
          },
          y: {
            ticks: { font: font, precision: 0 },
            grid: { color: gridColor },
            beginAtZero: true,
            title: { display: true, text: "Count", font: font },
          },
        },
      },
    });
  }

  function initProvinceDeliveryCharts(vlRaw, hpvRaw) {
    if (vlRaw) {
      initStackedProvinceChart(
        "me-chart-province-vl-specimens",
        {
          labels: vlRaw.labels,
          weeks: vlRaw.weeks,
          vl_plasma: (vlRaw.specimens && vlRaw.specimens.vl_plasma) || [],
          vl_dbs: (vlRaw.specimens && vlRaw.specimens.vl_dbs) || [],
        },
        "VL specimens by province"
      );
      initStackedProvinceChart(
        "me-chart-province-vl-results",
        {
          labels: vlRaw.labels,
          weeks: vlRaw.weeks,
          vl_plasma: (vlRaw.results && vlRaw.results.vl_plasma) || [],
          vl_dbs: (vlRaw.results && vlRaw.results.vl_dbs) || [],
        },
        "VL results by province"
      );
    }
    if (hpvRaw) {
      initGroupedProvinceChart("me-chart-province-hpv", hpvRaw, "HPV by province");
    }
  }

  function initDeliveryTrendCharts(raw) {
    if (!raw || typeof Chart === "undefined") {
      return;
    }
    var labels = raw.labels || [];
    var wk = raw.weeks;
    function block(series) {
      return {
        labels: labels,
        weeks: wk,
        specimens: series.specimens,
        results: series.results,
      };
    }
    if (raw.vl) {
      initSpecimenResultTrendChart("me-chart-trend-vl", block(raw.vl), "VL");
    }
    if (raw.hpv) {
      initSpecimenResultTrendChart("me-chart-trend-hpv", block(raw.hpv), "HPV");
    }
    if (raw.tb) {
      initSpecimenResultTrendChart("me-chart-trend-tb", block(raw.tb), "TB");
    }
  }

  function resizeMeCharts() {
    if (typeof Chart === "undefined" || typeof Chart.getChart !== "function") {
      return;
    }
    [
      "me-chart-reports-samples",
      "me-chart-fuel-distance",
      "me-chart-delivery-specimens",
      "me-chart-delivery-results",
      "me-chart-trend-vl",
      "me-chart-trend-hpv",
      "me-chart-trend-tb",
      "me-chart-province-vl-specimens",
      "me-chart-province-vl-results",
      "me-chart-province-hpv",
    ].forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) {
        return;
      }
      var ch = Chart.getChart(el);
      if (ch) {
        ch.resize();
      }
    });
  }

  function initMeMetricsCharts() {
    var main = readJsonScript("me-metrics-chart-data");
    initReportsSamplesChart(main);
    if (main) {
      initFuelDistanceChart(main);
    }
    var delivery = readJsonScript("me-metrics-chart-delivery");
    initDeliveryCharts(delivery);
    var deliveryTrends = readJsonScript("me-metrics-chart-delivery-trends");
    initDeliveryTrendCharts(deliveryTrends);
    var provinceVl = readJsonScript("me-metrics-chart-province-vl");
    var provinceHpv = readJsonScript("me-metrics-chart-province-hpv");
    initProvinceDeliveryCharts(provinceVl, provinceHpv);
    requestAnimationFrame(resizeMeCharts);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMeMetricsCharts);
  } else {
    initMeMetricsCharts();
  }
  window.addEventListener("load", resizeMeCharts);
})();
