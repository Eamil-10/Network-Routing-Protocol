"""Unit tests for CustomLinkedList for packet route history."""
from core_dsa.linked_list import CustomLinkedList


def test_linked_list_empty():
    ll = CustomLinkedList()
    assert ll.is_empty() is True
    assert ll.length() == 0
    assert len(ll) == 0
    assert ll.to_list() == []
    assert ll.display() == "Empty Route History"


def test_linked_list_append():
    ll = CustomLinkedList()
    ll.append("R1", {"role": "source"})
    ll.append("R2", {"role": "transit"})
    ll.append("R4", {"role": "transit"})
    ll.append("R6", {"role": "destination"})

    assert ll.is_empty() is False
    assert ll.length() == 4
    assert ll.to_list() == ["R1", "R2", "R4", "R6"]
    assert ll.display() == "R1 → R2 → R4 → R6"

    detailed = ll.to_detailed_list()
    assert len(detailed) == 4
    assert detailed[0]["hop_number"] == 1
    assert detailed[0]["router_id"] == "R1"
    assert detailed[3]["router_id"] == "R6"


def test_linked_list_clear():
    ll = CustomLinkedList()
    ll.append("A")
    ll.append("B")
    ll.clear()
    assert ll.is_empty() is True
    assert ll.length() == 0
    assert ll.head is None
    assert ll.tail is None
