"""
Custom LIFO Stack Data Structure
================================
Academic Context:
A Stack is a linear data structure that adheres to the Last-In, First-Out (LIFO)
principle. The most recently pushed element is the first one popped.

In Network Packet Routing & Depth-First Search (DFS):
1. DFS Traversal: DFS explores as far as possible along each branch before backtracking.
   Using an explicit LIFO stack makes the depth-first exploration and backtracking steps
   visible and inspectable.
2. Backtracking: When a dead end is encountered (all adjacent routers visited or inactive),
   routers are popped off the stack to return to the nearest branch point with unvisited
   neighbors.
"""

from typing import Any, List, Optional


class CustomStack:
    """
    Manual implementation of a Last-In, First-Out (LIFO) Stack.
    Operates without reliance on external stack libraries.
    """

    def __init__(self):
        """Initialize an empty LIFO stack."""
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """
        Add an item onto the top of the stack.
        Time Complexity: O(1)
        """
        self._items.append(item)

    def pop(self) -> Any:
        """
        Remove and return the item at the top of the stack.
        Raises IndexError if the stack is empty.
        Time Complexity: O(1)
        """
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        """
        Return the item at the top of the stack without removing it.
        Returns None if stack is empty.
        Time Complexity: O(1)
        """
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """
        Check whether the stack contains any elements.
        Time Complexity: O(1)
        """
        return len(self._items) == 0

    def size(self) -> int:
        """
        Return the total number of items currently in the stack.
        Time Complexity: O(1)
        """
        return len(self._items)

    def to_list(self) -> List[Any]:
        """
        Return a snapshot list of items from bottom to top (last item is TOP).
        """
        return list(self._items)

    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()

    def __repr__(self) -> str:
        return f"CustomStack(bottom -> {self._items} -> TOP)"

    def __len__(self) -> int:
        return len(self._items)


if __name__ == "__main__":
    print("=" * 60)
    print("CUSTOM LIFO STACK DEMONSTRATION")
    print("Role: Depth-First Search (DFS) Traversal & Backtracking")
    print("=" * 60)

    s = CustomStack()
    print(f"\n1. Initial State:")
    print(f"   - Is empty: {s.is_empty()}")
    print(f"   - Size: {s.size()}")

    print(f"\n2. Pushing Routers onto Stack (DFS Branching):")
    for r in ["R1 (Start)", "R2 (Branch A)", "R4 (Deep Path)", "R6 (Dead End)"]:
        s.push(r)
        print(f"   + Pushed [{r}] -> Stack State: {s.to_list()}")

    print(f"\n3. Inspecting Top & Size:")
    print(f"   - Peek Top: {s.peek()}")
    print(f"   - Current Size: {s.size()}")

    print(f"\n4. Popping Routers from Stack (Backtracking Unwind):")
    while not s.is_empty():
        top_item = s.pop()
        print(f"   - Backtracked/Popped: {top_item} | Stack Remaining: {s.to_list()}")

    print("\n" + "=" * 60)
    print("CustomStack demonstration completed successfully.")
    print("=" * 60)

