"""Unit tests for manual BFS traversal and minimum-hop route discovery."""
from core_dsa.graph import NetworkGraph
from core_dsa.traversal import simulate_bfs


def create_mesh_graph():
    """Create standard 6-router mesh graph."""
    g = NetworkGraph()
    for r_id in ["R1", "R2", "R3", "R4", "R5", "R6"]:
        g.add_router(r_id)

    g.add_link("R1", "R2")
    g.add_link("R1", "R3")
    g.add_link("R2", "R3")
    g.add_link("R2", "R4")
    g.add_link("R3", "R5")
    g.add_link("R2", "R5")
    g.add_link("R4", "R5")
    g.add_link("R4", "R6")
    g.add_link("R5", "R6")
    return g


def test_bfs_minimum_hop_route():
    g = create_mesh_graph()
    result = simulate_bfs(g, "R1", "R6")

    assert result["success"] is True
    assert result["algorithm"] == "BFS"
    assert result["source"] == "R1"
    assert result["destination"] == "R6"

    # In this mesh, shortest unweighted hop count is 3
    # (R1 -> R2 -> R4 -> R6 or R1 -> R3 -> R5 -> R6)
    assert result["hops"] == 3
    assert len(result["route"]) == 4
    assert result["route"][0] == "R1"
    assert result["route"][-1] == "R6"
    assert len(result["steps"]) > 0
    assert len(result["reconstruction_steps"]) > 0


def test_bfs_source_equals_destination():
    g = create_mesh_graph()
    result = simulate_bfs(g, "R2", "R2")
    assert result["success"] is True
    assert result["route"] == ["R2"]
    assert result["hops"] == 0


def test_bfs_disconnected_unreachable():
    g = create_mesh_graph()
    # Add an isolated router R7
    g.add_router("R7")
    result = simulate_bfs(g, "R1", "R7")

    assert result["success"] is False
    assert result["route"] == []
    assert result["hops"] == 0
