/**
 * Router Search Module (Linear Search vs Binary Search)
 * Provides interactive step-by-step animation and algorithmic comparison.
 */

const SearchView = {
  currentRouters: [],

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const btnCompare = document.getElementById("btn-run-search-compare");
    if (btnCompare) {
      btnCompare.addEventListener("click", () => this.runComparison());
    }

    const btnQuickSearch = document.getElementById("search-input-target");
    if (btnQuickSearch) {
      btnQuickSearch.addEventListener("keypress", (e) => {
        if (e.key === "Enter") this.runComparison();
      });
    }
  },

  async runComparison() {
    const input = document.getElementById("search-input-target");
    const targetId = input ? input.value.trim().toUpperCase() : "R4";

    if (!targetId) {
      App.showToast("Please enter a Router ID to search (e.g., R4)", "warning");
      return;
    }

    try {
      const data = await API.searchCompare(targetId);
      this.renderComparisonResults(data);
      this.animateLinearSearch(data.linear);
      this.animateBinarySearch(data.binary);
    } catch (err) {
      console.error("Search comparison error:", err);
      App.showToast("Error running search comparison", "danger");
    }
  },

  renderComparisonResults(data) {
    const tableBody = document.getElementById("search-comparison-tbody");
    if (!tableBody) return;

    const lin = data.linear;
    const bin = data.binary;

    tableBody.innerHTML = `
      <tr>
        <td><strong>Target Router ID</strong></td>
        <td><span class="badge badge-info">${data.target_id}</span></td>
        <td><span class="badge badge-info">${data.target_id}</span></td>
      </tr>
      <tr>
        <td><strong>Search Result</strong></td>
        <td>
          <span class="badge ${lin.found ? "badge-success" : "badge-danger"}">
            ${lin.found ? "FOUND" : "NOT FOUND"}
          </span>
        </td>
        <td>
          <span class="badge ${bin.found ? "badge-success" : "badge-danger"}">
            ${bin.found ? "FOUND" : "NOT FOUND"}
          </span>
        </td>
      </tr>
      <tr style="background-color: #eff6ff;">
        <td><strong>Number of Comparisons</strong><br><small style="color: #64748b;">Primary DSA Metric</small></td>
        <td><strong style="color: #2563eb; font-size: 1.1rem;">${lin.comparisons}</strong></td>
        <td><strong style="color: #10b981; font-size: 1.1rem;">${bin.comparisons}</strong></td>
      </tr>
      <tr>
        <td><strong>Time Complexity</strong></td>
        <td><code>O(n)</code> (Linear)</td>
        <td><code>O(log n)</code> (Logarithmic)</td>
      </tr>
      <tr>
        <td><strong>Precondition Required</strong></td>
        <td>None (Works on unsorted data)</td>
        <td>Strictly requires sorted keys</td>
      </tr>
      <tr>
        <td><strong>Execution Time</strong></td>
        <td>${lin.execution_time_ms.toFixed(4)} ms</td>
        <td>${bin.execution_time_ms.toFixed(4)} ms</td>
      </tr>
    `;

    // Render explanation
    const expBox = document.getElementById("search-explanation-card");
    if (expBox) {
      expBox.innerHTML = `
        <div class="educational-banner">
          <h4>Search Performance Analysis (${data.target_id})</h4>
          <p>${data.comparison_analysis.explanation}</p>
        </div>
      `;
    }
  },

  animateLinearSearch(linearData) {
    const container = document.getElementById("linear-search-trace-box");
    if (!container) return;

    let html = `<div style="display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 12px;">`;
    linearData.steps.forEach((s) => {
      html += `
        <div style="padding: 6px 10px; border: 1px solid ${s.is_match ? "#10b981" : "#cbd5e1"}; 
                    background: ${s.is_match ? "#ecfdf5" : "#ffffff"}; 
                    border-radius: 6px; text-align: center; min-width: 60px;">
          <div style="font-size: 0.68rem; color: #64748b;">idx ${s.index}</div>
          <div style="font-weight: 700; color: ${s.is_match ? "#047857" : "#1e293b"};">${s.current_id}</div>
          <div style="font-size: 0.65rem; color: #3b82f6;">comp #${s.comparisons_so_far}</div>
        </div>
      `;
    });
    html += `</div>`;

    html += `<div class="step-log-feed" style="max-height: 140px;">`;
    linearData.steps.forEach((s) => {
      html += `
        <div class="step-log-item ${s.is_match ? "current-step" : ""}">
          <span class="step-num-badge">#${s.step}</span>
          <div>${s.message}</div>
        </div>`;
    });
    html += `</div>`;
    container.innerHTML = html;
  },

  animateBinarySearch(binaryData) {
    const container = document.getElementById("binary-search-trace-box");
    if (!container) return;

    let html = `
      <div style="margin-bottom: 10px; font-size: 0.82rem; color: var(--text-muted);">
        Sorted Keys: <code>[${binaryData.sorted_keys.join(", ")}]</code>
      </div>
      <div class="step-log-feed" style="max-height: 180px;">
    `;

    binaryData.steps.forEach((s) => {
      html += `
        <div class="step-log-item ${s.is_match ? "current-step" : ""}">
          <span class="step-num-badge">#${s.step}</span>
          <div>
            <strong>low=${s.low}, mid=${s.mid} ('${s.mid_id}'), high=${s.high}</strong>: 
            ${s.message}
          </div>
        </div>
      `;
    });
    html += `</div>`;
    container.innerHTML = html;
  },
};
