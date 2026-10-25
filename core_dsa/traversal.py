"""
Manual Graph Traversal Algorithms: BFS and DFS with Educational Tracing
========================================================================
Academic Context:
1. Breadth-First Search (BFS):
   - Explores a graph level by level using a FIFO Queue.
   - For unweighted networks, the first time BFS reaches a destination router,
     the discovered path is guaranteed to have the MINIMUM NUMBER OF HOPS (edges).
   - Time Complexity: O(V + E)
   - Space Complexity: O(V) for the queue and visited set.

2. Depth-First Search (DFS):
   - Explores as deeply as possible along each branch before backtracking using a LIFO Stack.
   - Traversal order depends on neighbor inspection order.
   - Crucial DSA lesson: DFS does NOT guarantee a minimum-hop route! It demonstrates
     deep exploration, recursion/stack management, and backtracking.
   - Time Complexity: O(V + E)
   - Space Complexity: O(V) for the stack and visited set.

No external graph libraries (such as NetworkX or SciPy) are used.
Parent pointers are explicitly recorded to demonstrate deterministic path reconstruction.
"""

import time
from typing import Dict, List, Optional, Any, Set, Tuple
from core_dsa.graph import NetworkGraph
from core_dsa.queue import CustomQueue
from core_dsa.stack import CustomStack


def reconstruct_path(
    parent_map: Dict[str, Optional[str]],
    source: str,
    destination: str
) -> Tuple[List[str], List[Dict[str, Any]]]:
    """
    Reconstruct the path from source to destination using parent pointers.
    Returns:
        - reconstructed_path: list of router IDs [source, ..., destination]
        - reconstruction_steps: list of step dictionaries showing backtracking
          from destination back to source.
    """
    if destination not in parent_map and destination != source:
        return [], []

    path_reversed: List[str] = []
    reconstruction_steps: List[Dict[str, Any]] = []

    curr: Optional[str] = destination
    step_num = 1

    while curr is not None:
        path_reversed.append(curr)
        p = parent_map.get(curr)
        reconstruction_steps.append({
            "step": step_num,
            "node": curr,
            "parent": p,
            "message": f"parent[{curr}] = {p if p is not None else 'SOURCE (None)'}"
        })
        step_num += 1
        if curr == source:
            break
        curr = p

    # If the walk did not reach source, destination was not connected
    if not path_reversed or path_reversed[-1] != source:
        return [], []

    path = list(reversed(path_reversed))
    return path, reconstruction_steps


