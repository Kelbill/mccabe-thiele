import matplotlib
matplotlib.use("Agg") 

import matplotlib.pyplot as plt
import pytest
from matplotlib.figure import Figure

from plotting import make_diagram

#make_diagram(alpha, R, xD, q, xF, xB)
def test_returns_figure():
    fig = make_diagram(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    assert isinstance(fig, Figure)
    plt.close(fig)


def test_title_has_stage_count():
    fig = make_diagram(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    ax = fig.axes[0]
    assert "7 stages" in ax.get_title()
    assert "feed on stage 3" in ax.get_title()
    plt.close(fig)


def test_has_six_lines():
    # equilibrium, diagonal, rectifying, stripping, q-line, stages
    fig = make_diagram(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    ax = fig.axes[0]
    assert len(ax.lines) == 6
    plt.close(fig)

def test_bad_R_raises():
    with pytest.raises(ValueError):
        make_diagram(2.5, -1, 0.9, 1, 0.6, 0.1)
    with pytest.raises(ValueError):
        make_diagram(2.5, 0.5, 0.9, 1, 0.6, 0.1)

def test_staircase_ends_at_xB():
    fig = make_diagram(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    ax = fig.axes[0]
    xs, ys = zip(*ax.lines[-1].get_xydata())
    assert xs[-1] <= 0.1 
    assert xs[0] == 0.9
    assert all(a >= b for a, b in zip(xs, xs[1:]))
    plt.close(fig)