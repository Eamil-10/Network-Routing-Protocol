"""
Packet Model and Packet Queue Management
=========================================
Academic Context:
In packet-switched communication networks, data is divided into structured units
called Packets. Each packet carries a header (Source, Destination, Packet ID) and
traverses routers hop-by-hop toward its destination.

Data Structures Applied:
1. FIFO Packet Queue:
   - Manages incoming packets awaiting routing computation.
   - Preserves First-In, First-Out arrival order (CO1).
2. Singly Linked List:
   - Stores the packet's sequential hop history (CO2).
   - Each visited router node is dynamically appended to the linked list.
"""

import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from core_dsa.queue import CustomQueue
from core_dsa.linked_list import CustomLinkedList
from core_dsa.graph import NetworkGraph
from core_dsa.traversal import simulate_bfs, simulate_dfs


class Packet:
    """Represents a Network Data Packet with metadata and linked-list route history."""

    def __init__(
        self,
        packet_id: str,
        source: str,
        destination: str,
        algorithm: str = "BFS",
        payload_size_bytes: int = 1024
    ):
        self.packet_id: str = packet_id
        self.source: str = source
        self.destination: str = destination
        self.algorithm: str = algorithm.upper()
        self.payload_size_bytes: int = payload_size_bytes
        self.created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Routing status: 'QUEUED', 'IN_TRANSIT', 'DELIVERED', 'FAILED_NO_ROUTE'
        self.status: str = "QUEUED"
        self.route: List[str] = []
        self.hops: int = 0
        self.nodes_visited: int = 0
        self.processed_at: Optional[str] = None
        self.error_message: Optional[str] = None

        # Route history stored in a manual Singly Linked List
        self.history_list: CustomLinkedList = CustomLinkedList()

    def process(self, graph: NetworkGraph) -> Dict[str, Any]:
        """
        Process and route this packet through the network graph using its selected algorithm.
        Populates the linked-list route history.
        """
        self.processed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.algorithm == "DFS":
            sim_result = simulate_dfs(graph, self.source, self.destination)
        else:
            sim_result = simulate_bfs(graph, self.source, self.destination)

        self.history_list.clear()

        if sim_result["success"]:
            self.status = "DELIVERED"
            self.route = sim_result["route"]
            self.hops = sim_result["hops"]
            self.nodes_visited = sim_result["nodes_visited"]
            self.error_message = None

            # Append every visited router along the path to the linked list
            for idx, router_id in enumerate(self.route):
                self.history_list.append(
                    data=router_id,
                    metadata={
                        "hop_index": idx,
                        "is_source": (idx == 0),
                        "is_destination": (idx == len(self.route) - 1),
                        "timestamp": datetime.now().strftime("%H:%M:%S.%f")[:12]
                    }
                )
        else:
            self.status = "FAILED_NO_ROUTE"
            self.route = []
            self.hops = 0
            self.nodes_visited = sim_result.get("nodes_visited", 0)
            self.error_message = sim_result.get("error", "Destination is unreachable from current topology.")

            # Record source failure in history
            self.history_list.append(
                data=self.source,
                metadata={"status": "FAILED_AT_SOURCE"}
            )

        return {
            "packet": self.to_dict(),
            "simulation": sim_result
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize packet information for UI display and database logging."""
        return {
            "packet_id": self.packet_id,
            "source": self.source,
            "destination": self.destination,
            "algorithm": self.algorithm,
            "status": self.status,
            "route": self.route,
            "route_display": self.history_list.display(),
            "hops": self.hops,
            "nodes_visited": self.nodes_visited,
            "created_at": self.created_at,
            "processed_at": self.processed_at,
            "error_message": self.error_message,
            "history_nodes": self.history_list.to_detailed_list()
        }


class PacketQueueManager:
    """
    Manages the buffer of packets awaiting transmission using CustomQueue (FIFO).
    Also maintains delivered and failed packet audit lists.
    """

    def __init__(self):
        self.queue: CustomQueue = CustomQueue()
        self.delivered_packets: List[Packet] = []
        self.failed_packets: List[Packet] = []
        self._packet_counter: int = 1

    def create_packet_id(self) -> str:
        """Generate deterministic sequential IDs like P001, P002..."""
        p_id = f"P{self._packet_counter:03d}"
        self._packet_counter += 1
        return p_id

    def enqueue_packet(
        self,
        source: str,
        destination: str,
        algorithm: str = "BFS",
        custom_id: Optional[str] = None
    ) -> Packet:
        """Create and enqueue a new packet."""
        p_id = custom_id or self.create_packet_id()
        packet = Packet(
            packet_id=p_id,
            source=source,
            destination=destination,
            algorithm=algorithm
        )
        self.queue.enqueue(packet)
        return packet

    def dequeue_and_process(self, graph: NetworkGraph) -> Optional[Dict[str, Any]]:
        """
        Dequeue the front packet from the FIFO queue and route it through the network.
        """
        if self.queue.is_empty():
            return None

        packet: Packet = self.queue.dequeue()
        result = packet.process(graph)

        if packet.status == "DELIVERED":
            self.delivered_packets.append(packet)
        else:
            self.failed_packets.append(packet)

        return result

    def get_queue_view(self) -> List[Dict[str, Any]]:
        """Return snapshot of packets currently in queue (Front -> Rear)."""
        packets = self.queue.to_list()
        return [p.to_dict() for p in packets]

    def get_all_history(self) -> List[Dict[str, Any]]:
        """Return all processed packets (both delivered and failed)."""
        all_processed = self.delivered_packets + self.failed_packets
        return [p.to_dict() for p in reversed(all_processed)]

    def stats(self) -> Dict[str, int]:
        """Return summary count metrics for dashboard."""
        return {
            "in_queue": self.queue.size(),
            "delivered": len(self.delivered_packets),
            "failed": len(self.failed_packets),
            "total_processed": len(self.delivered_packets) + len(self.failed_packets)
        }
