"""
Custom Graph Data Structure for Network Packet Routing
======================================================
Academic Context:
A Graph G = (V, E) consists of a set of vertices V (routers) and edges E (communication links).
In this educational simulator, the network is modeled as an unweighted, undirected graph.

Data Structure Representations Implemented:
1. Adjacency List:
   - Maps each vertex v in V to a list/set of neighboring vertices.
   - Space Complexity: O(V + E)
   - Efficient for sparse networks and graph traversals.
2. Adjacency Matrix:
   - A 2D square matrix of size |V| x |V|, where M[i][j] = 1 if an edge connects
     router i and router j, and 0 otherwise.
   - Space Complexity: O(V^2)
   - Allows O(1) edge existence queries.

Failure Simulation Support:
- Routers and links maintain operational status flags (active/disabled).
- Traversal algorithms query active neighbors, dynamically responding to hardware faults.
"""

from typing import Dict, List, Set, Tuple, Optional, Any


class Router:
    """Represents a Network Router (Vertex in the graph)."""

    def __init__(
        self,
        router_id: str,
        name: str = "",
        ip_address: str = "",
        location: str = "",
        x: float = 0.0,
        y: float = 0.0,
        is_active: bool = True
    ):
        self.id: str = router_id
        self.name: str = name or f"Router {router_id}"
        self.ip_address: str = ip_address or f"192.168.1.{hash(router_id) % 254 + 1}"
        self.location: str = location or "Data Center Core"
        self.x: float = x
        self.y: float = y
        self.is_active: bool = is_active

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "ip_address": self.ip_address,
            "location": self.location,
            "x": self.x,
            "y": self.y,
            "is_active": self.is_active
        }


class Link:
    """Represents a Communication Link (Edge in the graph)."""

    def __init__(self, source: str, target: str, is_active: bool = True):
        # Normalize undirected edge tuple (alphabetical order)
        u, v = sorted([source, target])
        self.source: str = u
        self.target: str = v
        self.is_active: bool = is_active

    @property
    def edge_key(self) -> Tuple[str, str]:
        return (self.source, self.target)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "is_active": self.is_active
        }


