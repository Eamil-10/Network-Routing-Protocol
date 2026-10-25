/**
 * Performance and Traversal Comparison Module
 * Runs benchmark comparisons between BFS and DFS and renders Chart.js charts.
 */

const PerformanceView = {
  chartInstance: null,

  init() {
    this.bindEvents();
  },

  bindEvents() {
    const btnCompare = document.getElementById("btn-run-traversal-compare");
    if (btnCompare) {
      btnCompare.addEventListener("click", () => this.runTraversalComparison());
    }
  },

  async runTraversalComparison() {
    const srcSelect = document.getElementById("compare-source-select") || document.getElementById("sim-source-select");
    const dstSelect = document.getElementById("compare-dest-select") || document.getElementById("sim-dest-select");

    const source = srcSelect ? srcSelect.value : "R1";
    const destination = dstSelect ? dstSelect.value : "R6";

    if (!source || !destination) {
      App.showToast("Please select both source and destination routers.", "warning");
      return;
    }

    try {
      const data = await API.compareTraversals(source, destination);
      this.renderTable(data);
      this.renderChart(data);
      this.renderVerdict(data);
    } catch (err) {
      console.error("Comparison error:", err);
      App.showToast("Error running traversal comparison", "danger");
    }
  },

  renderTable(data) {
    const tbody = document.getElementById("traversal-comparison-tbody");
    if (!tbody) return;

    const b = data.bfs;
    const d = data.dfs;

    tbody.innerHTML = `
      <tr>
        <td><strong>Route Found</strong></td>
        <td><code>${b.route.length > 0 ? b.route.join(" → ") : "None"}</code></td>
        <td><code>${d.route.length > 0 ? d.route.join(" → ") : "None"}</code></td>
      </tr>
      <tr style="background: #f0fdf4;">
        <td><strong>Hop Count (Edges)</strong><br><small style="color: #059669;">Primary Efficiency Metric</small></td>
        <td><strong style="color: #10b981; font-size: 1.15rem;">${b.hops}</strong> (Minimum)</td>
        <td><strong style="color: #f59e0b; font-size: 1.15rem;">${d.hops}</strong></td>
      </tr>
      <tr>
        <td><strong>Nodes Visited</strong></td>
        <td>${b.nodes_visited}</td>
        <td>${d.nodes_visited}</td>
      </tr>
      <tr>
        <td><strong>Edges Examined</strong></td>
        <td>${b.edges_examined}</td>
        <td>${d.edges_examined}</td>
      </tr>
      <tr>
        <td><strong>Total Traversal Steps</strong></td>
        <td>${b.traversal_steps}</td>
        <td>${d.traversal_steps}</td>
      </tr>
      <tr>
        <td><strong>Backtracking Events</strong></td>
        <td>0 (Queue Level-Order)</td>
        <td><strong>${d.backtracking_count}</strong> (Stack Unwinding)</td>
      </tr>
      <tr>
        <td><strong>Execution Time</strong></td>
        <td>${b.execution_time_ms.toFixed(4)} ms</td>
        <td>${d.execution_time_ms.toFixed(4)} ms</td>
      </tr>
      <tr>
        <td><strong>Theoretical Time Complexity</strong></td>
        <td><code>O(V + E)</code></td>
        <td><code>O(V + E)</code></td>
      </tr>
      <tr>
        <td><strong>Auxiliary Space Complexity</strong></td>
        <td><code>O(V)</code> (FIFO Queue)</td>
        <td><code>O(V)</code> (LIFO Stack)</td>
      </tr>
    `;
  },

  renderChart(data) {
    const canvas = document.getElementById("traversal-comparison-chart");
    if (!canvas || typeof Chart === "undefined") return;

    if (this.chartInstance) {
      this.chartInstance.destroy();
    }

    const b = data.bfs;
    const d = data.dfs;

    this.chartInstance = new Chart(canvas, {
      type: "bar",
      data: {
        labels: ["Hop Count (Fewer is Better)", "Nodes Visited", "Traversal Steps", "Edges Examined"],
        datasets: [
          {
            label: "BFS (Breadth-First Search)",
            data: [b.hops, b.nodes_visited, b.traversal_steps, b.edges_examined],
            backgroundColor: "rgba(37, 99, 235, 0.7)",
            borderColor: "rgb(37, 99, 235)",
            borderWidth: 1,
            borderRadius: 6,
          },
          {
            label: "DFS (Depth-First Search)",
            data: [d.hops, d.nodes_visited, d.traversal_steps, d.edges_examined],
            backgroundColor: "rgba(245, 158, 11, 0.7)",
            borderColor: "rgb(245, 158, 11)",
            borderWidth: 1,
            borderRadius: 6,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: `Comparison: ${data.source} → ${data.destination}`,
            font: { size: 14, weight: "bold" },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { precision: 0 },
          },
        },
      },
    });
  },

  renderVerdict(data) {
    const verdictBox = document.getElementById("traversal-verdict-box");
    if (!verdictBox) return;

    const b = data.bfs;
    const d = data.dfs;

    verdictBox.innerHTML = `
      <div class="educational-banner" style="border-left-color: #10b981; background: #ecfdf5; border-color: #a7f3d0;">
        <h4 style="color: #065f46;">Academic Findings & Algorithm Justification</h4>
        <p style="color: #064e3b; margin-bottom: 6px;">
          • <strong>BFS (Breadth-First Search):</strong> Found a <strong>${b.hops}-hop route</strong>. 
          In an unweighted network, BFS explores neighbors level by level using a FIFO queue, guaranteeing that the first time 
          the destination router is reached, the discovered route possesses the <em>minimum number of hops</em>.
        </p>
        <p style="color: #064e3b; margin-bottom: 6px;">
          • <strong>DFS (Depth-First Search):</strong> Explored deeply and discovered a <strong>${d.hops}-hop route</strong> 
          with <strong>${d.backtracking_count} backtrack event(s)</strong>. DFS does NOT guarantee a minimum-hop route; its path depends on neighbor order.
        </p>
        <p style="color: #064e3b;">
          • <strong>Conclusion for Network Routing:</strong> For unweighted packet routing where shortest path = lowest hop delay, 
          BFS is the academically appropriate algorithm. DFS is valuable for topological connectivity, cycle detection, and maze/puzzle exploration.
        </p>
      </div>
    `;
  },
};
