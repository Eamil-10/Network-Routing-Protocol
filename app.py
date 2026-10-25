"""
Network Routing Simulator - Flask Web Application
==================================================
Academic Context:
A demonstration platform for Data Structures and Graph Traversal Algorithms:
- Graph (Adjacency List & Matrix)
- FIFO Queue (Breadth-First Search & Packet Buffer)
- LIFO Stack (Depth-First Search & Backtracking)
- Singly Linked List (Packet Route History)
- Linear Search vs Binary Search ($O(n)$ vs $O(\\log n)$)
- Dynamic Routing Recalculation on Router/Link Failure
- Routing Table Forwarding Simulation

Built strictly without third-party graph traversal or shortest-path libraries.
"""

import os
from flask import Flask, render_template, request, jsonify
from core_dsa.graph import NetworkGraph
from core_dsa.traversal import simulate_bfs, simulate_dfs
from core_dsa.search import linear_search_routers, binary_search_routers
from core_dsa.routing_table import generate_routing_table, simulate_table_forwarding
from core_dsa.packet import PacketQueueManager
from database.db import (
    init_db,
    get_all_scenarios,
    get_scenario_by_id,
    log_packet_transmission,
    log_activity,
    get_recent_activities,
    get_packet_history_from_db
)
from database.seed_data import PRESET_SCENARIOS

app = Flask(__name__)
app.config["SECRET_KEY"] = "dsa-network-routing-simulator-secret-2026"

# Global runtime state
active_graph = NetworkGraph()
packet_manager = PacketQueueManager()
current_scenario_id = "default_mesh"


def load_scenario_into_graph(scenario_id: str) -> bool:
    """Load a network topology into the active NetworkGraph instance."""
    global current_scenario_id, active_graph
    scenario = get_scenario_by_id(scenario_id)
    if not scenario and scenario_id in PRESET_SCENARIOS:
        scenario = PRESET_SCENARIOS[scenario_id]

    if not scenario:
        return False

    active_graph.clear()
    current_scenario_id = scenario_id

    for r in scenario["routers"]:
        active_graph.add_router(
            router_id=r["id"],
            name=r.get("name", ""),
            ip_address=r.get("ip_address", ""),
            location=r.get("location", ""),
            x=r.get("x", 0.0),
            y=r.get("y", 0.0),
            is_active=r.get("is_active", True)
        )

    for l in scenario["links"]:
        active_graph.add_link(
            source=l["source"],
            target=l["target"],
            is_active=l.get("is_active", True)
        )

    log_activity("TOPOLOGY_LOAD", f"Loaded topology scenario '{scenario['name']}'.")
    return True


# Initialize database and load default scenario on startup
with app.app_context():
    init_db()
    load_scenario_into_graph("default_mesh")


# ---------------------------------------------------------
# HTML Views
# ---------------------------------------------------------

@app.route("/")
def index():
    """Main single-page application dashboard and visualizer."""
    return render_template("index.html")


# ---------------------------------------------------------
# REST API: Topology & Graph Management
# ---------------------------------------------------------

@app.route("/api/topology", methods=["GET"])
def get_topology():
    """Return complete current graph representation (routers, links, adj list, adj matrix)."""
    return jsonify({
        "success": True,
        "scenario_id": current_scenario_id,
        "topology": active_graph.to_dict()
    })


@app.route("/api/topology/load-scenario", methods=["POST"])
def load_scenario():
    """Load one of the predefined network scenarios."""
    data = request.get_json() or {}
    scenario_id = data.get("scenario_id", "default_mesh")
    success = load_scenario_into_graph(scenario_id)
    if not success:
        return jsonify({"success": False, "error": f"Scenario '{scenario_id}' not found."}), 404

    return jsonify({
        "success": True,
        "message": f"Successfully loaded scenario '{scenario_id}'.",
        "topology": active_graph.to_dict()
    })


@app.route("/api/topology/reset", methods=["POST"])
def reset_topology():
    """Reset current scenario to original state."""
    load_scenario_into_graph(current_scenario_id)
    return jsonify({
        "success": True,
        "message": f"Scenario '{current_scenario_id}' reset to default state.",
        "topology": active_graph.to_dict()
    })


@app.route("/api/router/add", methods=["POST"])
def add_router():
    """Add a new router vertex to the graph."""
    data = request.get_json() or {}
    router_id = data.get("id", "").strip().upper()
    if not router_id:
        return jsonify({"success": False, "error": "Router ID is required."}), 400

    r = active_graph.add_router(
        router_id=router_id,
        name=data.get("name", f"Router {router_id}"),
        ip_address=data.get("ip_address", ""),
        location=data.get("location", "Custom Node"),
        x=float(data.get("x", 300)),
        y=float(data.get("y", 200)),
        is_active=data.get("is_active", True)
    )

    log_activity("ROUTER_ADD", f"Added router vertex '{router_id}'.")
    return jsonify({
        "success": True,
        "router": r.to_dict(),
        "topology": active_graph.to_dict()
    })


