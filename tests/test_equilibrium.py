import numpy as np
import pytest
from equilibrium import y_eq, x_eq

def test_endpoints():
    # y_eq(0, a) should be 0 and y_eq(1, a) should be 1
    assert y_eq(0, 2.5) == pytest.approx(0)
    assert y_eq(1, 2.5) == pytest.approx(1,rel=1e-4)
    with pytest.raises(ValueError):
        y_eq(-0.1, 2.5)

def test_known_value():
    # y_eq(0.5, 2.5) is about 0.7143, use pytest.approx
    assert y_eq(0.5, 2.5) == pytest.approx(0.7143, rel=1e-4)

def test_bad_alpha_raises_error():
    with pytest.raises(ValueError):
        y_eq(0.5, 1)
    with pytest.raises(ValueError):
        y_eq(0.5, 0.5)

def test_bad_x_raises_error():
    with pytest.raises(ValueError):
        y_eq(-0.1, 2.5)
    with pytest.raises(ValueError):
        y_eq(1.1, 2.5)

def test_round_trip():
    # Test that x_eq(y_eq(x, alpha), alpha) == x for a range of x and alpha
    x_values = np.linspace(0, 1, 10)
    alpha_values = [1.5, 2.0, 3.0]
    for alpha in alpha_values:
        for x in x_values:
            y = y_eq(x, alpha)
            x_recovered = x_eq(y, alpha)
            assert x_recovered == pytest.approx(x, rel=1e-4)

def test_array_shape():
    # Test that y_eq and x_eq can handle numpy arrays
    x_array = np.array([0.0, 0.5, 1.0])
    alpha = 2.5
    y_array = y_eq(x_array, alpha)
    assert y_array.shape == x_array.shape
    x_recovered_array = x_eq(y_array, alpha)
    assert np.allclose(x_recovered_array, x_array, rtol=1e-4)

def test_curve_above_diagonal():
    # For alpha > 1, y_eq(x, alpha) should be above the diagonal y=x for 0 < x < 1
    x_values = np.linspace(0, 1, 100)
    alpha = 2.5
    y_values = y_eq(x_values, alpha)
    assert np.all(y_values[1:-1] > x_values[1:-1])  # gicompare tanan in-between values sa y na dapat mas dako sa in between values sa x 