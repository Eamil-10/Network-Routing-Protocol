"""Unit tests for dynamic routing, router failure, link failure, and No-Route conditions."""
from core_dsa.graph import NetworkGraph
from core_dsa.traversal import simulate_bfs


def test_dynamic_rerouting_after_router_failure():
    # Diamond graph:
    # R1 -> R2 -> R4
    # R1 -> R3 -> R4
    g = NetworkGraph()
    for r in ["R1", "R2", "R3", "R4"]:
        g.add_router(r)

    g.add_link("R1", "R2")
    g.add_link("R2", "R4")
    g.add_link("R1", "R3")
    g.add_link("R3", "R4")

    # Initial route
    res1 = simulate_bfs(g, "R1", "R4")
    assert res1["success"] is True
    initial_route = res1["route"]
    assert initial_route == ["R1", "R2", "R4"]

    # Now fail router R2!
    g.set_router_status("R2", False)

    # Dynamic route recalculation
    res2 = simulate_bfs(g, "R1", "R4")
    assert res2["success"] is True
    new_route = res2["route"]
    assert "R2" not in new_route
    assert new_route == ["R1", "R3", "R4"]


def test_dynamic_rerouting_after_link_failure():
    g = NetworkGraph()
    for r in ["R1", "R2", "R3", "R4"]:
        g.add_router(r)

    g.add_link("R1", "R2")
    g.add_link("R2", "R4")
    g.add_link("R1", "R3")
    g.add_link("R3", "R4")

    # Disable link R1 ↔ R2
    g.set_link_status("R1", "R2", False)

    res = simulate_bfs(g, "R1", "R4")
    assert res["success"] is True
    assert res["route"] == ["R1", "R3", "R4"]


def test_bridge_failure_causes_no_route():
    # Bridge network: R1 - R2 (bridge) - R3
    g = NetworkGraph()
    g.add_router("R1")
    g.add_router("R2")
    g.add_router("R3")
    g.add_link("R1", "R2")
    g.add_link("R2", "R3")

    # Fail bridge router R2
    g.set_router_status("R2", False)

    res = simulate_bfs(g, "R1", "R3")
    assert res["success"] is False
    assert res["route"] == []
    assert res["hops"] == 0


def test_default_topology_demo_routes():
    """Verify default topology satisfies:
    (a) Multiple routes exist between R1 and R6.
    (b) DFS finds a longer route than BFS and backtracks at least once.
    (c) Failing router R2 on the BFS route still leaves an alternative route.
    """
    from core_dsa.traversal import simulate_dfs

    g = NetworkGraph()
    for r in ["R1", "R2", "R3", "R4", "R5", "R6"]:
        g.add_router(r)

    links = [
        ("R1", "R2"),
        ("R1", "R3"),
        ("R2", "R4"),
        ("R3", "R5"),
        ("R4", "R5"),
        ("R4", "R6"),
        ("R5", "R6"),
    ]
    for u, v in links:
        g.add_link(u, v)

    # (a) Multiple routes exist
    bfs_res = simulate_bfs(g, "R1", "R6")
    dfs_res = simulate_dfs(g, "R1", "R6")

    assert bfs_res["success"] is True
    assert dfs_res["success"] is True
    assert bfs_res["route"] != dfs_res["route"]

    # (b) DFS finds a longer route than BFS and backtracks at least once
    assert bfs_res["hops"] == 3
    assert bfs_res["route"] == ["R1", "R2", "R4", "R6"]
    assert dfs_res["hops"] == 4
    assert dfs_res["route"] == ["R1", "R2", "R4", "R5", "R6"]
    assert dfs_res["hops"] > bfs_res["hops"]
    assert dfs_res["backtracking_count"] >= 1

    # (c) Failing R2 on the BFS route leaves an alternative route (R1 -> R3 -> R5 -> R6)
    g.set_router_status("R2", False)
    reroute_res = simulate_bfs(g, "R1", "R6")
    assert reroute_res["success"] is True
    assert "R2" not in reroute_res["route"]
    assert reroute_res["route"] == ["R1", "R3", "R5", "R6"]
    assert reroute_res["hops"] == 3

    # Failing both R2 and R3 leaves no route
    g.set_router_status("R3", False)
    severed_res = simulate_bfs(g, "R1", "R6")
    assert severed_res["success"] is False
    assert severed_res["route"] == []