@app.route("/api/router/toggle", methods=["POST"])
def toggle_router():
    """Enable or disable a router (failure simulation)."""
    data = request.get_json() or {}
    router_id = data.get("id", "").strip().upper()
    is_active = data.get("is_active")

    if router_id not in active_graph.routers:
        return jsonify({"success": False, "error": f"Router '{router_id}' does not exist."}), 404

    if is_active is None:
        is_active = not active_graph.is_router_active(router_id)

    active_graph.set_router_status(router_id, is_active)
    status_str = "ENABLED (ACTIVE)" if is_active else "FAILED (DISABLED)"
    log_activity("ROUTER_STATUS", f"Router '{router_id}' status changed to {status_str}.")

    return jsonify({
        "success": True,
        "router_id": router_id,
        "is_active": is_active,
        "message": f"Router '{router_id}' is now {status_str}.",
        "topology": active_graph.to_dict()
    })


@app.route("/api/router/<router_id>", methods=["DELETE"])
def delete_router(router_id: str):
    """Delete a router and all its links from the graph."""
    r_id = router_id.strip().upper()
    success = active_graph.remove_router(r_id)
    if not success:
        return jsonify({"success": False, "error": f"Router '{r_id}' not found."}), 404

    log_activity("ROUTER_DELETE", f"Deleted router '{r_id}' and connected links.")
    return jsonify({
        "success": True,
        "message": f"Router '{r_id}' deleted.",
        "topology": active_graph.to_dict()
    })


@app.route("/api/link/add", methods=["POST"])
def add_link():
    """Add a communication link between two routers."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    target = data.get("target", "").strip().upper()

    if not source or not target:
        return jsonify({"success": False, "error": "Both source and target router IDs are required."}), 400

    link = active_graph.add_link(source, target, is_active=True)
    if not link:
        return jsonify({"success": False, "error": "Invalid link endpoints or self-loop."}), 400

    log_activity("LINK_ADD", f"Created link '{source} ↔ {target}'.")
    return jsonify({
        "success": True,
        "link": link.to_dict(),
        "topology": active_graph.to_dict()
    })


@app.route("/api/link/toggle", methods=["POST"])
def toggle_link():
    """Enable or disable a communication link (link failure simulation)."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    target = data.get("target", "").strip().upper()
    is_active = data.get("is_active")

    if not active_graph.link_exists(source, target):
        return jsonify({"success": False, "error": f"Link '{source} ↔ {target}' does not exist."}), 404

    u, v = sorted([source, target])
    curr_link = active_graph.links[(u, v)]
    if is_active is None:
        is_active = not curr_link.is_active

    active_graph.set_link_status(source, target, is_active)
    status_str = "RESTORED (ACTIVE)" if is_active else "FAILED (DISABLED)"
    log_activity("LINK_STATUS", f"Link '{source} ↔ {target}' changed to {status_str}.")

    return jsonify({
        "success": True,
        "source": source,
        "target": target,
        "is_active": is_active,
        "message": f"Link '{source} ↔ {target}' is now {status_str}.",
        "topology": active_graph.to_dict()
    })


@app.route("/api/link", methods=["DELETE"])
def delete_link():
    """Permanently remove a communication link."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    target = data.get("target", "").strip().upper()

    success = active_graph.remove_link(source, target)
    if not success:
        return jsonify({"success": False, "error": f"Link '{source} ↔ {target}' not found."}), 404

    log_activity("LINK_DELETE", f"Removed link '{source} ↔ {target}'.")
    return jsonify({
        "success": True,
        "message": f"Link '{source} ↔ {target}' deleted.",
        "topology": active_graph.to_dict()
    })


# ---------------------------------------------------------
# REST API: Traversal Simulation (BFS & DFS)
# ---------------------------------------------------------

@app.route("/api/simulate/bfs", methods=["POST"])
def run_bfs():
    """Execute manual BFS and generate step-by-step traversal snapshots."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    destination = data.get("destination", "").strip().upper()

    result = simulate_bfs(active_graph, source, destination)
    log_activity("BFS_SIMULATION", f"Ran BFS from {source} to {destination}: {'Found' if result['success'] else 'No Route'}.")
    return jsonify(result)


