/**
 * API Client Module for Network Routing Simulator
 * Handles communication with Flask REST endpoints.
 */

const API = {
  // Topology and Graph Management
  async getTopology() {
    const res = await fetch("/api/topology");
    return res.json();
  },

  async loadScenario(scenarioId) {
    const res = await fetch("/api/topology/load-scenario", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ scenario_id: scenarioId }),
    });
    return res.json();
  },

  async resetTopology() {
    const res = await fetch("/api/topology/reset", { method: "POST" });
    return res.json();
  },

  async addRouter(routerData) {
    const res = await fetch("/api/router/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(routerData),
    });
    return res.json();
  },

  async toggleRouter(routerId, isActive = null) {
    const res = await fetch("/api/router/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: routerId, is_active: isActive }),
    });
    return res.json();
  },

  async deleteRouter(routerId) {
    const res = await fetch(`/api/router/${routerId}`, { method: "DELETE" });
    return res.json();
  },

  async addLink(source, target) {
    const res = await fetch("/api/link/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, target }),
    });
    return res.json();
  },

  async toggleLink(source, target, isActive = null) {
    const res = await fetch("/api/link/toggle", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, target, is_active: isActive }),
    });
    return res.json();
  },

  async deleteLink(source, target) {
    const res = await fetch("/api/link", {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, target }),
    });
    return res.json();
  },

  // Traversal Simulations (BFS & DFS)
  async runBFS(source, destination) {
    const res = await fetch("/api/simulate/bfs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });
    return res.json();
  },

  async runDFS(source, destination) {
    const res = await fetch("/api/simulate/dfs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });
    return res.json();
  },

  async compareTraversals(source, destination) {
    const res = await fetch("/api/simulate/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });
    return res.json();
  },

  // Search Module
  async searchLinear(targetId) {
    const res = await fetch("/api/search/linear", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_id: targetId }),
    });
    return res.json();
  },

  async searchBinary(targetId) {
    const res = await fetch("/api/search/binary", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_id: targetId }),
    });
    return res.json();
  },

  async searchCompare(targetId) {
    const res = await fetch("/api/search/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_id: targetId }),
    });
    return res.json();
  },

  // Routing Table
  async getRoutingTable(routerId) {
    const res = await fetch(`/api/routing-table/${routerId}`);
    return res.json();
  },

  async forwardViaTable(source, destination) {
    const res = await fetch("/api/routing-table/forward", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination }),
    });
    return res.json();
  },

  // Packet Buffer & FIFO Queue
  async createPacket(source, destination, algorithm) {
    const res = await fetch("/api/packets/create", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source, destination, algorithm }),
    });
    return res.json();
  },

  async getPacketQueue() {
    const res = await fetch("/api/packets/queue");
    return res.json();
  },

  async processNextPacket() {
    const res = await fetch("/api/packets/process-next", { method: "POST" });
    return res.json();
  },

  async getPacketHistory() {
    const res = await fetch("/api/packets/history");
    return res.json();
  },

  // Dashboard & Scenarios
  async getDashboardStats() {
    const res = await fetch("/api/dashboard/stats");
    return res.json();
  },

  async listScenarios() {
    const res = await fetch("/api/scenarios");
    return res.json();
  },
};