class NetworkGraph:
    """
    Manual Graph implementation representing the computer network topology.
    Does NOT use NetworkX or external graph libraries.
    """

    def __init__(self):
        self.routers: Dict[str, Router] = {}
        self.links: Dict[Tuple[str, str], Link] = {}
        # Adjacency list: router_id -> list of neighbor router_ids
        self._adj_list: Dict[str, List[str]] = {}

    def add_router(
        self,
        router_id: str,
        name: str = "",
        ip_address: str = "",
        location: str = "",
        x: float = 0.0,
        y: float = 0.0,
        is_active: bool = True
    ) -> Router:
        """Add a router vertex to the graph."""
        if router_id not in self.routers:
            self.routers[router_id] = Router(
                router_id=router_id,
                name=name,
                ip_address=ip_address,
                location=location,
                x=x,
                y=y,
                is_active=is_active
            )
            self._adj_list[router_id] = []
        else:
            # Update attributes if already present
            router = self.routers[router_id]
            if name: router.name = name
            if ip_address: router.ip_address = ip_address
            if location: router.location = location
            if x != 0.0 or y != 0.0:
                router.x = x
                router.y = y
            router.is_active = is_active
        return self.routers[router_id]

    def remove_router(self, router_id: str) -> bool:
        """Remove a router vertex and all connected links from the graph."""
        if router_id not in self.routers:
            return False

        # Remove all incident edges
        links_to_remove = [
            key for key in self.links.keys()
            if router_id in key
        ]
        for key in links_to_remove:
            u, v = key
            self.remove_link(u, v)

        # Remove from adjacency list
        del self._adj_list[router_id]
        # Remove from router dictionary
        del self.routers[router_id]
        return True

    def add_link(self, source: str, target: str, is_active: bool = True) -> Optional[Link]:
        """Add an undirected communication link between two routers."""
        if source not in self.routers or target not in self.routers:
            return None
        if source == target:
            return None  # No self-loops in standard packet routing

        u, v = sorted([source, target])
        link = Link(u, v, is_active=is_active)
        self.links[(u, v)] = link

        # Maintain undirected adjacency list
        if target not in self._adj_list[source]:
            self._adj_list[source].append(target)
            self._adj_list[source].sort()

        if source not in self._adj_list[target]:
            self._adj_list[target].append(source)
            self._adj_list[target].sort()

        return link

    def remove_link(self, source: str, target: str) -> bool:
        """Remove a communication link between two routers."""
        u, v = sorted([source, target])
        if (u, v) not in self.links:
            return False

        del self.links[(u, v)]

        if source in self._adj_list and target in self._adj_list[source]:
            self._adj_list[source].remove(target)
        if target in self._adj_list and source in self._adj_list[target]:
            self._adj_list[target].remove(source)

        return True

    def router_exists(self, router_id: str) -> bool:
        """Check if router exists in graph."""
        return router_id in self.routers

    def link_exists(self, source: str, target: str) -> bool:
        """Check if link exists in graph."""
        u, v = sorted([source, target])
        return (u, v) in self.links

    def set_router_status(self, router_id: str, is_active: bool) -> bool:
        """Enable or disable a router (failure simulation)."""
        if router_id not in self.routers:
            return False
        self.routers[router_id].is_active = is_active
        return True

    def set_link_status(self, source: str, target: str, is_active: bool) -> bool:
        """Enable or disable a link (link failure simulation)."""
        u, v = sorted([source, target])
        if (u, v) not in self.links:
            return False
        self.links[(u, v)].is_active = is_active
        return True

    def is_router_active(self, router_id: str) -> bool:
        """Return True if router exists and is active."""
        return router_id in self.routers and self.routers[router_id].is_active

    def is_link_active(self, source: str, target: str) -> bool:
        """Return True if link exists and both link and endpoint routers are active."""
        u, v = sorted([source, target])
        if (u, v) not in self.links:
            return False
        link = self.links[(u, v)]
        return link.is_active and self.is_router_active(u) and self.is_router_active(v)

    def get_neighbors(self, router_id: str, active_only: bool = True) -> List[str]:
        """
        Return the list of neighbor routers for a given router.
        If active_only is True, filters out disabled routers and disabled links.
        Returned neighbors are deterministically sorted for predictable algorithm steps.
        """
        if router_id not in self._adj_list:
            return []

        neighbors = list(self._adj_list[router_id])
        if not active_only:
            return sorted(neighbors)

        # Check router itself is active
        if not self.is_router_active(router_id):
            return []

        active_neighbors = [
            nbr for nbr in neighbors
            if self.is_router_active(nbr) and self.is_link_active(router_id, nbr)
        ]
        return sorted(active_neighbors)

    def get_adjacency_list(self, active_only: bool = False) -> Dict[str, List[str]]:
        """
        Return the graph's Adjacency List representation.
        Format: { 'R1': ['R2', 'R3'], 'R2': ['R1', 'R4'], ... }
        """
        sorted_keys = sorted(self.routers.keys())
        result: Dict[str, List[str]] = {}
        for r_id in sorted_keys:
            if active_only:
                result[r_id] = self.get_neighbors(r_id, active_only=True)
            else:
                result[r_id] = sorted(list(self._adj_list.get(r_id, [])))
        return result

    def get_adjacency_matrix(self, active_only: bool = False) -> Dict[str, Any]:
        """
        Return the graph's Adjacency Matrix representation.
        Format:
        {
            "vertices": ["R1", "R2", "R3", "R4"],
            "matrix": [
                [0, 1, 1, 0],
                [1, 0, 0, 1],
                ...
            ]
        }
        """
        vertices = sorted(self.routers.keys())
        n = len(vertices)
        index_map = {v_id: i for i, v_id in enumerate(vertices)}
        matrix = [[0 for _ in range(n)] for _ in range(n)]

        for r_id in vertices:
            neighbors = self.get_neighbors(r_id, active_only=active_only) if active_only else self._adj_list.get(r_id, [])
            i = index_map[r_id]
            for nbr in neighbors:
                if nbr in index_map:
                    j = index_map[nbr]
                    matrix[i][j] = 1

        return {
            "vertices": vertices,
            "matrix": matrix
        }

    def clear(self) -> None:
        """Clear all routers and links from the graph."""
        self.routers.clear()
        self.links.clear()
        self._adj_list.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Export complete topology state for serialization and API responses."""
        return {
            "routers": [r.to_dict() for r in self.routers.values()],
            "links": [l.to_dict() for l in self.links.values()],
            "adjacency_list": self.get_adjacency_list(active_only=False),
            "adjacency_matrix": self.get_adjacency_matrix(active_only=False),
            "total_routers": len(self.routers),
            "total_links": len(self.links),
            "active_routers": sum(1 for r in self.routers.values() if r.is_active),
            "active_links": sum(1 for l in self.links.values() if l.is_active)
        }
