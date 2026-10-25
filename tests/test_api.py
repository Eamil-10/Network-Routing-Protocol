"""Integration tests for Flask REST API endpoints."""
import pytest
import json
from app import app, active_graph, load_scenario_into_graph


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        load_scenario_into_graph("default_mesh")
        yield client


def test_api_index(client):
    res = client.get("/")
    assert res.status_code == 200


def test_api_get_topology(client):
    res = client.get("/api/topology")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "routers" in data["topology"]
    assert "links" in data["topology"]
    assert "adjacency_list" in data["topology"]
    assert "adjacency_matrix" in data["topology"]


def test_api_simulate_bfs(client):
    payload = {"source": "R1", "destination": "R6"}
    res = client.post("/api/simulate/bfs", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["algorithm"] == "BFS"
    assert data["hops"] == 3
    assert data["route"][0] == "R1"
    assert data["route"][-1] == "R6"


def test_api_simulate_dfs(client):
    payload = {"source": "R1", "destination": "R6"}
    res = client.post("/api/simulate/dfs", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["algorithm"] == "DFS"
    assert data["route"][-1] == "R6"


def test_api_search_compare(client):
    payload = {"target_id": "R4"}
    res = client.post("/api/search/compare", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "linear" in data
    assert "binary" in data
    assert data["linear"]["found"] is True
    assert data["binary"]["found"] is True


def test_api_packets_queue_and_process(client):
    # Create packet
    create_payload = {"source": "R1", "destination": "R6", "algorithm": "BFS"}
    res = client.post("/api/packets/create", json=create_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["queue_size"] >= 1

    # Process packet
    proc_res = client.post("/api/packets/process-next")
    assert proc_res.status_code == 200
    proc_data = proc_res.get_json()
    assert proc_data["success"] is True
    assert proc_data["packet"]["status"] == "DELIVERED"
    assert len(proc_data["packet"]["history_nodes"]) > 0


def test_api_routing_table(client):
    res = client.get("/api/routing-table/R1")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert len(data["routing_table"]) > 0


def test_api_dashboard_stats(client):
    res = client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert "total_routers" in data
    assert "active_routers" in data
