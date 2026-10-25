"""
Traditional Routing Table Generator & Forwarding Simulator
==========================================================
Academic Context:
In traditional computer networks (e.g. IP routing), routers maintain a Forwarding Information
Base (Routing Table). When a packet arrives, the router inspects the packet's destination IP/ID,
looks up the table, and forwards the packet out the designated interface to the 'Next Hop'.

Key Educational Concepts:
1. Routing Table:
   - Maps Destination -> Next Hop -> Hop Count -> Status
   - Provides direct O(1) or prefix-lookup forwarding at packet arrival time.
2. Graph-Based Routing vs Table-Based Forwarding:
   - Graph Routing: Discovers paths dynamically by traversing topology (BFS/DFS).
     High computation overhead on every packet if done without caching.
   - Table-Based Routing: Traversal or distance-vector/link-state protocols pre-populate
     the table. Forwarding is instantaneous lookup, but tables MUST be updated when links fail.
"""

from typing import Dict, List, Any, Optional
from core_dsa.graph import NetworkGraph
from core_dsa.queue import CustomQueue


def generate_routing_table(graph: NetworkGraph, router_id: str) -> List[Dict[str, Any]]:
    """
    Generate a traditional next-hop routing table for a given router
    by computing minimum-hop paths using manual BFS.
    """
    if not graph.is_router_active(router_id):
        return []

    destinations = sorted([
        r for r in graph.routers.keys()
        if r != router_id
    ])

    table: List[Dict[str, Any]] = []

    for dest in destinations:
        # Check if dest router is active
        if not graph.is_router_active(dest):
            table.append({
                "destination": dest,
                "next_hop": "UNREACHABLE",
                "hops": "∞",
                "status": "Inactive Router",
                "route_path": []
            })
            continue

        # Run manual BFS from router_id to dest
        queue = CustomQueue()
        queue.enqueue(router_id)
        visited = {router_id}
        parent_map: Dict[str, Optional[str]] = {router_id: None}
        reached = False

        while not queue.is_empty():
            curr = queue.dequeue()
            if curr == dest:
                reached = True
                break

            for nbr in graph.get_neighbors(curr, active_only=True):
                if nbr not in visited:
                    visited.add(nbr)
                    parent_map[nbr] = curr
                    queue.enqueue(nbr)

        if reached:
            # Reconstruct path
            path = []
            curr: Optional[str] = dest
            while curr is not None:
                path.append(curr)
                curr = parent_map.get(curr)
            path.reverse()

            # Next hop is the second node in path
            next_hop = path[1] if len(path) > 1 else dest
            hops = len(path) - 1

            table.append({
                "destination": dest,
                "next_hop": next_hop,
                "hops": hops,
                "status": "Active",
                "route_path": path
            })
        else:
            table.append({
                "destination": dest,
                "next_hop": "UNREACHABLE",
                "hops": "∞",
                "status": "No Route (Partitioned)",
                "route_path": []
            })

    return table


def simulate_table_forwarding(
    graph: NetworkGraph,
    source: str,
    destination: str,
    max_hops: int = 20
) -> Dict[str, Any]:
    """
    Simulate packet forwarding hop-by-hop using pre-computed routing tables.
    Demonstrates how real routers forward packets next-hop by next-hop.
    """
    if not graph.is_router_active(source) or not graph.is_router_active(destination):
        return {
            "success": False,
            "path": [],
            "error": "Source or destination router is inactive."
        }

    path = [source]
    curr = source
    hops = 0
    visited = {source}

    while curr != destination and hops < max_hops:
        rt = generate_routing_table(graph, curr)
        dest_entry = next((entry for entry in rt if entry["destination"] == destination), None)

        if not dest_entry or dest_entry["next_hop"] == "UNREACHABLE":
            return {
                "success": False,
                "path": path,
                "hops": hops,
                "error": f"Forwarding loop or dead end encountered at router {curr}."
            }

        next_hop = dest_entry["next_hop"]
        if next_hop in visited:
            # Routing loop detected
            return {
                "success": False,
                "path": path + [next_hop],
                "hops": hops + 1,
                "error": f"Routing loop detected between {curr} and {next_hop}."
            }

        path.append(next_hop)
        visited.add(next_hop)
        curr = next_hop
        hops += 1

    return {
        "success": (curr == destination),
        "path": path,
        "hops": hops,
        "destination_reached": (curr == destination)
    }
