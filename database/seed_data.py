"""
Predefined Network Topologies and Test Scenarios
================================================
Academic Context:
Provides standardized topologies to evaluate BFS, DFS, search algorithms,
router failure rerouting, and disconnected graph partitions.
"""

from typing import Dict, List, Any

PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "default_mesh": {
        "id": "default_mesh",
        "name": "Standard Academic 6-Router Mesh",
        "description": "Classic 6-router topology with multiple redundant paths between R1 and R6. Ideal for comparing BFS minimum-hop vs DFS deep traversal.",
        "is_default": 1,
        "routers": [
            {"id": "R1", "name": "Router 1 (Gateway)", "ip_address": "192.168.1.1", "location": "Gateway Core", "x": 100, "y": 250, "is_active": True},
            {"id": "R2", "name": "Router 2 (North)", "ip_address": "192.168.1.2", "location": "Floor 1 Server", "x": 260, "y": 140, "is_active": True},
            {"id": "R3", "name": "Router 3 (South)", "ip_address": "192.168.1.3", "location": "Floor 2 Server", "x": 260, "y": 360, "is_active": True},
            {"id": "R4", "name": "Router 4 (North-East)", "ip_address": "192.168.1.4", "location": "Data Center A", "x": 440, "y": 140, "is_active": True},
            {"id": "R5", "name": "Router 5 (South-East)", "ip_address": "192.168.1.5", "location": "Data Center B", "x": 440, "y": 360, "is_active": True},
            {"id": "R6", "name": "Router 6 (Egress)", "ip_address": "192.168.1.6", "location": "Edge Border", "x": 600, "y": 250, "is_active": True},
        ],
        "links": [
            {"source": "R1", "target": "R2", "is_active": True},
            {"source": "R1", "target": "R3", "is_active": True},
            {"source": "R2", "target": "R4", "is_active": True},
            {"source": "R3", "target": "R5", "is_active": True},
            {"source": "R4", "target": "R5", "is_active": True},
            {"source": "R4", "target": "R6", "is_active": True},
            {"source": "R5", "target": "R6", "is_active": True},
        ]
    },
    "redundant_ring": {
        "id": "redundant_ring",
        "name": "Redundant Ring Network (8 Routers)",
        "description": "Circular ring network with cross-links. Demonstrates cycle handling, alternate path selection, and resiliency against single link cuts.",
        "is_default": 0,
        "routers": [
            {"id": "R1", "name": "Router 1", "ip_address": "10.0.0.1", "location": "Node A", "x": 350, "y": 80, "is_active": True},
            {"id": "R2", "name": "Router 2", "ip_address": "10.0.0.2", "location": "Node B", "x": 520, "y": 140, "is_active": True},
            {"id": "R3", "name": "Router 3", "ip_address": "10.0.0.3", "location": "Node C", "x": 580, "y": 300, "is_active": True},
            {"id": "R4", "name": "Router 4", "ip_address": "10.0.0.4", "location": "Node D", "x": 520, "y": 460, "is_active": True},
            {"id": "R5", "name": "Router 5", "ip_address": "10.0.0.5", "location": "Node E", "x": 350, "y": 520, "is_active": True},
            {"id": "R6", "name": "Router 6", "ip_address": "10.0.0.6", "location": "Node F", "x": 180, "y": 460, "is_active": True},
            {"id": "R7", "name": "Router 7", "ip_address": "10.0.0.7", "location": "Node G", "x": 120, "y": 300, "is_active": True},
            {"id": "R8", "name": "Router 8", "ip_address": "10.0.0.8", "location": "Node H", "x": 180, "y": 140, "is_active": True},
        ],
        "links": [
            {"source": "R1", "target": "R2", "is_active": True},
            {"source": "R2", "target": "R3", "is_active": True},
            {"source": "R3", "target": "R4", "is_active": True},
            {"source": "R4", "target": "R5", "is_active": True},
            {"source": "R5", "target": "R6", "is_active": True},
            {"source": "R6", "target": "R7", "is_active": True},
            {"source": "R7", "target": "R8", "is_active": True},
            {"source": "R8", "target": "R1", "is_active": True},
            {"source": "R2", "target": "R7", "is_active": True},
            {"source": "R3", "target": "R6", "is_active": True},
        ]
    },
    "bottleneck_bridge": {
        "id": "bottleneck_bridge",
        "name": "Bottleneck & Bridge Topology (7 Routers)",
        "description": "Two subnets connected by a single critical bridge link (R3 ↔ R4). Demonstrates single-point-of-failure rerouting and graceful No-Route handling.",
        "is_default": 0,
        "routers": [
            {"id": "R1", "name": "Campus West 1", "ip_address": "172.16.1.1", "location": "West Wing", "x": 100, "y": 180, "is_active": True},
            {"id": "R2", "name": "Campus West 2", "ip_address": "172.16.1.2", "location": "West Annex", "x": 100, "y": 340, "is_active": True},
            {"id": "R3", "name": "West Bridge Router", "ip_address": "172.16.1.3", "location": "Inter-site Gateway W", "x": 260, "y": 260, "is_active": True},
            {"id": "R4", "name": "East Bridge Router", "ip_address": "172.16.2.1", "location": "Inter-site Gateway E", "x": 440, "y": 260, "is_active": True},
            {"id": "R5", "name": "Campus East 1", "ip_address": "172.16.2.2", "location": "East Wing", "x": 600, "y": 180, "is_active": True},
            {"id": "R6", "name": "Campus East 2", "ip_address": "172.16.2.3", "location": "East Annex", "x": 600, "y": 340, "is_active": True},
            {"id": "R7", "name": "Data Core East", "ip_address": "172.16.2.4", "location": "Central Server Core", "x": 720, "y": 260, "is_active": True},
        ],
        "links": [
            {"source": "R1", "target": "R2", "is_active": True},
            {"source": "R1", "target": "R3", "is_active": True},
            {"source": "R2", "target": "R3", "is_active": True},
            {"source": "R3", "target": "R4", "is_active": True},  # Critical bridge edge
            {"source": "R4", "target": "R5", "is_active": True},
            {"source": "R4", "target": "R6", "is_active": True},
            {"source": "R5", "target": "R6", "is_active": True},
            {"source": "R5", "target": "R7", "is_active": True},
            {"source": "R6", "target": "R7", "is_active": True},
        ]
    },
    "large_scale": {
        "id": "large_scale",
        "name": "Extended Campus Backbone (15 Routers)",
        "description": "Large 15-router network designed for demonstrating Linear Search vs Binary Search comparison efficiency on larger arrays.",
        "is_default": 0,
        "routers": [
            {"id": "R1", "name": "Core Router 1", "ip_address": "10.10.1.1", "location": "Admin Hub", "x": 100, "y": 160, "is_active": True},
            {"id": "R2", "name": "Core Router 2", "ip_address": "10.10.1.2", "location": "Admin Hub", "x": 100, "y": 340, "is_active": True},
            {"id": "R3", "name": "Dist Router 3", "ip_address": "10.10.2.1", "location": "Eng Block A", "x": 220, "y": 100, "is_active": True},
            {"id": "R4", "name": "Dist Router 4", "ip_address": "10.10.2.2", "location": "Eng Block B", "x": 220, "y": 240, "is_active": True},
            {"id": "R5", "name": "Dist Router 5", "ip_address": "10.10.2.3", "location": "Library", "x": 220, "y": 380, "is_active": True},
            {"id": "R6", "name": "Access Router 6", "ip_address": "10.10.3.1", "location": "Lab 1", "x": 350, "y": 100, "is_active": True},
            {"id": "R7", "name": "Access Router 7", "ip_address": "10.10.3.2", "location": "Lab 2", "x": 350, "y": 240, "is_active": True},
            {"id": "R8", "name": "Access Router 8", "ip_address": "10.10.3.3", "location": "Lab 3", "x": 350, "y": 380, "is_active": True},
            {"id": "R9", "name": "Aggregation 9", "ip_address": "10.10.4.1", "location": "Main Tower", "x": 480, "y": 140, "is_active": True},
            {"id": "R10", "name": "Aggregation 10", "ip_address": "10.10.4.2", "location": "Main Tower", "x": 480, "y": 320, "is_active": True},
            {"id": "R11", "name": "Server Farm 11", "ip_address": "10.10.5.1", "location": "Data Pod 1", "x": 600, "y": 100, "is_active": True},
            {"id": "R12", "name": "Server Farm 12", "ip_address": "10.10.5.2", "location": "Data Pod 2", "x": 600, "y": 240, "is_active": True},
            {"id": "R13", "name": "Server Farm 13", "ip_address": "10.10.5.3", "location": "Data Pod 3", "x": 600, "y": 380, "is_active": True},
            {"id": "R14", "name": "Egress Border 14", "ip_address": "10.10.6.1", "location": "ISP Primary", "x": 720, "y": 180, "is_active": True},
            {"id": "R15", "name": "Egress Border 15", "ip_address": "10.10.6.2", "location": "ISP Backup", "x": 720, "y": 320, "is_active": True},
        ],
        "links": [
            {"source": "R1", "target": "R2", "is_active": True},
            {"source": "R1", "target": "R3", "is_active": True},
            {"source": "R1", "target": "R4", "is_active": True},
            {"source": "R2", "target": "R4", "is_active": True},
            {"source": "R2", "target": "R5", "is_active": True},
            {"source": "R3", "target": "R6", "is_active": True},
            {"source": "R4", "target": "R7", "is_active": True},
            {"source": "R5", "target": "R8", "is_active": True},
            {"source": "R6", "target": "R9", "is_active": True},
            {"source": "R7", "target": "R9", "is_active": True},
            {"source": "R7", "target": "R10", "is_active": True},
            {"source": "R8", "target": "R10", "is_active": True},
            {"source": "R9", "target": "R11", "is_active": True},
            {"source": "R9", "target": "R12", "is_active": True},
            {"source": "R10", "target": "R12", "is_active": True},
            {"source": "R10", "target": "R13", "is_active": True},
            {"source": "R11", "target": "R14", "is_active": True},
            {"source": "R12", "target": "R14", "is_active": True},
            {"source": "R12", "target": "R15", "is_active": True},
            {"source": "R13", "target": "R15", "is_active": True},
            {"source": "R14", "target": "R15", "is_active": True},
        ]
    }
}