@app.route("/api/simulate/dfs", methods=["POST"])
def run_dfs():
    """Execute manual DFS and generate step-by-step traversal snapshots."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    destination = data.get("destination", "").strip().upper()

    result = simulate_dfs(active_graph, source, destination)
    log_activity("DFS_SIMULATION", f"Ran DFS from {source} to {destination}: {'Found' if result['success'] else 'No Route'}.")
    return jsonify(result)


@app.route("/api/simulate/compare", methods=["POST"])
def compare_traversals():
    """Run both BFS and DFS on the same network state and return comparison."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    destination = data.get("destination", "").strip().upper()

    bfs_res = simulate_bfs(active_graph, source, destination)
    dfs_res = simulate_dfs(active_graph, source, destination)

    return jsonify({
        "source": source,
        "destination": destination,
        "bfs": {
            "success": bfs_res["success"],
            "route": bfs_res["route"],
            "hops": bfs_res["hops"],
            "nodes_visited": bfs_res["nodes_visited"],
            "edges_examined": bfs_res["edges_examined"],
            "traversal_steps": bfs_res["traversal_steps"],
            "execution_time_ms": bfs_res["execution_time_ms"],
            "dsa_justification": bfs_res["dsa_justification"]
        },
        "dfs": {
            "success": dfs_res["success"],
            "route": dfs_res["route"],
            "hops": dfs_res["hops"],
            "nodes_visited": dfs_res["nodes_visited"],
            "edges_examined": dfs_res["edges_examined"],
            "traversal_steps": dfs_res["traversal_steps"],
            "backtracking_count": dfs_res.get("backtracking_count", 0),
            "execution_time_ms": dfs_res["execution_time_ms"],
            "dsa_justification": dfs_res["dsa_justification"]
        },
        "analysis": {
            "minimum_hop_guarantee": "BFS provides the minimum-hop route in an unweighted graph.",
            "hop_difference": (dfs_res["hops"] - bfs_res["hops"]) if (bfs_res["success"] and dfs_res["success"]) else "N/A",
            "backtracking_noted": f"DFS performed {dfs_res.get('backtracking_count', 0)} backtrack step(s) using its LIFO stack."
        }
    })


# ---------------------------------------------------------
# REST API: Router Search (Linear vs Binary)
# ---------------------------------------------------------

@app.route("/api/search/linear", methods=["POST"])
def search_linear():
    """Perform sequential Linear Search on the router directory."""
    data = request.get_json() or {}
    target_id = data.get("target_id", "").strip().upper()
    routers = [r.to_dict() for r in active_graph.routers.values()]

    result = linear_search_routers(routers, target_id)
    return jsonify(result)


@app.route("/api/search/binary", methods=["POST"])
def search_binary():
    """Perform manual Binary Search on sorted router records."""
    data = request.get_json() or {}
    target_id = data.get("target_id", "").strip().upper()
    routers = [r.to_dict() for r in active_graph.routers.values()]

    result = binary_search_routers(routers, target_id)
    return jsonify(result)


@app.route("/api/search/compare", methods=["POST"])
def search_compare():
    """Compare Linear Search and Binary Search side-by-side."""
    data = request.get_json() or {}
    target_id = data.get("target_id", "").strip().upper()
    routers = [r.to_dict() for r in active_graph.routers.values()]

    linear_res = linear_search_routers(routers, target_id)
    binary_res = binary_search_routers(routers, target_id)

    return jsonify({
        "target_id": target_id,
        "total_elements": len(routers),
        "linear": linear_res,
        "binary": binary_res,
        "comparison_analysis": {
            "comparison_difference": linear_res["comparisons"] - binary_res["comparisons"],
            "linear_complexity": "O(n)",
            "binary_complexity": "O(log n)",
            "explanation": (
                f"For target '{target_id}', Linear Search performed {linear_res['comparisons']} comparison(s) "
                f"while Binary Search required only {binary_res['comparisons']} comparison(s). "
                f"Comparisons provide an unambiguous theoretical metric independent of CPU timing jitter."
            )
        }
    })


# ---------------------------------------------------------
# REST API: Routing Table & Forwarding
# ---------------------------------------------------------

@app.route("/api/routing-table/<router_id>", methods=["GET"])
def get_routing_table(router_id: str):
    """Generate forwarding table for a specific router."""
    r_id = router_id.strip().upper()
    if r_id not in active_graph.routers:
        return jsonify({"success": False, "error": f"Router '{r_id}' not found."}), 404

    table = generate_routing_table(active_graph, r_id)
    return jsonify({
        "success": True,
        "router_id": r_id,
        "is_active": active_graph.is_router_active(r_id),
        "routing_table": table,
        "concept_explanation": (
            "A routing table maps each network destination to the immediate 'Next Hop'. "
            "Unlike graph traversal on every packet, table lookup is direct, "
            "but requires recomputation when topology changes."
        )
    })


