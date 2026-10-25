"""Unit tests for NetworkGraph, Adjacency List, and Adjacency Matrix."""
from core_dsa.graph import NetworkGraph


def test_graph_add_routers_and_links():
    g = NetworkGraph()
    g.add_router("R1", name="Router 1")
    g.add_router("R2", name="Router 2")
    g.add_router("R3", name="Router 3")

    assert g.router_exists("R1") is True
    assert g.router_exists("R4") is False

    g.add_link("R1", "R2")
    g.add_link("R2", "R3")

    assert g.link_exists("R1", "R2") is True
    assert g.link_exists("R2", "R1") is True  # Undirected
    assert g.link_exists("R1", "R3") is False

    assert g.get_neighbors("R1") == ["R2"]
    assert g.get_neighbors("R2") == ["R1", "R3"]


def test_graph_adjacency_list():
    g = NetworkGraph()
    g.add_router("R1")
    g.add_router("R2")
    g.add_router("R3")
    g.add_link("R1", "R2")
    g.add_link("R1", "R3")

    adj_list = g.get_adjacency_list()
    assert adj_list["R1"] == ["R2", "R3"]
    assert adj_list["R2"] == ["R1"]
    assert adj_list["R3"] == ["R1"]


def test_graph_adjacency_matrix():
    g = NetworkGraph()
    g.add_router("R1")
    g.add_router("R2")
    g.add_router("R3")
    g.add_link("R1", "R2")
    g.add_link("R2", "R3")

    adj_matrix = g.get_adjacency_matrix()
    vertices = adj_matrix["vertices"]
    matrix = adj_matrix["matrix"]

    assert vertices == ["R1", "R2", "R3"]
    # Matrix:
    # R1 connects to R2: (0, 1) = 1, (1, 0) = 1
    # R2 connects to R3: (1, 2) = 1, (2, 1) = 1
    assert matrix[0] == [0, 1, 0]
    assert matrix[1] == [1, 0, 1]
    assert matrix[2] == [0, 1, 0]


def test_graph_router_and_link_failures():
    g = NetworkGraph()
    g.add_router("R1")
    g.add_router("R2")
    g.add_router("R3")
    g.add_link("R1", "R2")
    g.add_link("R2", "R3")

    # Disable router R2
    assert g.is_router_active("R2") is True
    g.set_router_status("R2", False)
    assert g.is_router_active("R2") is False

    # Neighbors of R1 with active_only=True should now be empty because R2 is down
    assert g.get_neighbors("R1", active_only=True) == []
    # With active_only=False, R2 is still in topology
    assert g.get_neighbors("R1", active_only=False) == ["R2"]

    # Re-enable R2
    g.set_router_status("R2", True)
    assert g.get_neighbors("R1", active_only=True) == ["R2"]

    # Disable link R1 ↔ R2
    g.set_link_status("R1", "R2", False)
    assert g.is_link_active("R1", "R2") is False
    assert g.get_neighbors("R1", active_only=True) == []
