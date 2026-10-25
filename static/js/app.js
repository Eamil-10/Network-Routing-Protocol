/**
 * Main Application Controller for Network Routing Simulator
 * Manages UI interactions, tab switching, and component orchestration.
 */

const App = {
  activeTopology: null,
  mainCyView: null,
  dashboardCyView: null,
  unifiedSimulation: null,
  bfsSimulation: null,
  dfsSimulation: null,
  currentSimAlgo: "BFS",
  lastComputedRoute: ["R1", "R2", "R4", "R6"],

  async init() {
    console.log("Initializing Network Routing Simulator...");

    // 1. Initialize Cytoscape Visualizers
    this.initVisualizers();

    // 2. Initialize Sub-modules
    SearchView.init();
    PerformanceView.init();

    // 3. Bind Navigation & Global UI Events
    this.bindEvents();

    // 4. Load Initial Data
    await this.loadInitialData();

    // 5. Setup periodic dashboard poll
    setInterval(() => this.updateDashboardStats(), 5000);
  },

  initVisualizers() {
    // Main Cytoscape Graph Canvas
    this.mainCyView = new CytoscapeView("main-cytoscape-canvas", {
      onNodeClick: (nodeData) => this.handleNodeClick(nodeData),
      onEdgeClick: (edgeData) => this.handleEdgeClick(edgeData),
    });

    // Dashboard Mini Preview (if container exists)
    if (document.getElementById("dashboard-cytoscape-preview")) {
      this.dashboardCyView = new CytoscapeView("dashboard-cytoscape-preview");
    }

    // Unified Simulation Engine (Right panel in Simulator tab)
    this.unifiedSimulation = new TraversalSimulation(this.mainCyView, {
      dsContainer: document.getElementById("sim-ds-container"),
      dsTitle: document.getElementById("sim-ds-title"),
      dsSize: document.getElementById("sim-ds-size"),
      visitedBox: document.getElementById("sim-visited-container"),
      parentTable: document.getElementById("sim-parent-tbody"),
      explanationText: document.getElementById("sim-explanation-text"),
      currentNodeBadge: document.getElementById("sim-current-node"),
      stepCounterBadge: document.getElementById("sim-step-counter"),
      backtrackBadge: document.getElementById("sim-backtrack-indicator"),
      finalRouteBox: document.getElementById("sim-reconstructed-route-box"),
      finalRoutePath: document.getElementById("sim-final-route-path"),
      btnStart: document.getElementById("btn-sim-start"),
      btnPause: document.getElementById("btn-sim-pause"),
      btnStep: document.getElementById("btn-sim-step"),
      btnPrev: document.getElementById("btn-sim-prev"),
    });

    // Sub-panel simulations (for legacy or detailed tabs if present)
    if (document.getElementById("bfs-queue-container")) {
      this.bfsSimulation = new TraversalSimulation(this.mainCyView, {
        dsContainer: document.getElementById("bfs-queue-container"),
        visitedBox: document.getElementById("bfs-visited-box"),
        parentTable: document.getElementById("bfs-parent-tbody"),
        explanationBox: document.getElementById("bfs-explanation-box"),
        stepLogContainer: document.getElementById("bfs-step-log-feed"),
        reconstructionBox: document.getElementById("bfs-reconstruction-box"),
        currentNodeBadge: document.getElementById("bfs-current-node-badge"),
        stepCounterBadge: document.getElementById("bfs-step-counter-badge"),
        btnStart: document.getElementById("btn-bfs-start"),
        btnPause: document.getElementById("btn-bfs-pause"),
        btnStep: document.getElementById("btn-bfs-step"),
        btnPrev: document.getElementById("btn-bfs-prev"),
      });
    }

    if (document.getElementById("dfs-stack-container")) {
      this.dfsSimulation = new TraversalSimulation(this.mainCyView, {
        dsContainer: document.getElementById("dfs-stack-container"),
        visitedBox: document.getElementById("dfs-visited-box"),
        parentTable: document.getElementById("dfs-parent-tbody"),
        explanationBox: document.getElementById("dfs-explanation-box"),
        stepLogContainer: document.getElementById("dfs-step-log-feed"),
        reconstructionBox: document.getElementById("dfs-reconstruction-box"),
        currentNodeBadge: document.getElementById("dfs-current-node-badge"),
        stepCounterBadge: document.getElementById("dfs-step-counter-badge"),
        btnStart: document.getElementById("btn-dfs-start"),
        btnPause: document.getElementById("btn-dfs-pause"),
        btnStep: document.getElementById("btn-dfs-step"),
        btnPrev: document.getElementById("btn-dfs-prev"),
      });
    }
  },

  bindEvents() {
    // 3-Tab navigation
    const navButtons = document.querySelectorAll(".nav-tab-btn");
    navButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const targetTab = btn.getAttribute("data-tab");
        this.switchTab(targetTab);
      });
    });

    // Scenario selector
    const scenarioSelect = document.getElementById("preset-scenario-select");
    if (scenarioSelect) {
      scenarioSelect.addEventListener("change", async (e) => {
        await this.loadScenario(e.target.value);
      });
    }

    // Reset topology button
    const btnResetTopo = document.getElementById("btn-reset-topology");
    if (btnResetTopo) {
      btnResetTopo.addEventListener("click", async () => {
        const data = await API.resetTopology();
        if (data.success) {
          this.showToast("Topology reset to initial preset state.", "success");
          await this.refreshAllViews();
        }
      });
    }

    // Cytoscape Canvas Controls (Fit, Zoom)
    const btnFit = document.getElementById("btn-canvas-fit");
    if (btnFit) btnFit.addEventListener("click", () => this.mainCyView.fit());
    const btnZoomIn = document.getElementById("btn-canvas-zoom-in");
    if (btnZoomIn) btnZoomIn.addEventListener("click", () => this.mainCyView.zoomIn());
    const btnZoomOut = document.getElementById("btn-canvas-zoom-out");
    if (btnZoomOut) btnZoomOut.addEventListener("click", () => this.mainCyView.zoomOut());

    // Algorithm Selector Buttons (BFS / DFS)
    const btnSelectBFS = document.getElementById("btn-select-algo-bfs");
    if (btnSelectBFS) {
      btnSelectBFS.addEventListener("click", () => this.setAlgorithm("BFS"));
    }
    const btnSelectDFS = document.getElementById("btn-select-algo-dfs");
    if (btnSelectDFS) {
      btnSelectDFS.addEventListener("click", () => this.setAlgorithm("DFS"));
    }

    // Unified Run Traversal Button
    const btnCompute = document.getElementById("btn-compute-traversal");
    if (btnCompute) {
      btnCompute.addEventListener("click", () => this.runUnifiedSimulation());
    }

    // Unified Simulation Playback Controls
    const btnSimStep = document.getElementById("btn-sim-step");
    if (btnSimStep) btnSimStep.addEventListener("click", () => this.unifiedSimulation.stepForward());
    const btnSimPrev = document.getElementById("btn-sim-prev");
    if (btnSimPrev) btnSimPrev.addEventListener("click", () => this.unifiedSimulation.stepBackward());
    const btnSimStart = document.getElementById("btn-sim-start");
    if (btnSimStart) btnSimStart.addEventListener("click", () => this.unifiedSimulation.start());
    const btnSimPause = document.getElementById("btn-sim-pause");
    if (btnSimPause) btnSimPause.addEventListener("click", () => this.unifiedSimulation.pause());
    const btnSimReset = document.getElementById("btn-sim-reset");
    if (btnSimReset) btnSimReset.addEventListener("click", () => this.unifiedSimulation.reset());

    // Speed Slider
    const speedSlider = document.getElementById("sim-speed-slider");
    const speedVal = document.getElementById("sim-speed-val");
    if (speedSlider) {
      const updateSpeed = (val) => {
        if (speedVal) speedVal.textContent = `${val}ms`;
        this.unifiedSimulation.setSpeed(val);
      };
      speedSlider.addEventListener("input", (e) => updateSpeed(e.target.value));
      speedSlider.addEventListener("change", (e) => updateSpeed(e.target.value));
    }

    // Packet creation & processing
    const btnCreatePacket = document.getElementById("btn-enqueue-packet");
    if (btnCreatePacket) {
      btnCreatePacket.addEventListener("click", () => this.handleCreatePacket());
    }

    const btnProcessNext = document.getElementById("btn-process-next-packet");
    if (btnProcessNext) {
      btnProcessNext.addEventListener("click", () => this.handleProcessNextPacket());
    }

    // Failure simulation controls
    const btnDisableRouter = document.getElementById("btn-toggle-selected-router");
    if (btnDisableRouter) {
      btnDisableRouter.addEventListener("click", () => this.handleToggleSelectedRouter());
    }

    const btnRecalcRoute = document.getElementById("btn-dynamic-recalc-route");
    if (btnRecalcRoute) {
      btnRecalcRoute.addEventListener("click", () => this.handleDynamicRecalculation());
    }

    // Routing table selector
    const rtSelect = document.getElementById("routing-table-router-select");
    if (rtSelect) {
      rtSelect.addEventListener("change", (e) => this.loadRoutingTableFor(e.target.value));
    }
  },

  bindSimulationControls(prefix, simEngine) {
    const btnStart = document.getElementById(`btn-${prefix}-start`);
    const btnPause = document.getElementById(`btn-${prefix}-pause`);
    const btnStep = document.getElementById(`btn-${prefix}-step`);
    const btnPrev = document.getElementById(`btn-${prefix}-prev`);
    const btnReset = document.getElementById(`btn-${prefix}-reset`);
    const speedSelect = document.getElementById(`${prefix}-speed-select`);

    if (btnStart) btnStart.addEventListener("click", () => simEngine.start());
    if (btnPause) btnPause.addEventListener("click", () => simEngine.pause());
    if (btnStep) btnStep.addEventListener("click", () => simEngine.stepForward());
    if (btnPrev) btnPrev.addEventListener("click", () => simEngine.stepBackward());
    if (btnReset) btnReset.addEventListener("click", () => simEngine.reset());

    if (speedSelect) {
      speedSelect.addEventListener("change", (e) => simEngine.setSpeed(e.target.value));
    }
  },

  switchTab(tabId) {
    document.querySelectorAll(".nav-tab-btn").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-tab") === tabId);
    });

    document.querySelectorAll(".tab-pane").forEach((pane) => {
      pane.classList.toggle("active", pane.id === `tab-${tabId}`);
    });

    // Resize Cytoscape on tab view change
    setTimeout(() => {
      if (this.mainCyView && this.mainCyView.cy) {
        this.mainCyView.cy.resize();
        this.mainCyView.fit();
      }
      if (this.dashboardCyView && this.dashboardCyView.cy) {
        this.dashboardCyView.cy.resize();
        this.dashboardCyView.fit();
      }
    }, 50);

    // Tab-specific refreshes
    if (tabId === "history") this.loadPacketHistory();
    if (tabId === "routing-table") {
      const select = document.getElementById("routing-table-router-select");
      if (select && select.value) this.loadRoutingTableFor(select.value);
    }
  },

  async loadInitialData() {
    try {
      // Load preset scenarios list
      const scenData = await API.listScenarios();
      const scenSelect = document.getElementById("preset-scenario-select");
      if (scenSelect && scenData.scenarios) {
        scenSelect.innerHTML = scenData.scenarios
          .map((s) => `<option value="${s.id}">${s.name}</option>`)
          .join("");
      }

      await this.refreshAllViews();
    } catch (err) {
      console.error("Failed to load initial data:", err);
    }
  },

  async loadScenario(scenarioId) {
    try {
      const data = await API.loadScenario(scenarioId);
      if (data.success) {
        this.showToast(`Loaded scenario: ${scenarioId}`, "success");
        await this.refreshAllViews();
      }
    } catch (err) {
      console.error("Failed to switch scenario:", err);
    }
  },

  async refreshAllViews() {
    const topoData = await API.getTopology();
    if (!topoData.success) return;

    this.activeTopology = topoData.topology;

    // Render in Cytoscape views
    this.mainCyView.renderTopology(this.activeTopology);
    this.dashboardCyView.renderTopology(this.activeTopology);

    // Populate all Router selector dropdowns
    this.populateRouterSelectors(this.activeTopology.routers);

    // Render Adjacency List & Matrix
    this.renderAdjacencyList(this.activeTopology.adjacency_list);
    this.renderAdjacencyMatrix(this.activeTopology.adjacency_matrix);

    // Render Router Directory table for search
    this.renderRouterDirectory(this.activeTopology.routers);

    // Refresh Dashboard Stats
    await this.updateDashboardStats();

    // Refresh Queue View
    await this.refreshPacketQueue();
  },

  populateRouterSelectors(routers) {
    const routerIds = routers.map((r) => r.id);
    const selectors = [
      "sim-source-select",
      "sim-dest-select",
      "bfs-source-select",
      "bfs-dest-select",
      "dfs-source-select",
      "dfs-dest-select",
      "compare-source-select",
      "compare-dest-select",
      "packet-source-select",
      "packet-dest-select",
      "routing-table-router-select",
      "failure-router-select",
    ];

    selectors.forEach((selectId) => {
      const el = document.getElementById(selectId);
      if (!el) return;
      const currentVal = el.value;

      el.innerHTML = routerIds
        .map((id) => `<option value="${id}">${id}</option>`)
        .join("");

      if (routerIds.includes(currentVal)) {
        el.value = currentVal;
      } else if (selectId.includes("dest") && routerIds.length > 1) {
        el.value = routerIds[routerIds.length - 1];
      } else if (routerIds.length > 0) {
        el.value = routerIds[0];
      }
    });
  },

  renderAdjacencyList(adjList) {
    const container = document.getElementById("adjacency-list-view");
    if (!container) return;

    let html = `<div style="font-family: var(--font-mono); font-size: 0.88rem; line-height: 1.8;">`;
    for (const [router, neighbors] of Object.entries(adjList)) {
      html += `
        <div style="padding: 4px 8px; border-bottom: 1px solid var(--border);">
          <strong style="color: #2563eb;">${router}</strong> → ${
            neighbors.length > 0
              ? neighbors
                  .map((n) => `<span class="badge badge-info" style="margin: 0 2px;">${n}</span>`)
                  .join(" ")
              : '<span class="text-muted">(Isolated)</span>'
          }
        </div>
      `;
    }
    html += `</div>`;
    container.innerHTML = html;
  },

  renderAdjacencyMatrix(matrixData) {
    const container = document.getElementById("adjacency-matrix-view");
    if (!container || !matrixData) return;

    const vertices = matrixData.vertices;
    const matrix = matrixData.matrix;

    let html = `<table class="adj-matrix-table"><thead><tr><th></th>`;
    vertices.forEach((v) => {
      html += `<th>${v}</th>`;
    });
    html += `</tr></thead><tbody>`;

    vertices.forEach((rowVertex, i) => {
      html += `<tr><th>${rowVertex}</th>`;
      vertices.forEach((colVertex, j) => {
        const val = matrix[i][j];
        const isConn = val === 1;
        html += `<td class="${isConn ? "cell-connected" : "cell-empty"}">${val}</td>`;
      });
      html += `</tr>`;
    });

    html += `</tbody></table>`;
    container.innerHTML = html;
  },

  renderRouterDirectory(routers) {
    const tbody = document.getElementById("router-directory-tbody");
    if (!tbody) return;

    tbody.innerHTML = routers
      .map(
        (r) => `
        <tr>
          <td><strong>${r.id}</strong></td>
          <td>${r.name}</td>
          <td><code>${r.ip_address}</code></td>
          <td>
            <span class="badge ${r.is_active ? "badge-success" : "badge-danger"}">
              ${r.is_active ? "Active" : "Disabled"}
            </span>
          </td>
          <td>${r.location}</td>
        </tr>
      `
      )
      .join("");
  },

  async updateDashboardStats() {
    try {
      const data = await API.getDashboardStats();
      if (!data.success) return;

      const setVal = (id, val) => {
        const el = document.getElementById(id);
        if (el) el.textContent = val;
      };

      setVal("stat-total-routers", data.total_routers);
      setVal("stat-active-links", data.active_links);
      setVal("stat-packets-queue", data.packets_in_queue);
      setVal("stat-delivered-packets", data.delivered_packets);
      setVal("stat-failed-packets", data.failed_packets);
      setVal("stat-active-routes", data.active_routers > 1 ? "Operational" : "Degraded");

      // Update Activity Feed
      const feed = document.getElementById("dashboard-activity-feed");
      if (feed && data.recent_activities) {
        feed.innerHTML = data.recent_activities
          .map(
            (act) => `
            <div class="step-log-item">
              <span class="step-num-badge">${act.event_type.replace(/_/g, " ")}</span>
              <div style="flex: 1;">
                <div>${act.message}</div>
                <div style="font-size: 0.7rem; color: #94a3b8;">${act.timestamp}</div>
              </div>
            </div>
          `
          )
          .join("");
      }
    } catch (e) {
      // Silent catch
    }
  },

  // -------------------------------------------------------------
  // Simulation Triggers (Unified BFS & DFS)
  // -------------------------------------------------------------
  setAlgorithm(algo) {
    this.currentSimAlgo = algo;
    const btnBFS = document.getElementById("btn-select-algo-bfs");
    const btnDFS = document.getElementById("btn-select-algo-dfs");
    const badge = document.getElementById("unified-algo-badge");
    const dsTitle = document.getElementById("sim-ds-title");

    if (algo === "BFS") {
      if (btnBFS) {
        btnBFS.classList.add("btn-primary", "active");
        btnBFS.classList.remove("btn-secondary");
      }
      if (btnDFS) {
        btnDFS.classList.remove("btn-primary", "active");
        btnDFS.classList.add("btn-secondary");
      }
      if (badge) {
        badge.textContent = "BFS (FIFO Queue - CO1)";
        badge.className = "badge badge-primary";
      }
      if (dsTitle) dsTitle.textContent = "📦 Live FIFO Queue (Front ➔ Rear)";
    } else {
      if (btnDFS) {
        btnDFS.classList.add("btn-primary", "active");
        btnDFS.classList.remove("btn-secondary");
      }
      if (btnBFS) {
        btnBFS.classList.remove("btn-primary", "active");
        btnBFS.classList.add("btn-secondary");
      }
      if (badge) {
        badge.textContent = "DFS (LIFO Stack - CO1)";
        badge.className = "badge badge-warning";
      }
      if (dsTitle) dsTitle.textContent = "📚 Live LIFO Stack (Bottom ➔ Top)";
    }

    if (this.unifiedSimulation) {
      this.unifiedSimulation.reset();
    }
    this.showToast(`Switched algorithm to ${algo}`, "info");
  },

  async runUnifiedSimulation() {
    const srcEl = document.getElementById("sim-source-select");
    const dstEl = document.getElementById("sim-dest-select");
    const src = srcEl ? srcEl.value : "R1";
    const dst = dstEl ? dstEl.value : "R6";

    this.mainCyView.setSourceDestination(src, dst);

    try {
      let result;
      if (this.currentSimAlgo === "BFS") {
        result = await API.runBFS(src, dst);
        if (result.success) {
          this.lastComputedRoute = result.route;
          this.showToast(`BFS computed: ${result.hops} hops discovered.`, "info");
        } else {
          this.showToast(result.error || "No route found", "danger");
        }
        this.unifiedSimulation.loadSimulation(result, "BFS");
      } else {
        result = await API.runDFS(src, dst);
        if (result.success) {
          this.lastComputedRoute = result.route;
          this.showToast(
            `DFS computed: ${result.hops} hops (${result.backtracking_count} backtrack${result.backtracking_count === 1 ? "" : "s"}).`,
            "info"
          );
        } else {
          this.showToast(result.error || "No route found", "danger");
        }
        this.unifiedSimulation.loadSimulation(result, "DFS");
      }
    } catch (err) {
      console.error("Traversal computation error:", err);
      this.showToast("Failed to compute traversal", "danger");
    }
  },

  async runBFSSimulation() {
    const src = document.getElementById("bfs-source-select")?.value || "R1";
    const dst = document.getElementById("bfs-dest-select")?.value || "R6";

    this.mainCyView.setSourceDestination(src, dst);

    try {
      const result = await API.runBFS(src, dst);
      if (!result.success && result.error) {
        this.showToast(result.error, "danger");
      }
      if (this.bfsSimulation) this.bfsSimulation.loadSimulation(result, "BFS");
      this.showToast(`BFS computed: ${result.hops} hops discovered.`, "info");
    } catch (err) {
      console.error("BFS failed:", err);
      this.showToast("Failed to compute BFS traversal", "danger");
    }
  },

  async runDFSSimulation() {
    const src = document.getElementById("dfs-source-select")?.value || "R1";
    const dst = document.getElementById("dfs-dest-select")?.value || "R6";

    this.mainCyView.setSourceDestination(src, dst);

    try {
      const result = await API.runDFS(src, dst);
      if (!result.success && result.error) {
        this.showToast(result.error, "danger");
      }
      if (this.dfsSimulation) this.dfsSimulation.loadSimulation(result, "DFS");
      this.showToast(`DFS computed: ${result.hops} hops (${result.backtracking_count} backtracks).`, "info");
    } catch (err) {
      console.error("DFS failed:", err);
      this.showToast("Failed to compute DFS traversal", "danger");
    }
  },

  // -------------------------------------------------------------
  // Packet Queue Management (FIFO)
  // -------------------------------------------------------------
  async handleCreatePacket() {
    const src = document.getElementById("packet-source-select")?.value || "R1";
    const dst = document.getElementById("packet-dest-select")?.value || "R6";
    const algo = document.getElementById("packet-algorithm-select")?.value || "BFS";

    if (src === dst) {
      this.showToast("Source and destination routers must be different.", "warning");
      return;
    }

    try {
      const data = await API.createPacket(src, dst, algo);
      if (data.success) {
        this.showToast(`Enqueued Packet ${data.packet.packet_id} into FIFO Queue.`, "success");
        await this.refreshPacketQueue();
        await this.updateDashboardStats();
      }
    } catch (err) {
      this.showToast("Error enqueuing packet", "danger");
    }
  },

  async handleProcessNextPacket() {
    try {
      const data = await API.processNextPacket();
      if (!data.success) {
        this.showToast(data.error || "Cannot process packet", "warning");
        return;
      }

      const pkt = data.packet;
      const isDelivered = pkt.status === "DELIVERED";

      this.showToast(
        `Packet ${pkt.packet_id} ${isDelivered ? "Delivered!" : "Failed: No Route"}`,
        isDelivered ? "success" : "danger"
      );

      const banner = document.getElementById("packet-delivered-banner");

      // Render the packet's path in the visualizer & animate dot
      if (isDelivered && pkt.route && pkt.route.length > 0) {
        this.mainCyView.setSourceDestination(pkt.source, pkt.destination);
        this.mainCyView.highlightFinalPath(pkt.route);

        // Animate packet dot along final route
        await this.mainCyView.animatePacketAlongPath(pkt.route);

        // Show linked-list history (R1 -> R2 -> ...) after delivery
        if (banner) {
          const llChain = pkt.history_nodes && pkt.history_nodes.length > 0
            ? pkt.history_nodes.map((n) => `<span class="badge badge-info">${n.router_id}</span>`).join(" ➔ ")
            : pkt.route.map((r) => `<span class="badge badge-info">${r}</span>`).join(" ➔ ");

          banner.style.display = "block";
          banner.innerHTML = `
            <div style="font-weight: 700; color: #065f46; margin-bottom: 4px;">
              🎉 Packet Delivered: <strong>${pkt.packet_id}</strong> (${pkt.source} ➔ ${pkt.destination} via ${pkt.algorithm})
            </div>
            <div style="font-size: 0.82rem; color: #047857; margin-bottom: 6px;">
              Total Hops: <strong>${pkt.hops}</strong> | Traversed Path: <code>${pkt.route.join(" → ")}</code>
            </div>
            <div style="font-size: 0.82rem; color: #1e293b; display: flex; align-items: center; gap: 6px; flex-wrap: wrap;">
              <strong>Singly Linked List Hop History (CO2):</strong> ${llChain}
            </div>
          `;
        }
      } else {
        if (banner) {
          banner.style.display = "block";
          banner.innerHTML = `
            <div style="font-weight: 700; color: #b91c1c;">
              ❌ Packet Dropped: <strong>${pkt.packet_id}</strong> (${pkt.source} ➔ ${pkt.destination})
            </div>
            <div style="font-size: 0.82rem; color: #991b1b;">
              Status: NO ROUTE AVAILABLE due to network partition.
            </div>
          `;
        }
      }

      await this.refreshPacketQueue();
      await this.loadPacketHistory();
      await this.updateDashboardStats();
    } catch (err) {
      console.error("Process packet error:", err);
      this.showToast("Error processing packet", "danger");
    }
  },

  async refreshPacketQueue() {
    try {
      const data = await API.getPacketQueue();
      if (!data.success) return;

      const container = document.getElementById("packet-queue-visualizer");
      if (!container) return;

      const queue = data.queue || [];
      if (queue.length === 0) {
        container.innerHTML = `
          <div class="queue-strip">
            <span class="text-muted" style="font-size: 0.82rem;">FIFO Queue is currently empty. Create a packet below.</span>
          </div>`;
        return;
      }

      let html = `<div class="queue-strip"><span class="queue-tag tag-front">FRONT (Next)</span>`;
      queue.forEach((p, idx) => {
        html += `
          <div class="queue-item" style="flex-direction: column; align-items: flex-start; padding: 6px 10px;">
            <div style="font-weight: 700; color: #1e3a8a;">${p.packet_id}</div>
            <div style="font-size: 0.72rem; color: #475569;">${p.source} → ${p.destination} (${p.algorithm})</div>
          </div>
        `;
        if (idx < queue.length - 1) {
          html += `<span style="color: #94a3b8; font-weight: bold;">→</span>`;
        }
      });
      html += `<span class="queue-tag tag-rear">REAR (Last In)</span></div>`;
      container.innerHTML = html;
    } catch (err) {
      // Silent catch
    }
  },

  // -------------------------------------------------------------
  // Packet History (Linked List View)
  // -------------------------------------------------------------
  async loadPacketHistory() {
    try {
      const data = await API.getPacketHistory();
      if (!data.success) return;

      const tbody = document.getElementById("packet-history-tbody");
      if (!tbody) return;

      const packets = data.in_memory_recent || [];
      if (packets.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-muted" style="text-align: center;">No packets processed yet.</td></tr>`;
        return;
      }

      tbody.innerHTML = packets
        .map(
          (p) => `
          <tr>
            <td><strong>${p.packet_id}</strong></td>
            <td><span class="badge badge-info">${p.source}</span> → <span class="badge badge-info">${p.destination}</span></td>
            <td><span class="badge badge-info">${p.algorithm}</span></td>
            <td>
              <span class="badge ${p.status === "DELIVERED" ? "badge-success" : "badge-danger"}">
                ${p.status}
              </span>
            </td>
            <td>${p.hops}</td>
            <td><code>${p.route_display || p.error_message || "None"}</code></td>
            <td>
              <button class="btn btn-secondary btn-sm" onclick="App.viewPacketLinkedList('${p.packet_id}')">
                View Linked List
              </button>
            </td>
          </tr>
        `
        )
        .join("");
    } catch (err) {
      console.error("Failed to load packet history:", err);
    }
  },

  async viewPacketLinkedList(packetId) {
    const data = await API.getPacketHistory();
    const packet = (data.in_memory_recent || []).find((p) => p.packet_id === packetId);
    if (!packet) return;

    const modal = document.getElementById("packet-ll-modal");
    const container = document.getElementById("packet-ll-nodes-container");
    const title = document.getElementById("packet-ll-modal-title");

    if (title) title.textContent = `Packet ${packet.packet_id} Route History (Singly Linked List)`;

    if (container) {
      const nodes = packet.history_nodes || [];
      let html = `<div class="linked-list-strip">`;
      nodes.forEach((n, idx) => {
        html += `
          <div class="ll-node">
            <span class="ll-node-num">Hop ${n.hop_number}</span>
            <span class="ll-node-val">${n.router_id}</span>
            <span style="font-size: 0.65rem; color: #64748b;">${n.metadata?.timestamp || "Active"}</span>
          </div>
        `;
        if (idx < nodes.length - 1) {
          html += `<span class="ll-arrow">→</span>`;
        }
      });
      html += `</div>`;
      html += `
        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 10px;">
          <strong>Traversal Status:</strong> ${packet.status} | <strong>Total Hops:</strong> ${packet.hops} | 
          <strong>Route Chain:</strong> <code>${packet.route_display}</code>
        </div>
      `;
      container.innerHTML = html;
    }

    if (modal) modal.classList.add("active");
  },

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("active");
  },

  // -------------------------------------------------------------
  // Failure Simulation & Dynamic Routing
  // -------------------------------------------------------------
  async handleToggleSelectedRouter() {
    const select = document.getElementById("failure-router-select");
    const routerId = select ? select.value : "R2";
    await this.toggleRouterFailure(routerId);
  },

  async toggleRouterFailure(routerId) {
    const prevRoute = this.lastComputedRoute ? [...this.lastComputedRoute] : ["R1", "R2", "R4", "R6"];
    try {
      const data = await API.toggleRouter(routerId);
      if (data.success) {
        this.showToast(data.message, data.is_active ? "success" : "warning");
        await this.refreshAllViews();

        const srcEl = document.getElementById("sim-source-select");
        const dstEl = document.getElementById("sim-dest-select");
        const src = srcEl ? srcEl.value : "R1";
        const dst = dstEl ? dstEl.value : "R6";

        const rerouteRes = await API.runBFS(src, dst);
        const alertBanner = document.getElementById("dynamic-reroute-alert");
        const statusText = document.getElementById("reroute-status-text");
        const diffBox = document.getElementById("reroute-path-comparison");

        if (rerouteRes.success && rerouteRes.route && rerouteRes.route.length > 0) {
          this.lastComputedRoute = rerouteRes.route;
          if (alertBanner) alertBanner.className = "reroute-banner reroute-success";
          if (statusText) {
            statusText.innerHTML = `Router <strong>${routerId}</strong> ${data.is_active ? "Restored" : "Failed (Light Red)"}. Dynamic Rerouting active:`;
          }
          if (diffBox) {
            diffBox.innerHTML = `
              <span class="badge badge-secondary">Old route:</span> <code>${prevRoute.join(" → ")}</code>
              <span style="font-weight: bold; margin: 0 6px;">➔</span>
              <span class="badge badge-success">New route:</span> <code>${rerouteRes.route.join(" → ")}</code> (${rerouteRes.hops} hops)
            `;
          }
          this.mainCyView.setSourceDestination(src, dst);
          this.mainCyView.highlightFinalPath(rerouteRes.route);
        } else {
          if (alertBanner) alertBanner.className = "reroute-banner reroute-failed";
          if (statusText) {
            statusText.innerHTML = `Router <strong>${routerId}</strong> Failed. ⚠️ <strong>NO ROUTE AVAILABLE</strong>`;
          }
          if (diffBox) {
            diffBox.innerHTML = `
              <span class="badge badge-secondary">Old route:</span> <code>${prevRoute.join(" → ")}</code>
              <span style="font-weight: bold; margin: 0 6px;">➔</span>
              <span class="badge badge-danger">NO ROUTE AVAILABLE</span>
            `;
          }
          this.mainCyView.resetSimulationVisuals();
        }
      }
    } catch (err) {
      console.error("Router failure error:", err);
      this.showToast("Failed to toggle router status", "danger");
    }
  },

  async toggleLinkFailure(source, target) {
    const prevRoute = this.lastComputedRoute ? [...this.lastComputedRoute] : ["R1", "R2", "R4", "R6"];
    try {
      const data = await API.toggleLink(source, target);
      if (data.success) {
        this.showToast(data.message, data.is_active ? "success" : "warning");
        await this.refreshAllViews();

        const srcEl = document.getElementById("sim-source-select");
        const dstEl = document.getElementById("sim-dest-select");
        const src = srcEl ? srcEl.value : "R1";
        const dst = dstEl ? dstEl.value : "R6";

        const rerouteRes = await API.runBFS(src, dst);
        const alertBanner = document.getElementById("dynamic-reroute-alert");
        const statusText = document.getElementById("reroute-status-text");
        const diffBox = document.getElementById("reroute-path-comparison");

        if (rerouteRes.success && rerouteRes.route && rerouteRes.route.length > 0) {
          this.lastComputedRoute = rerouteRes.route;
          if (alertBanner) alertBanner.className = "reroute-banner reroute-success";
          if (statusText) {
            statusText.innerHTML = `Link <strong>${source} ↔ ${target}</strong> ${data.is_active ? "Restored" : "Severed (Light Red)"}. Dynamic Rerouting active:`;
          }
          if (diffBox) {
            diffBox.innerHTML = `
              <span class="badge badge-secondary">Old route:</span> <code>${prevRoute.join(" → ")}</code>
              <span style="font-weight: bold; margin: 0 6px;">➔</span>
              <span class="badge badge-success">New route:</span> <code>${rerouteRes.route.join(" → ")}</code> (${rerouteRes.hops} hops)
            `;
          }
          this.mainCyView.setSourceDestination(src, dst);
          this.mainCyView.highlightFinalPath(rerouteRes.route);
        } else {
          if (alertBanner) alertBanner.className = "reroute-banner reroute-failed";
          if (statusText) {
            statusText.innerHTML = `Link <strong>${source} ↔ ${target}</strong> Severed. ⚠️ <strong>NO ROUTE AVAILABLE</strong>`;
          }
          if (diffBox) {
            diffBox.innerHTML = `
              <span class="badge badge-secondary">Old route:</span> <code>${prevRoute.join(" → ")}</code>
              <span style="font-weight: bold; margin: 0 6px;">➔</span>
              <span class="badge badge-danger">NO ROUTE AVAILABLE</span>
            `;
          }
          this.mainCyView.resetSimulationVisuals();
        }
      }
    } catch (err) {
      console.error("Link failure error:", err);
      this.showToast("Failed to toggle link status", "danger");
    }
  },

  async handleDynamicRecalculation() {
    const src = document.getElementById("failure-sim-source")?.value || "R1";
    const dst = document.getElementById("failure-sim-dest")?.value || "R6";
    const displayBox = document.getElementById("dynamic-reroute-display");

    try {
      const data = await API.runBFS(src, dst);
      if (!displayBox) return;

      if (data.success && data.route && data.route.length > 0) {
        displayBox.innerHTML = `
          <div class="alert-box alert-success" style="padding: 8px 12px; font-size: 0.8rem;">
            <strong>✅ Dynamic Route Recalculated:</strong><br>
            Active Route: <code>${data.route.join(" → ")}</code> (${data.hops} hops)
          </div>
        `;
        this.mainCyView.setSourceDestination(src, dst);
        this.mainCyView.highlightFinalPath(data.route);
      } else {
        displayBox.innerHTML = `
          <div class="alert-box alert-danger" style="padding: 8px 12px; font-size: 0.8rem;">
            <strong>⚠️ NO ROUTE AVAILABLE:</strong> Destination ${dst} unreachable from ${src}.
          </div>
        `;
        this.mainCyView.resetSimulationVisuals();
      }
    } catch (err) {
      this.showToast("Dynamic route recalculation error", "danger");
    }
  },

  // -------------------------------------------------------------
  // Traditional Routing Table
  // -------------------------------------------------------------
  async loadRoutingTableFor(routerId) {
    try {
      const data = await API.getRoutingTable(routerId);
      const tbody = document.getElementById("routing-table-tbody");
      if (!tbody || !data.success) return;

      tbody.innerHTML = data.routing_table
        .map(
          (entry) => `
          <tr>
            <td><strong>${entry.destination}</strong></td>
            <td>
              <span class="badge ${entry.next_hop === "UNREACHABLE" ? "badge-danger" : "badge-info"}">
                ${entry.next_hop}
              </span>
            </td>
            <td>${entry.hops}</td>
            <td><code>${entry.route_path.length > 0 ? entry.route_path.join(" → ") : "None"}</code></td>
            <td>
              <span class="badge ${entry.status === "Active" ? "badge-success" : "badge-danger"}">
                ${entry.status}
              </span>
            </td>
          </tr>
        `
        )
        .join("");
    } catch (err) {
      console.error("Failed to load routing table:", err);
    }
  },

  // -------------------------------------------------------------
  // Node / Edge Click Handlers
  // -------------------------------------------------------------
  async handleNodeClick(nodeData) {
    const routerId = nodeData.id;
    const select = document.getElementById("failure-router-select");
    if (select) select.value = routerId;
    // Toggling clicked router simulates hardware failure and triggers live dynamic rerouting
    await this.toggleRouterFailure(routerId);
  },

  async handleEdgeClick(edgeData) {
    // Toggling clicked edge simulates link cut and triggers live dynamic rerouting
    await this.toggleLinkFailure(edgeData.source, edgeData.target);
  },

  // -------------------------------------------------------------
  // Toast Notifications
  // -------------------------------------------------------------
  showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    if (!container) return;

    const toast = document.createElement("div");
    toast.className = "toast";

    const iconMap = {
      success: "✅",
      warning: "⚠️",
      danger: "❌",
      info: "ℹ️",
    };

    toast.innerHTML = `
      <span>${iconMap[type] || "ℹ️"}</span>
      <span style="font-size: 0.85rem; color: #1e293b;">${message}</span>
    `;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transition = "opacity 0.3s ease";
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },
};

// Initialize Application on DOM Ready
document.addEventListener("DOMContentLoaded", () => {
  App.init();
});

