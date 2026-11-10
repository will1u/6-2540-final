"""Shared plot style for the report figures (Claude-authored).

Constants: column widths, the series colours (fixed order), the colour rules for the E1 / E2 / A30 / B60 / NODET
cases, and line styles that read in greyscale. apply() sets matplotlib rcParams. save(fig, name) writes
report/<name>.pdf and report/<name>.png at 300 dpi.

Used by make_die_map.py and make_report_figures.py. Run those from design/sim (see design/figures/README.md).
"""

import os

import matplotlib as mpl
import matplotlib.pyplot as plt

W1 = 3.4                      # inches, one journal column
W2 = 7.0                      # inches, two columns

BLUE = "#2a78d6"              # series 1; E2 (6 um Au)
ORANGE = "#eb6834"            # series 2; E1 (0.35 um Au)
AQUA = "#1baf7a"              # series 3; NODET
YELLOW = "#eda100"            # series 4
SERIES = [BLUE, ORANGE, AQUA, YELLOW]

INK = "#0b0b0b"               # text and axis ink
AXIS = "#898781"              # spines and ticks
GRID = "#e1e0d9"              # hairline grid

# (line style, marker) pairs, one per series, so each reads in greyscale
STYLE_SOLID = ("-", "o")      # A30
STYLE_DASHED = ("--", "s")    # B60
STYLE_DASHDOT = ("-.", "^")
STYLE_DOTTED = (":", "D")

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report")


def apply():
    """Set the report rcParams. Call once before making any figure."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial"],
        "font.size": 8,
        "axes.labelsize": 9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "lines.linewidth": 1.5,
        "lines.markersize": 4.5,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.labelcolor": INK,
        "ytick.labelcolor": INK,
        "axes.edgecolor": AXIS,
        "xtick.color": AXIS,
        "ytick.color": AXIS,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "axes.grid": True,
        "axes.grid.axis": "both",
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "axes.axisbelow": True,
        "axes.prop_cycle": mpl.cycler(color=SERIES),
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


def save(fig, name):
    """Write report/<name>.pdf and report/<name>.png (300 dpi, tight bounding box)."""
    os.makedirs(OUT, exist_ok=True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(OUT, f"{name}.{ext}"), dpi=300, bbox_inches="tight")
    plt.close(fig)
