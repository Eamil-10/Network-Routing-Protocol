/**
 * Cytoscape Network Visualizer Module
 * Handles interactive graph rendering, node dragging, and visual state updates.
 */

class CytoscapeView {
  constructor(containerId, options = {}) {
    this.container = document.getElementById(containerId);
    this.cy = null;
    this.onNodeClick = options.onNodeClick || null;
    this.onEdgeClick = options.onEdgeClick || null;
    this.sourceNodeId = null;
    this.destNodeId = null;
    this.init();
  }

  init() {
    if (!this.container) return;

    this.cy = cytoscape({
      container: this.container,
      boxSelectionEnabled: false,
      autounselectify: true,
      wheelSensitivity: 0.25,
      style: [
        // Default Router Node
        {
          selector: "node",
          style: {
            label: "data(label)",
            "text-valign": "center",
            "text-halign": "center",
            color: "#ffffff",
            "font-size": "13px",
            "font-weight": "700",
            "font-family": "-apple-system, BlinkMacSystemFont, sans-serif",
            width: 44,
            height: 44,
            "background-color": "#2563eb",
            "border-width": 3,
            "border-color": "#1d4ed8",
            "transition-property": "background-color, border-color, width, height, border-width",
            "transition-duration": "0.3s",
          },
        },
        // Inactive / Failed Router Node
        {
          selector: "node.disabled",
          style: {
            "background-color": "#fee2e2",
            "border-color": "#ef4444",
            "border-style": "dashed",
            "border-width": 3,
            color: "#b91c1c",
            label: "data(label) [DOWN]",
          },
        },
        // Packet Dot Animation Node
        {
          selector: "node.packet-dot-anim",
          style: {
            width: 26,
            height: 26,
            "background-color": "#fef3c7",
            "border-color": "#f59e0b",
            "border-width": 3,
            color: "#92400e",
            "font-size": "14px",
            "text-valign": "center",
            "text-halign": "center",
            "z-index": 9999,
          },
        },
        // Source Router Node
        {
          selector: "node.source",
          style: {
            "background-color": "#10b981",
            "border-color": "#047857",
            "border-width": 4,
            color: "#ffffff",
            width: 50,
            height: 50,
          },
        },
        // Destination Router Node
        {
          selector: "node.destination",
          style: {
            "background-color": "#8b5cf6",
            "border-color": "#6d28d9",
            "border-width": 4,
            color: "#ffffff",
            width: 50,
            height: 50,
          },
        },
        // Currently Processing Node in Traversal
        {
          selector: "node.current",
          style: {
            "background-color": "#f59e0b",
            "border-color": "#b45309",
            "border-width": 5,
            color: "#ffffff",
            width: 54,
            height: 54,
          },
        },
        // Queued / Stacked Node
        {
          selector: "node.queued",
          style: {
            "background-color": "#0284c7",
            "border-color": "#0369a1",
            "border-width": 3,
            color: "#ffffff",
          },
        },
        // Visited Node
        {
          selector: "node.visited",
          style: {
            "background-color": "#0d9488",
            "border-color": "#0f766e",
            "border-width": 3,
            color: "#ffffff",
          },
        },
        // Final Path Node
        {
          selector: "node.final-path",
          style: {
            "background-color": "#10b981",
            "border-color": "#064e3b",
            "border-width": 5,
            width: 52,
            height: 52,
            color: "#ffffff",
          },
        },
        // Default Communication Link
        {
          selector: "edge",
          style: {
            width: 3,
            "line-color": "#cbd5e1",
            "curve-style": "bezier",
            "transition-property": "line-color, width",
            "transition-duration": "0.3s",
          },
        },
        // Disabled / Failed Link
        {
          selector: "edge.disabled",
          style: {
            "line-color": "#ef4444",
            "line-style": "dashed",
            width: 3,
          },
        },
        // Traversed Link
        {
          selector: "edge.traversed",
          style: {
            "line-color": "#f59e0b",
            width: 4,
          },
        },
        // Final Path Link
        {
          selector: "edge.final-path",
          style: {
            "line-color": "#10b981",
            width: 6,
          },
        },
      ],
      layout: {
        name: "preset",
      },
    });

    // Node click event
    this.cy.on("tap", "node", (evt) => {
      const node = evt.target;
      if (this.onNodeClick) {
        this.onNodeClick(node.data(), evt);
      }
    });

    // Edge click event
    this.cy.on("tap", "edge", (evt) => {
      const edge = evt.target;
      if (this.onEdgeClick) {
        this.onEdgeClick(edge.data(), evt);
      }
    });
  }

