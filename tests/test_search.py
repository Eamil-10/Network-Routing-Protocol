"""Unit tests for manual Linear Search and Binary Search algorithms."""
from core_dsa.search import linear_search_routers, binary_search_routers

SAMPLE_ROUTERS = [
    {"id": "R1", "name": "Router 1", "ip_address": "192.168.1.1", "location": "Gateway"},
    {"id": "R2", "name": "Router 2", "ip_address": "192.168.1.2", "location": "North"},
    {"id": "R3", "name": "Router 3", "ip_address": "192.168.1.3", "location": "South"},
    {"id": "R4", "name": "Router 4", "ip_address": "192.168.1.4", "location": "East"},
    {"id": "R5", "name": "Router 5", "ip_address": "192.168.1.5", "location": "West"},
    {"id": "R6", "name": "Router 6", "ip_address": "192.168.1.6", "location": "Edge"},
]


def test_linear_search_found():
    res = linear_search_routers(SAMPLE_ROUTERS, "R3")
    assert res["found"] is True
    assert res["record"]["id"] == "R3"
    assert res["comparisons"] == 3  # Found at index 2 (1-based count = 3)
    assert len(res["steps"]) == 3


def test_linear_search_not_found():
    res = linear_search_routers(SAMPLE_ROUTERS, "R99")
    assert res["found"] is False
    assert res["record"] is None
    assert res["comparisons"] == len(SAMPLE_ROUTERS)


def test_binary_search_found():
    res = binary_search_routers(SAMPLE_ROUTERS, "R4")
    assert res["found"] is True
    assert res["record"]["id"] == "R4"
    # For n=6, binary search will find it in at most ceil(log2(6)) = 3 comparisons
    assert res["comparisons"] <= 3
    assert len(res["steps"]) > 0


def test_binary_search_not_found():
    res = binary_search_routers(SAMPLE_ROUTERS, "R99")
    assert res["found"] is False
    assert res["record"] is None
    assert res["comparisons"] <= 4


def test_search_comparison_advantage():
    # 15 elements
    routers_15 = [{"id": f"R{i}", "name": f"Router {i}"} for i in range(1, 16)]
    # Target at end: R15
    linear_res = linear_search_routers(routers_15, "R15")
    binary_res = binary_search_routers(routers_15, "R15")

    # Linear search takes 15 comparisons (worst case O(n))
    assert linear_res["comparisons"] == 15
    # Binary search takes at most 4 comparisons (O(log2 15) <= 4)
    assert binary_res["comparisons"] <= 4
    assert binary_res["comparisons"] < linear_res["comparisons"]
