import pytest
import numpy as np
from operating_lines import rectifying_y, q_line_y, intersection, stripping_y


def test_rectifying_y_through_xD():
    assert rectifying_y(0.6, 2.0, 0.6) == pytest.approx(0.6)

def test_q_line_y_through_xF():
    assert q_line_y(0.6, 0.8, 0.6) == pytest.approx(0.6)
    assert q_line_y(0.0, 0.8, 0.6) == pytest.approx(3)

def test_intersection_q_zero():
    xi, yi = intersection(2.0, 0.9, 0, 0.6)
    assert xi == pytest.approx(0.45)
    assert yi == pytest.approx(0.6)

def test_intersection_q_one():
    xi, yi = intersection(2.0, 0.9, 1, 0.6)
    assert xi == pytest.approx(0.6)
    assert yi == pytest.approx(0.7)

def test_intersection_both_lines():
    xi, yi = intersection(2.0, 0.9, 0.8, 0.6)
    assert rectifying_y(xi, 2.0, 0.9) == pytest.approx(yi)
    assert q_line_y(xi, 0.8, 0.6) == pytest.approx(yi)

def test_stripping_y_through_xB():
    assert stripping_y(0.3, 2.0, 0.9, 0.8, 0.6, 0.3) == pytest.approx(0.3)

def test_bad_intersection():
    with pytest.raises(ValueError):
        intersection(-1.0, 0.9, 0.8, 0.6)

def test_bad_q_line_y():
    with pytest.raises(ValueError):
        q_line_y(0.5, 1, 0.6)
    with pytest.raises(ValueError):
        q_line_y(0.5, 0.8, -0.1)

def test_bad_rectifying_y():
    with pytest.raises(ValueError):
        rectifying_y(0.5, -1, 0.9)

    with pytest.raises(ValueError):
        rectifying_y(0.5, 2.0, -0.1)