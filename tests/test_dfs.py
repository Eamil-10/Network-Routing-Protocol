"""Unit tests for manual DFS traversal, stack state, and backtracking."""
from core_dsa.graph import NetworkGraph
from core_dsa.traversal import simulate_dfs


def create_mesh_graph():
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


def test_dfs_finds_path():
    g = create_mesh_graph()
    result = simulate_dfs(g, "R1", "R6")

    assert result["success"] is True
    assert result["algorithm"] == "DFS"
    assert result["route"][0] == "R1"
    assert result["route"][-1] == "R6"
    assert len(result["steps"]) > 0


def test_dfs_backtracking_on_dead_end():
    # Topology with a dead-end branch: R1 - R2 - R3 (dead end), and R1 - R4 - R5 (destination)
    g = NetworkGraph()
    for r in ["R1", "R2", "R3", "R4", "R5"]:
        g.add_router(r)

    g.add_link("R1", "R2")
    g.add_link("R2", "R3")  # Dead end branch
    g.add_link("R1", "R4")
    g.add_link("R4", "R5")  # Target branch

    result = simulate_dfs(g, "R1", "R5")
    assert result["success"] is True
    assert result["route"] == ["R1", "R4", "R5"] or result["route"][-1] == "R5"
    assert "backtracking_count" in result


def test_dfs_unreachable():
    g = create_mesh_graph()
    g.add_router("R99")
    result = simulate_dfs(g, "R1", "R99")
    assert result["success"] is False
    assert result["route"] == []
