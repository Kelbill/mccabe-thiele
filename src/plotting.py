import numpy as np
import matplotlib.pyplot as plt

from equilibrium import y_eq
from operating_lines import intersection
from stages import step_stages


def make_diagram(alpha, R, xD, q, xF, xB):

    n, feed_stage, points = step_stages(alpha, R, xD, q, xF, xB)
    xi, yi = intersection(R, xD, q, xF)
    fig, ax = plt.subplots(figsize=(7, 7))
    x_curve = np.linspace(0, 1, 200)

    ax.plot(x_curve, y_eq(x_curve, alpha), label="Equilibrium curve")     # y_eq of x_curve
    ax.plot([0, 1], [0, 1], "k--", label="y = x")

    ax.plot([xi, xD], [yi, xD], label="Rectifying line")  # y at xD is xD
    ax.plot([xB, xi], [xB, yi], label="Stripping line")   # y at xB is xB
    ax.plot([xF, xi], [xF, yi], label="q-line")           # y at xF is xF

    xs, ys = zip(*points)
    ax.plot(xs, ys, label="Stages")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("x (liquid mole fraction)")
    ax.set_ylabel("y (vapor mole fraction)")
    ax.set_title(f"McCabe-Thiele: {n} stages, feed on stage {feed_stage}")
    ax.legend()
    ax.grid(True)

    return fig