def simulate_bfs(
    graph: NetworkGraph,
    source: str,
    destination: str
) -> Dict[str, Any]:
    """
    Execute Breadth-First Search (BFS) manually using CustomQueue.
    Generates step-by-step educational snapshots for visual playback.
    """
    start_time = time.perf_counter()

    trace_steps: List[Dict[str, Any]] = []
    parent_map: Dict[str, Optional[str]] = {}
    visited_set: Set[str] = set()
    visited_order: List[str] = []
    edges_examined = 0

    # Verification of endpoints
    if not graph.is_router_active(source):
        return {
            "success": False,
            "error": f"Source router '{source}' is either inactive or does not exist.",
            "route": [],
            "hops": 0,
            "nodes_visited": 0,
            "edges_examined": 0,
            "steps": [],
            "parent_map": {},
            "reconstruction_steps": [],
            "execution_time_ms": 0.0
        }

    if not graph.is_router_active(destination):
        return {
            "success": False,
            "error": f"Destination router '{destination}' is either inactive or does not exist.",
            "route": [],
            "hops": 0,
            "nodes_visited": 0,
            "edges_examined": 0,
            "steps": [],
            "parent_map": {},
            "reconstruction_steps": [],
            "execution_time_ms": 0.0
        }

    # Initialize FIFO Queue
    queue = CustomQueue()
    queue.enqueue(source)
    visited_set.add(source)
    visited_order.append(source)
    parent_map[source] = None

    step_counter = 1

    trace_steps.append({
        "step": step_counter,
        "action": "INITIALIZE",
        "current_node": source,
        "neighbor": None,
        "queue": queue.to_list(),
        "visited": list(visited_order),
        "parent_map": dict(parent_map),
        "message": f"Start BFS at source '{source}'. Marked as visited and enqueued into FIFO Queue."
    })
    step_counter += 1

    found = False

    # Check immediate equality
    if source == destination:
        found = True

    while not queue.is_empty() and not found:
        curr = queue.dequeue()

        trace_steps.append({
            "step": step_counter,
            "action": "DEQUEUE",
            "current_node": curr,
            "neighbor": None,
            "queue": queue.to_list(),
            "visited": list(visited_order),
            "parent_map": dict(parent_map),
            "message": f"Dequeued '{curr}' from front of FIFO queue for neighbor inspection."
        })
        step_counter += 1

        neighbors = graph.get_neighbors(curr, active_only=True)

        for nbr in neighbors:
            edges_examined += 1

            if nbr not in visited_set:
                visited_set.add(nbr)
                visited_order.append(nbr)
                parent_map[nbr] = curr
                queue.enqueue(nbr)

                trace_steps.append({
                    "step": step_counter,
                    "action": "ENQUEUE_NEIGHBOR",
                    "current_node": curr,
                    "neighbor": nbr,
                    "queue": queue.to_list(),
                    "visited": list(visited_order),
                    "parent_map": dict(parent_map),
                    "message": f"Discovered unvisited neighbor '{nbr}'. Recorded parent[{nbr}] = '{curr}'. Enqueued '{nbr}' into FIFO queue."
                })
                step_counter += 1

                if nbr == destination:
                    found = True
                    trace_steps.append({
                        "step": step_counter,
                        "action": "DESTINATION_REACHED",
                        "current_node": nbr,
                        "neighbor": None,
                        "queue": queue.to_list(),
                        "visited": list(visited_order),
                        "parent_map": dict(parent_map),
                        "message": f"Target destination '{destination}' reached! BFS guarantees this route has the minimum number of hops."
                    })
                    step_counter += 1
                    break
            else:
                trace_steps.append({
                    "step": step_counter,
                    "action": "EXAMINE_ALREADY_VISITED",
                    "current_node": curr,
                    "neighbor": nbr,
                    "queue": queue.to_list(),
                    "visited": list(visited_order),
                    "parent_map": dict(parent_map),
                    "message": f"Neighbor '{nbr}' of '{curr}' has already been visited. Skipped to prevent cycles."
                })
                step_counter += 1

    path, reconstruction_steps = reconstruct_path(parent_map, source, destination) if found else ([], [])
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 4)

    if found:
        trace_steps.append({
            "step": step_counter,
            "action": "PATH_RECONSTRUCTED",
            "current_node": destination,
            "neighbor": None,
            "queue": queue.to_list(),
            "visited": list(visited_order),
            "parent_map": dict(parent_map),
            "final_path": path,
            "message": f"Path reconstruction complete: {' → '.join(path)} ({len(path) - 1} hops)."
        })
    else:
        trace_steps.append({
            "step": step_counter,
            "action": "NO_ROUTE_FOUND",
            "current_node": None,
            "neighbor": None,
            "queue": queue.to_list(),
            "visited": list(visited_order),
            "parent_map": dict(parent_map),
            "message": f"FIFO Queue became empty without reaching '{destination}'. No route exists in the current network topology."
        })

    return {
        "success": found,
        "algorithm": "BFS",
        "source": source,
        "destination": destination,
        "route": path,
        "hops": max(0, len(path) - 1),
        "nodes_visited": len(visited_order),
        "edges_examined": edges_examined,
        "traversal_steps": len(trace_steps),
        "steps": trace_steps,
        "parent_map": parent_map,
        "reconstruction_steps": reconstruction_steps,
        "execution_time_ms": elapsed_ms,
        "dsa_justification": (
            "BFS explores the network level by level using a FIFO Queue. "
            "In an unweighted graph where all links have equal cost, the first time "
            "BFS reaches a destination, the discovered route has the MINIMUM NUMBER OF HOPS."
        )
    }


