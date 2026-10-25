"""
Custom Singly Linked List Data Structure
=========================================
Academic Context:
A Linked List is a linear dynamic data structure composed of nodes, where each node
contains data and a reference (pointer) to the next node in sequence.

In Network Packet Routing:
1. Dynamic Route History: Unlike fixed-size static arrays, a linked list can grow
   dynamically as a packet traverses routers of arbitrary path lengths.
2. Route Audit Trail: Each hop in the transmission history is stored as a linked list node,
   recording the router traversed, arrival status, and hop index.
3. Memory Efficiency: Nodes are allocated dynamically during runtime without requiring
   costly contiguous block reallocations.
"""

from typing import Any, List, Optional, Dict


class LinkedListNode:
    """A node in a Singly Linked List."""

    def __init__(self, data: Any, metadata: Optional[Dict[str, Any]] = None):
        self.data: Any = data
        self.metadata: Dict[str, Any] = metadata or {}
        self.next: Optional["LinkedListNode"] = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class CustomLinkedList:
    """
    Manual implementation of a Singly Linked List with head and tail pointers.
    Maintains packet transmission and hop history.
    """

    def __init__(self):
        """Initialize an empty linked list."""
        self.head: Optional[LinkedListNode] = None
        self.tail: Optional[LinkedListNode] = None
        self._length: int = 0

    def append(self, data: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Append a new node to the end of the linked list.
        Time Complexity: O(1) via tail pointer
        """
        new_node = LinkedListNode(data, metadata)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            assert self.tail is not None
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def is_empty(self) -> bool:
        """Return True if the linked list contains no nodes."""
        return self.head is None

    def length(self) -> int:
        """Return total number of nodes in the linked list."""
        return self._length

    def clear(self) -> None:
        """Clear all nodes from the linked list."""
        self.head = None
        self.tail = None
        self._length = 0

    def to_list(self) -> List[Any]:
        """
        Traverse the list and return plain data values.
        Time Complexity: O(n)
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def to_detailed_list(self) -> List[Dict[str, Any]]:
        """
        Traverse the list and return detailed node records with metadata.
        Time Complexity: O(n)
        """
        result = []
        current = self.head
        idx = 1
        while current is not None:
            result.append({
                "hop_number": idx,
                "router_id": current.data,
                "metadata": current.metadata
            })
            current = current.next
            idx += 1
        return result

    def display(self) -> str:
        """
        Return a formatted traversal string such as 'R1 -> R2 -> R4 -> R6'.
        """
        items = self.to_list()
        if not items:
            return "Empty Route History"
        return " → ".join(str(item) for item in items)

    def __repr__(self) -> str:
        return f"CustomLinkedList({self.display()})"

    def __len__(self) -> int:
        return self._length


if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM SINGLY LINKED LIST DEMONSTRATION")
    print("Role: Dynamic Packet Transmission & Hop History (CO2)")
    print("=" * 60)

    # 1. Initial Empty State
    route_history = CustomLinkedList()
    print(f"\n1. Initial State:")
    print(f"   - Is empty: {route_history.is_empty()}")
    print(f"   - Length: {route_history.length()}")
    print(f"   - Display: {route_history.display()}")

    # 2. Append hops as packet traverses the network
    print(f"\n2. Simulating Packet Traversal (Hop-by-Hop Dynamic Appends):")
    hops = [
        ("R1", {"role": "Source Gateway", "ip": "192.168.1.1", "action": "Packet Ingress"}),
        ("R2", {"role": "Transit North", "ip": "192.168.1.2", "action": "Forwarded via BFS"}),
        ("R4", {"role": "Transit Data Center", "ip": "192.168.1.4", "action": "Forwarded via BFS"}),
        ("R6", {"role": "Destination Egress", "ip": "192.168.1.6", "action": "Packet Delivered"}),
    ]
    for router_id, meta in hops:
        route_history.append(router_id, meta)
        print(f"   + Appended hop [{router_id}]: Chain -> {route_history.display()}")

    # 3. Traversal & Verification
    print(f"\n3. Traversal & Verification:")
    print(f"   - Total Hops: {len(route_history)}")
    print(f"   - Head Node: {route_history.head}")
    print(f"   - Tail Node: {route_history.tail}")
    print(f"   - Plain Path: {route_history.to_list()}")
    print(f"   - Formatted Chain: {route_history.display()}")

    # 4. Detailed Node-by-Node Audit Trail
    print(f"\n4. Detailed Packet Route Audit Trail:")
    for record in route_history.to_detailed_list():
        hop = record["hop_number"]
        rid = record["router_id"]
        meta = record["metadata"]
        print(f"   Hop {hop}: Router {rid} | Role: {meta.get('role')} | IP: {meta.get('ip')} | Action: {meta.get('action')}")

    print("\n" + "=" * 60)
    print("CustomLinkedList demonstration completed successfully.")
    print("=" * 60)

