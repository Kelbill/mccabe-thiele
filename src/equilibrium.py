import numpy as np

def _check_composition(value, name):
    value = np.asarray(value, dtype=float)
    if np.any(value < 0) or np.any(value > 1):
        raise ValueError(f"{name} must be between 0 and 1, got min={value.min()}, max={value.max()}")
    return

def _check_alpha(alpha):
    if alpha <= 1:
        raise ValueError(f"alpha must be greater than 1, got {alpha}")
    return

def y_eq(x, alpha):
    x = np.asarray(x, dtype=float)
    _check_composition(x, "x")
    _check_alpha(alpha)
    y = (alpha * x) / (1 + (alpha - 1) * x)
    return y

def x_eq(y, alpha):
    y = np.asarray(y, dtype=float)
    _check_composition(y, "y")
    _check_alpha(alpha)
    x = y / (alpha - (alpha - 1) * y)
    return x

