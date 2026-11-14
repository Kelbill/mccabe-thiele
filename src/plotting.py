from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager

from equilibrium import y_eq
from operating_lines import intersection
from stages import step_stages

_fonts_dir = Path(__file__).parent.parent / "fonts"
_family = "sans-serif"
for _f in sorted(_fonts_dir.glob("Oswald*.ttf")):
    font_manager.fontManager.addfont(str(_f))
    _family = font_manager.FontProperties(fname=str(_f)).get_name()
plt.rcParams["font.family"] = _family

PALETTES = {
    "light": {
        "BG": "#FBFAF6",
        "INK": "#1C1A15",
        "MUTED": "#8F8A7D",
        "GRID": "#E8E5DB",
        "RED": "#E5484D",
        "RECT": "#D9962B",
        "STRIP": "#2F6DB5",
        "QLINE": "#8A5CC2",
    },
    "dark": {
        "BG": "#211F1A",
        "INK": "#F2EFE6",
        "MUTED": "#8F8A7D",
        "GRID": "#34312A",
        "RED": "#E5484D",
        "RECT": "#E8B84A",
        "STRIP": "#5B9BE0",
        "QLINE": "#B48AE8",
    },
}


def make_diagram(alpha, R, xD, q, xF, xB, dark=False):
    c = PALETTES["dark" if dark else "light"]

    n, feed_stage, points = step_stages(alpha, R, xD, q, xF, xB)
    xi, yi = intersection(R, xD, q, xF)

    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor(c["BG"])
    ax.set_facecolor(c["BG"])

    x_curve = np.linspace(0, 1, 200)
    ax.plot(x_curve, y_eq(x_curve, alpha), color=c["INK"], lw=2.2, label="Equilibrium curve")
    ax.plot([0, 1], [0, 1], color=c["MUTED"], ls="--", lw=1, label="y = x")
    ax.plot([xi, xD], [yi, xD], color=c["RECT"], lw=2, label="Rectifying line")
    ax.plot([xB, xi], [xB, yi], color=c["STRIP"], lw=2, label="Stripping line")
    ax.plot([xF, xi], [xF, yi], color=c["QLINE"], lw=2, label="q-line")

    xs, ys = zip(*points)
    ax.plot(xs, ys, color=c["RED"], lw=2.4, label="Stages")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("X  (LIQUID MOLE FRACTION)", color=c["MUTED"], fontsize=9)
    ax.set_ylabel("Y  (VAPOR MOLE FRACTION)", color=c["MUTED"], fontsize=9)

    ax.tick_params(colors=c["MUTED"], labelsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(c["GRID"])
    ax.grid(True, color=c["GRID"], lw=0.8)
    ax.legend(frameon=False, labelcolor=c["INK"], fontsize=9, loc="lower right",
              prop={"family": _family, "size": 9})

    fig.tight_layout()
    return fig