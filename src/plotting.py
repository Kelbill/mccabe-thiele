import numpy as np
import matplotlib.pyplot as plt

from equilibrium import y_eq
from operating_lines import intersection
from stages import step_stages

BG = "#FBFAF6"
INK = "#1C1A15"
GRAY = "#6B665B"
MUTED = "#8F8A7D"
GREEN = "#1B7A43"
GRID = "#E8E5DB"
RECT = "#D9622B"    # burnt orange
STRIP = "#2F6DB5"   # blue
QLINE = "#8A5CC2"   # purple


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
    ax.plot([xF, xi], [xF, yi], color=QLINE, lw=2, label="Q-line")

    xs, ys = zip(*points)
    ax.plot(xs, ys, color=GREEN, lw=2.4, label="Stages")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("X  (LIQUID MOLE FRACTION)", color=MUTED, fontfamily="monospace", fontsize=8)
    ax.set_ylabel("Y  (VAPOR MOLE FRACTION)", color=MUTED, fontfamily="monospace", fontsize=8)
    ax.set_title(
        f"McCabe-Thiele: {n} stages, feed on stage {feed_stage}",
        color=INK, loc="left", fontsize=13, fontweight="bold",
    )

    ax.tick_params(colors=MUTED, labelsize=8)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(GRID)
    ax.grid(True, color=GRID, lw=0.8)
    ax.legend(frameon=False, labelcolor=INK, fontsize=8, loc="lower right",
              prop={"family": "monospace", "size": 8})

    fig.tight_layout()
    return fig