"""Unit tests for CustomStack (LIFO)."""
import pytest
from core_dsa.stack import CustomStack


def test_stack_initial_state():
    s = CustomStack()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert s.peek() is None
    assert s.to_list() == []


def test_stack_lifo_order():
    s = CustomStack()
    s.push("R1")
    s.push("R2")
    s.push("R4")

    assert s.size() == 3
    assert s.peek() == "R4"

    top1 = s.pop()
    assert top1 == "R4"
    assert s.peek() == "R2"

    top2 = s.pop()
    assert top2 == "R2"

    top3 = s.pop()
    assert top3 == "R1"

    assert s.is_empty() is True


def test_stack_empty_pop_raises():
    s = CustomStack()
    with pytest.raises(IndexError):
        s.pop()


def test_stack_clear():
    s = CustomStack()
    s.push("X")
    s.push("Y")
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0
