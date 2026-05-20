/**
 * Trend charts for rider home (Chart.js). Expects JSON in #rider-trend-data (json_script).
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

  function initRiderHomeCharts() {
    var el = document.getElementById("rider-trend-data");
    if (!el || typeof Chart === "undefined") {
      return;
    }
    function destroyIf(canvas) {
      if (!canvas || typeof Chart.getChart !== "function") {
        return;
      }
      var existing = Chart.getChart(canvas);
      if (existing) {
        existing.destroy();
      }
    }
    var raw;
    try {
      raw = JSON.parse(el.textContent);
    } catch (e) {
      return;
    }
    var labels = (raw.labels || []).map(shortWeekLabel);
    var gridColor = "rgba(148, 163, 184, 0.35)";
    var font = { family: "system-ui, Segoe UI, Roboto, sans-serif" };

    var c1 = document.getElementById("rider-chart-samples-trips");
    if (c1 && raw.samples && raw.trips) {
      destroyIf(c1);
      new Chart(c1, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Samples collected",
              data: raw.samples,
              borderColor: "#1d4ed8",
              backgroundColor: "rgba(29, 78, 216, 0.12)",
              fill: true,
              tension: 0.25,
              yAxisID: "y",
            },
            {
              label: "Trips",
              data: raw.trips,
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
              text: "Samples & trips by week (last 12 weeks)",
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
              title: { display: true, text: "Samples", font: font },
              ticks: { font: font },
              grid: { color: gridColor },
              beginAtZero: true,
            },
            y1: {
              type: "linear",
              position: "right",
              title: { display: true, text: "Trips", font: font },
              ticks: { font: font, stepSize: 1 },
              grid: { drawOnChartArea: false },
              beginAtZero: true,
            },
          },
        },
      });
    }

    var c2 = document.getElementById("rider-chart-distance");
    if (c2 && raw.distance_km) {
      destroyIf(c2);
      new Chart(c2, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Distance (km)",
              data: raw.distance_km,
              backgroundColor: "rgba(51, 65, 85, 0.45)",
              borderColor: "#334155",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            title: {
              display: true,
              text: "Distance travelled by week (km)",
              font: Object.assign({ size: 14, weight: "600" }, font),
            },
          },
          scales: {
            x: {
              ticks: { font: font, maxRotation: 45, minRotation: 0 },
              grid: { display: false },
            },
            y: {
              title: { display: true, text: "km", font: font },
              ticks: { font: font },
              grid: { color: gridColor },
              beginAtZero: true,
            },
          },
        },
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initRiderHomeCharts);
  } else {
    initRiderHomeCharts();
  }
})();
