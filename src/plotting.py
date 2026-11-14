import numpy as np
import matplotlib.pyplot as plt

from equilibrium import y_eq
from operating_lines import intersection
from stages import step_stages

plt.rcParams["font.family"] = "monospace"

BG = "#211F1A"
INK = "#F2EFE6"
MUTED = "#8F8A7D"
GRID = "#34312A"
GREEN = "#3DBA6F"
RECT = "#F0884D"    # orange
STRIP = "#5B9BE0"   # blue
QLINE = "#B48AE8"   # purple


def make_diagram(alpha, R, xD, q, xF, xB):
    n, feed_stage, points = step_stages(alpha, R, xD, q, xF, xB)
    xi, yi = intersection(R, xD, q, xF)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    x_curve = np.linspace(0, 1, 200)
    ax.plot(x_curve, y_eq(x_curve, alpha), color=INK, lw=2.2, label="Equilibrium curve")
    ax.plot([0, 1], [0, 1], color=MUTED, ls="--", lw=1, label="y = x")
    ax.plot([xi, xD], [yi, xD], color=RECT, lw=2, label="Rectifying line")
    ax.plot([xB, xi], [xB, yi], color=STRIP, lw=2, label="Stripping line")
    ax.plot([xF, xi], [xF, yi], color=QLINE, lw=2, label="q-line")

    xs, ys = zip(*points)
    ax.plot(xs, ys, color=GREEN, lw=2.4, label="Stages")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("X  (LIQUID MOLE FRACTION)", color=MUTED, fontsize=8)
    ax.set_ylabel("Y  (VAPOR MOLE FRACTION)", color=MUTED, fontsize=8)

    ax.tick_params(colors=MUTED, labelsize=8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.grid(True, color=GRID, lw=0.8)
    ax.legend(frameon=False, labelcolor=INK, fontsize=8, loc="lower right")

    fig.tight_layout()
    return fig