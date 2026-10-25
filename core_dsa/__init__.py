"""
Core DSA Package for Network Packet Routing Simulator
======================================================
Custom, manual implementations of:
- CustomQueue (FIFO Queue)
- CustomStack (LIFO Stack)
- CustomLinkedList & LinkedListNode (Singly Linked List)
- NetworkGraph (Router, Link, Adjacency List, Adjacency Matrix)
- simulate_bfs & simulate_dfs (Step-by-step educational graph traversals)
- linear_search_routers & binary_search_routers (Search algorithm benchmarks)
- generate_routing_table & simulate_table_forwarding (Forwarding table simulation)
- Packet & PacketQueueManager (Packet queueing and route history)
"""

from core_dsa.queue import CustomQueue
from core_dsa.stack import CustomStack
from core_dsa.linked_list import CustomLinkedList, LinkedListNode
from core_dsa.graph import NetworkGraph, Router, Link
from core_dsa.traversal import simulate_bfs, simulate_dfs, reconstruct_path
from core_dsa.search import linear_search_routers, binary_search_routers
from core_dsa.routing_table import generate_routing_table, simulate_table_forwarding
from core_dsa.packet import Packet, PacketQueueManager

__all__ = [
    "CustomQueue",
    "CustomStack",
    "CustomLinkedList",
    "LinkedListNode",
    "NetworkGraph",
    "Router",
    "Link",
    "simulate_bfs",
    "simulate_dfs",
    "reconstruct_path",
    "linear_search_routers",
    "binary_search_routers",
    "generate_routing_table",
    "simulate_table_forwarding",
    "Packet",
    "PacketQueueManager",
]
