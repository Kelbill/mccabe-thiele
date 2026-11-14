import pytest
from operating_lines import rectifying_y, q_line_y, intersection, stripping_y

def test_rectifying_y():
    # Test rectifying_y with known values
    x = 0.5
    R = 2.0
    xD = 0.9
    expected_y = (R / (R + 1)) * x + (1 / (R + 1)) * xD
    assert rectifying_y(x, R, xD) == pytest.approx(expected_y)

def test_q_line_y():
    # Test q_line_y with known values
    x = 0.5
    q = 0.8
    xF = 0.6
    expected_y = (q / (q + 1)) * x + (1 / (q + 1)) * xF
    assert q_line_y(x, q, xF) == pytest.approx(expected_y)

def test_intersection():
    # Test intersection with known values
    R = 2.0
    xD = 0.9
    q = 0.8
    xF = 0.6
    y_rectifying = rectifying_y(xF, R, xD)
    y_q_line = q_line_y(xF, q, xF)
    assert intersection(R, xD, q, xF) == pytest.approx(y_rectifying)
    assert intersection(R, xD, q, xF) == pytest.approx(y_q_line)

def test_stripping_y():
    # Test stripping_y with known values
    x = 0.5
    R = 2.0
    xB = 0.1
    expected_y = (R / (R + 1)) * x + (1 / (R + 1)) * xB
    assert stripping_y(x, R, xB) == pytest.approx(expected_y)

def test_bad_stripping_y():
    x = 0.5
    R = 2.0
    xB = 0.1
    # Test that stripping_y raises ValueError for invalid R
    with pytest.raises(ValueError):
        stripping_y(x, -1, xB)

    # Test that stripping_y raises ValueError for invalid xB
    with pytest.raises(ValueError):
        stripping_y(x, R, -0.1)

def test_bad_intersection():
    R = -1.0
    xD = 0.9
    q = 0.8
    xF = 0.6
    # Test that intersection raises ValueError for invalid R
    with pytest.raises(ValueError):
        intersection(R, xD, q, xF)

    # Test that intersection raises ValueError for invalid xD
    with pytest.raises(ValueError):
        intersection(2.0, -0.1, q, xF)

    # Test that intersection raises ValueError for invalid q
    with pytest.raises(ValueError):
        intersection(2.0, xD, 1.2, xF)

    # Test that intersection raises ValueError for invalid xF
    with pytest.raises(ValueError):
        intersection(2.0, xD, q, -0.1)

def test_bad_q_line_y():
    x = 0.5
    q = 1.2
    xF = 0.6
    # Test that q_line_y raises ValueError for invalid q
    with pytest.raises(ValueError):
        q_line_y(x, q, xF)

    # Test that q_line_y raises ValueError for invalid xF
    with pytest.raises(ValueError):
        q_line_y(x, 0.8, -0.1)

def test_bad_rectifying_y():
    x = 0.5
    R = 2.0
    xD = 0.9
    # Test that rectifying_y raises ValueError for invalid R
    with pytest.raises(ValueError):
        rectifying_y(x, -1, xD)

    # Test that rectifying_y raises ValueError for invalid xD
    with pytest.raises(ValueError):
        rectifying_y(x, R, -0.1)