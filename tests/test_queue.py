"""Unit tests for CustomQueue (FIFO)."""
import pytest
from core_dsa.queue import CustomQueue


def test_queue_initial_state():
    q = CustomQueue()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert q.peek() is None
    assert q.to_list() == []


def test_queue_fifo_order():
    q = CustomQueue()
    q.enqueue("P001")
    q.enqueue("P002")
    q.enqueue("P003")

    assert q.size() == 3
    assert q.peek() == "P001"
    assert q.to_list() == ["P001", "P002", "P003"]

    item1 = q.dequeue()
    assert item1 == "P001"
    assert q.size() == 2

    item2 = q.dequeue()
    assert item2 == "P002"

    item3 = q.dequeue()
    assert item3 == "P003"

    assert q.is_empty() is True


def test_queue_empty_dequeue_raises():
    q = CustomQueue()
    with pytest.raises(IndexError):
        q.dequeue()


def test_queue_clear():
    q = CustomQueue()
    q.enqueue("A")
    q.enqueue("B")
    q.clear()
    assert q.is_empty() is True
    assert q.size() == 0