def simulate_dfs(
    graph: NetworkGraph,
    source: str,
    destination: str
) -> Dict[str, Any]:
    """
    Execute Depth-First Search (DFS) manually using an explicit CustomStack.
    Explicit stack tracking clearly demonstrates deep exploration and backtracking.
    """
    start_time = time.perf_counter()

    trace_steps: List[Dict[str, Any]] = []
    parent_map: Dict[str, Optional[str]] = {}
    visited_set: Set[str] = set()
    visited_order: List[str] = []
    backtrack_count = 0
    edges_examined = 0

    if not graph.is_router_active(source):
        return {
            "success": False,
            "error": f"Source router '{source}' is either inactive or does not exist.",
            "route": [],
            "hops": 0,
            "nodes_visited": 0,
            "edges_examined": 0,
            "steps": [],
            "parent_map": {},
            "reconstruction_steps": [],
            "backtracking_count": 0,
            "execution_time_ms": 0.0
        }

    if not graph.is_router_active(destination):
        return {
            "success": False,
            "error": f"Destination router '{destination}' is either inactive or does not exist.",
            "route": [],
            "hops": 0,
            "nodes_visited": 0,
            "edges_examined": 0,
            "steps": [],
            "parent_map": {},
            "reconstruction_steps": [],
            "backtracking_count": 0,
            "execution_time_ms": 0.0
        }

    # Initialize LIFO Stack
    # We store tuples of (router_id, parent_id)
    stack = CustomStack()
    stack.push(source)
    parent_map[source] = None

    step_counter = 1

    trace_steps.append({
        "step": step_counter,
        "action": "INITIALIZE",
        "current_node": source,
        "neighbor": None,
        "stack": stack.to_list(),
        "visited": list(visited_order),
        "parent_map": dict(parent_map),
        "is_backtracking": False,
        "message": f"Start DFS at source '{source}'. Pushed '{source}' onto LIFO Stack."
    })
    step_counter += 1

    found = False

    while not stack.is_empty():
        curr = stack.pop()

        if curr not in visited_set:
            visited_set.add(curr)
            visited_order.append(curr)

            trace_steps.append({
                "step": step_counter,
                "action": "POP_VISIT",
                "current_node": curr,
                "neighbor": None,
                "stack": stack.to_list(),
                "visited": list(visited_order),
                "parent_map": dict(parent_map),
                "is_backtracking": False,
                "message": f"Popped '{curr}' from top of LIFO Stack and marked as VISITED."
            })
            step_counter += 1

            if curr == destination:
                found = True
                trace_steps.append({
                    "step": step_counter,
                    "action": "DESTINATION_REACHED",
                    "current_node": curr,
                    "neighbor": None,
                    "stack": stack.to_list(),
                    "visited": list(visited_order),
                    "parent_map": dict(parent_map),
                    "is_backtracking": False,
                    "message": f"Destination '{destination}' reached via DFS! Note: DFS does not guarantee minimum hops."
                })
                step_counter += 1
                break

            neighbors = graph.get_neighbors(curr, active_only=True)
            # Push unvisited neighbors in reverse order so smaller IDs are popped first
            unvisited_neighbors = [nbr for nbr in neighbors if nbr not in visited_set]

            if not unvisited_neighbors and not stack.is_empty():
                # Dead end reached! Backtracking will occur on next pop
                backtrack_count += 1
                next_in_stack = stack.peek()
                trace_steps.append({
                    "step": step_counter,
                    "action": "DEAD_END_BACKTRACK",
                    "current_node": curr,
                    "neighbor": None,
                    "stack": stack.to_list(),
                    "visited": list(visited_order),
                    "parent_map": dict(parent_map),
                    "is_backtracking": True,
                    "backtrack_from": curr,
                    "backtrack_to": next_in_stack,
                    "message": f"Dead End at '{curr}': no unvisited neighbors. Backtracking up the stack toward '{next_in_stack}'."
                })
                step_counter += 1

            for nbr in reversed(neighbors):
                edges_examined += 1
                if nbr not in visited_set:
                    # Update parent pointer if not set or set from current exploration
                    parent_map[nbr] = curr
                    stack.push(nbr)
                    trace_steps.append({
                        "step": step_counter,
                        "action": "PUSH_NEIGHBOR",
                        "current_node": curr,
                        "neighbor": nbr,
                        "stack": stack.to_list(),
                        "visited": list(visited_order),
                        "parent_map": dict(parent_map),
                        "is_backtracking": False,
                        "message": f"Discovered unvisited neighbor '{nbr}'. Pushed onto LIFO Stack (recorded parent[{nbr}] = '{curr}')."
                    })
                    step_counter += 1

    path, reconstruction_steps = reconstruct_path(parent_map, source, destination) if found else ([], [])
    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 4)

    if found:
        trace_steps.append({
            "step": step_counter,
            "action": "PATH_RECONSTRUCTED",
            "current_node": destination,
            "neighbor": None,
            "stack": stack.to_list(),
            "visited": list(visited_order),
            "parent_map": dict(parent_map),
            "final_path": path,
            "is_backtracking": False,
            "message": f"DFS Route discovered: {' → '.join(path)} ({len(path) - 1} hops)."
        })
    else:
        trace_steps.append({
            "step": step_counter,
            "action": "NO_ROUTE_FOUND",
            "current_node": None,
            "neighbor": None,
            "stack": stack.to_list(),
            "visited": list(visited_order),
            "parent_map": dict(parent_map),
            "is_backtracking": False,
            "message": f"LIFO Stack exhausted without reaching destination '{destination}'. Destination unreachable."
        })

    return {
        "success": found,
        "algorithm": "DFS",
        "source": source,
        "destination": destination,
        "route": path,
        "hops": max(0, len(path) - 1),
        "nodes_visited": len(visited_order),
        "edges_examined": edges_examined,
        "traversal_steps": len(trace_steps),
        "backtracking_count": backtrack_count,
        "steps": trace_steps,
        "parent_map": parent_map,
        "reconstruction_steps": reconstruction_steps,
        "execution_time_ms": elapsed_ms,
        "dsa_justification": (
            "DFS explores one path deeply before backtracking using a LIFO Stack. "
            "The resulting route depends strictly on traversal order and is NOT guaranteed "
            "to have the minimum number of hops."
        )
    }
