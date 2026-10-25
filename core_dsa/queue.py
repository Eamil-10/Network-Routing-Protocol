"""
Custom FIFO Queue Data Structure
================================
Academic Context:
A Queue is a linear data structure that operates under the First-In, First-Out (FIFO)
principle. The first element enqueued into the queue is the first one to be dequeued.

In Network Packet Routing & Breadth-First Search (BFS):
1. Packet Queues in Routers: Packets arriving at a router's input port are buffered in a
   FIFO packet queue and dispatched in order of arrival.
2. BFS Traversal: BFS explores nodes layer-by-layer. A FIFO queue maintains the frontier
   of discovered routers so that routers closest to the source (level k) are completely
   processed before routers further away (level k+1) are examined.
"""

from typing import Any, List, Optional


class CustomQueue:
    """
    Manual implementation of a First-In, First-Out (FIFO) Queue.
    Operates without reliance on external queue or graph libraries.
    """

    def __init__(self):
        """Initialize an empty FIFO queue."""
        self._items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        Add an item to the rear of the queue.
        Time Complexity: O(1) amortized
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """
        Remove and return the item at the front of the queue.
        Raises IndexError if queue is empty.
        Time Complexity: O(n) in dynamic array shift, or O(1) conceptually.
        """
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self._items.pop(0)

    def peek(self) -> Optional[Any]:
        """
        Return the item at the front of the queue without removing it.
        Returns None if queue is empty.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._items[0]

    def is_empty(self) -> bool:
        """
        Check whether the queue contains any elements.
        Time Complexity: O(1)
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the total number of items currently in the queue.
        Time Complexity: O(1)
        """
        return len(self._items)

    def to_list(self) -> List[Any]:
        """
        Return a snapshot list of items from front to rear for visualization.
        """
        return list(self._items)

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items.clear()

    def __repr__(self) -> str:
        return f"CustomQueue(front -> {self._items} -> rear)"

    def __len__(self) -> int:
        return len(self._items)


if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM FIFO QUEUE DEMONSTRATION")
    print("Role: Packet Arrival Buffer & BFS Frontier (CO1)")
    print("=" * 60)

    q = CustomQueue()
    print(f"\n1. Initial State:")
    print(f"   - Is empty: {q.is_empty()}")
    print(f"   - Size: {q.size()}")

    print(f"\n2. Enqueueing Packets into Buffer (FIFO order):")
    for pkt in ["PKT-101 (VoIP)", "PKT-102 (HTTP)", "PKT-103 (DNS)", "PKT-104 (Video)"]:
        q.enqueue(pkt)
        print(f"   + Enqueued [{pkt}] -> Queue State: {q.to_list()}")

    print(f"\n3. Inspecting Front & Size:")
    print(f"   - Peek Front: {q.peek()}")
    print(f"   - Current Size: {q.size()}")

    print(f"\n4. Dequeueing Packets (First-In, First-Out):")
    while not q.is_empty():
        item = q.dequeue()
        print(f"   - Dequeued: {item} | Remaining Queue: {q.to_list()}")

    print("\n" + "=" * 60)
    print("CustomQueue demonstration completed successfully.")
    print("=" * 60)