@app.route("/api/routing-table/forward", methods=["POST"])
def forward_via_table():
    """Simulate packet forwarding using stored routing tables."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    destination = data.get("destination", "").strip().upper()

    result = simulate_table_forwarding(active_graph, source, destination)
    return jsonify(result)


# ---------------------------------------------------------
# REST API: Packet Management & Queue (FIFO & Linked List)
# ---------------------------------------------------------

@app.route("/api/packets/create", methods=["POST"])
def create_packet():
    """Create a new packet and place it into the FIFO packet queue."""
    data = request.get_json() or {}
    source = data.get("source", "").strip().upper()
    destination = data.get("destination", "").strip().upper()
    algorithm = data.get("algorithm", "BFS").strip().upper()

    if not source or not destination:
        return jsonify({"success": False, "error": "Source and destination are required."}), 400

    packet = packet_manager.enqueue_packet(source, destination, algorithm)
    log_activity("PACKET_CREATE", f"Packet {packet.packet_id} enqueued ({source} → {destination} via {algorithm}).")

    return jsonify({
        "success": True,
        "packet": packet.to_dict(),
        "queue_size": packet_manager.queue.size(),
        "queue": packet_manager.get_queue_view()
    })


@app.route("/api/packets/queue", methods=["GET"])
def get_packet_queue():
    """Return all packets currently awaiting routing in the FIFO queue."""
    return jsonify({
        "success": True,
        "queue": packet_manager.get_queue_view(),
        "queue_size": packet_manager.queue.size()
    })


@app.route("/api/packets/process-next", methods=["POST"])
def process_next_packet():
    """Dequeue front packet from FIFO queue, route it, and record in linked list."""
    if packet_manager.queue.is_empty():
        return jsonify({"success": False, "error": "Packet queue is currently empty."}), 400

    result = packet_manager.dequeue_and_process(active_graph)
    if not result:
        return jsonify({"success": False, "error": "Failed to process packet."}), 500

    pkt = result["packet"]
    # Persist in SQLite
    log_packet_transmission({
        "packet_id": pkt["packet_id"],
        "source": pkt["source"],
        "destination": pkt["destination"],
        "algorithm": pkt["algorithm"],
        "status": pkt["status"],
        "route": pkt["route"],
        "hops": pkt["hops"],
        "nodes_visited": pkt["nodes_visited"],
        "execution_time_ms": result["simulation"].get("execution_time_ms", 0.0)
    })

    log_activity(
        "PACKET_DELIVERED" if pkt["status"] == "DELIVERED" else "PACKET_FAILED",
        f"Packet {pkt['packet_id']} {pkt['status'].lower()}: {pkt['route_display'] or pkt['error_message']}"
    )

    return jsonify({
        "success": True,
        "packet": pkt,
        "simulation": result["simulation"],
        "queue_size": packet_manager.queue.size(),
        "stats": packet_manager.stats()
    })


@app.route("/api/packets/history", methods=["GET"])
def get_packet_history():
    """Return packet history with linked list nodes and audit status."""
    in_memory = packet_manager.get_all_history()
    db_history = get_packet_history_from_db(limit=50)

    return jsonify({
        "success": True,
        "in_memory_recent": in_memory,
        "database_history": db_history,
        "stats": packet_manager.stats()
    })


# ---------------------------------------------------------
# REST API: Dashboard Stats & Scenarios
# ---------------------------------------------------------

@app.route("/api/dashboard/stats", methods=["GET"])
def get_dashboard_stats():
    """Return consolidated metrics for the dashboard cards and activity feed."""
    topo_dict = active_graph.to_dict()
    q_stats = packet_manager.stats()
    recent_logs = get_recent_activities(limit=10)

    return jsonify({
        "success": True,
        "total_routers": topo_dict["total_routers"],
        "active_routers": topo_dict["active_routers"],
        "total_links": topo_dict["total_links"],
        "active_links": topo_dict["active_links"],
        "packets_in_queue": q_stats["in_queue"],
        "delivered_packets": q_stats["delivered"],
        "failed_packets": q_stats["failed"],
        "recent_activities": recent_logs,
        "current_scenario": current_scenario_id
    })


@app.route("/api/scenarios", methods=["GET"])
def list_scenarios():
    """List all available predefined test topologies."""
    scenarios = get_all_scenarios()
    return jsonify({
        "success": True,
        "scenarios": scenarios
    })


def find_available_port(start_port: int = 5000) -> int:
    """Find the first available TCP port on localhost starting from start_port."""
    import socket
    for p in range(start_port, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    return start_port


if __name__ == "__main__":
    requested_port = int(os.environ.get("PORT", 5000))
    port = find_available_port(requested_port)
    os.environ["PORT"] = str(port)

    if port != requested_port:
        print(
            f"\n[Notice] Port {requested_port} is occupied (common on macOS due to AirPlay Receiver).\n"
            f"         Automatically serving on: http://127.0.0.1:{port}\n"
        )

    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)


