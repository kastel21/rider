/**
 * National program trend charts for ME metrics. Expects JSON in #me-metrics-chart-data (json_script).
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

  function initMeMetricsCharts() {
    var el = document.getElementById("me-metrics-chart-data");
    if (!el || typeof Chart === "undefined") {
      return;
    }
    var raw;
    try {
      raw = JSON.parse(el.textContent);
    } catch (e) {
      return;
    }
    var labels = (raw.labels || []).map(shortWeekLabel);
    var grid = { color: "rgba(148, 163, 184, 0.35)" };
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };
    var wk = raw.weeks != null ? String(raw.weeks) : "";
    var titleText = wk ? "Reports & samples by week (" + wk + "-week window)" : "Reports & samples by week";

    var c1 = document.getElementById("me-chart-reports-samples");
    if (c1 && raw.reports && raw.samples) {
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
              grid: { color: grid },
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

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initMeMetricsCharts);
  } else {
    initMeMetricsCharts();
  }
})();