  renderTopology(topology) {
    if (!this.cy) return;

    this.cy.elements().remove();

    const elements = [];

    // Add routers as nodes
    topology.routers.forEach((r) => {
      elements.push({
        group: "nodes",
        data: {
          id: r.id,
          label: r.id,
          name: r.name,
          ip: r.ip_address,
          location: r.location,
          is_active: r.is_active,
        },
        position: {
          x: r.x || Math.random() * 500 + 50,
          y: r.y || Math.random() * 350 + 50,
        },
        classes: r.is_active ? "active" : "disabled",
      });
    });

    // Add links as edges
    topology.links.forEach((l) => {
      const edgeId = `${l.source}_${l.target}`;
      elements.push({
        group: "edges",
        data: {
          id: edgeId,
          source: l.source,
          target: l.target,
          is_active: l.is_active,
        },
        classes: l.is_active ? "active" : "disabled",
      });
    });

    this.cy.add(elements);
    this.cy.fit(null, 40);
  }

  setSourceDestination(sourceId, destId) {
    this.sourceNodeId = sourceId;
    this.destNodeId = destId;
    this.refreshVisualRoles();
  }

  refreshVisualRoles() {
    if (!this.cy) return;
    this.cy.nodes().removeClass("source destination");
    if (this.sourceNodeId) {
      this.cy.$id(this.sourceNodeId).addClass("source");
    }
    if (this.destNodeId) {
      this.cy.$id(this.destNodeId).addClass("destination");
    }
  }

  resetSimulationVisuals() {
    if (!this.cy) return;
    this.cy.nodes().removeClass("current queued visited final-path");
    this.cy.edges().removeClass("traversed final-path");
    this.refreshVisualRoles();
  }

  highlightCurrentNode(nodeId) {
    if (!this.cy || !nodeId) return;
    this.cy.nodes().removeClass("current");
    this.cy.$id(nodeId).addClass("current");
  }

  highlightQueuedNode(nodeId) {
    if (!this.cy || !nodeId) return;
    const node = this.cy.$id(nodeId);
    if (!node.hasClass("source") && !node.hasClass("destination")) {
      node.addClass("queued");
    }
  }

  highlightVisitedNode(nodeId) {
    if (!this.cy || !nodeId) return;
    const node = this.cy.$id(nodeId);
    node.removeClass("current queued");
    if (!node.hasClass("source") && !node.hasClass("destination")) {
      node.addClass("visited");
    }
  }

  highlightEdgeTraversed(source, target) {
    if (!this.cy || !source || !target) return;
    const edge = this.findEdge(source, target);
    if (edge) {
      edge.addClass("traversed");
    }
  }

  highlightFinalPath(pathNodes) {
    if (!this.cy || !pathNodes || pathNodes.length === 0) return;
    this.cy.nodes().removeClass("current queued visited");

    pathNodes.forEach((nodeId) => {
      this.cy.$id(nodeId).addClass("final-path");
    });

    for (let i = 0; i < pathNodes.length - 1; i++) {
      const u = pathNodes[i];
      const v = pathNodes[i + 1];
      const edge = this.findEdge(u, v);
      if (edge) {
        edge.removeClass("traversed").addClass("final-path");
      }
    }
  }

  findEdge(u, v) {
    if (!this.cy) return null;
    let edge = this.cy.$id(`${u}_${v}`);
    if (edge.length === 0) {
      edge = this.cy.$id(`${v}_${u}`);
    }
    return edge.length > 0 ? edge : null;
  }

  fit() {
    if (this.cy) this.cy.fit(null, 40);
  }

  zoomIn() {
    if (this.cy) this.cy.zoom(this.cy.zoom() * 1.2);
  }

  zoomOut() {
    if (this.cy) this.cy.zoom(this.cy.zoom() * 0.8);
  }

  async animatePacketAlongPath(pathNodes) {
    if (!this.cy || !pathNodes || pathNodes.length < 2) return;
    const startNode = this.cy.$id(pathNodes[0]);
    if (!startNode || startNode.empty()) return;

    const dotId = "packet_dot_transiting";
    this.cy.remove(`node[id = "${dotId}"]`);

    const startPos = startNode.position();
    const dot = this.cy.add({
      group: "nodes",
      data: { id: dotId, label: "📦" },
      position: { x: startPos.x, y: startPos.y },
      classes: "packet-dot-anim",
    });

    for (let i = 1; i < pathNodes.length; i++) {
      const targetNode = this.cy.$id(pathNodes[i]);
      if (targetNode && !targetNode.empty()) {
        const targetPos = targetNode.position();
        await new Promise((resolve) => {
          dot.animate(
            { position: { x: targetPos.x, y: targetPos.y } },
            { duration: 350, complete: resolve }
          );
        });
      }
    }

    // Keep packet at destination briefly then remove
    setTimeout(() => {
      if (this.cy) this.cy.remove(`node[id = "${dotId}"]`);
    }, 400);
  }
}

