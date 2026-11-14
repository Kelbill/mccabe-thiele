import pytest
from stages import step_stages

def test_known_case():
    #step_stages(alpha, R, xD, q, xF, xB, max_stages=500)
    n, feed, points = step_stages(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    assert n == 7
    assert feed == 3
    assert points[0] == (0.9, 0.9)
    assert points[1][0] == pytest.approx(0.7826, abs=1e-4)

def test_higher_R_fewer_stages():
    n1, feed1 = step_stages(2.5, 1.5, 0.9, 1, 0.6, 0.1)
    n2, feed2 = step_stages(2.5, 1.0, 0.9, 1, 0.6, 0.1)
    assert n1 < n2
    assert feed1 < feed2

def test_bad_R():
    with pytest.raises(ValueError):
        step_stages(2.5, 0.5, 0.9, 1, 0.6, 0.1)

def test_feed_between_stage_1_and_n():
    n, feed = step_stages(2.5, 2.0, 0.9, 1, 0.6, 0.1)
    assert feed > 1 and feed < n
