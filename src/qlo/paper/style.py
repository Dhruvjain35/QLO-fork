"""One figure style for every paper figure: white background, serif text with STIX math, vector PDF output.

Colours are the Okabe-Ito colour-blind-safe set; every series also differs in marker and line style, so the figures
still read in grayscale. Ordered noise strengths use cividis (monotone luminance).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SINGLE, DOUBLE = 3.4, 7.0            # inches: single- and double-column widths

OKABE = {"black": "#000000", "orange": "#E69F00", "sky": "#56B4E9", "green": "#009E73", "yellow": "#F0E442",
         "blue": "#0072B2", "vermillion": "#D55E00", "purple": "#CC79A7", "gray": "#7F7F7F"}

# estimator -> (label, colour, marker, linestyle, filled)
EST = {
    "loschmidt": ("Loschmidt", OKABE["blue"], "o", "-", True),
    "swap_ancilla": ("ancilla SWAP", OKABE["vermillion"], "s", "--", True),
    "swap_destructive": ("destructive SWAP", OKABE["orange"], "^", ":", False),
    "hadamard_u": ("Hadamard U-statistic", OKABE["green"], "D", "-.", True),
}
EST["swap"] = ("SWAP test", *EST["swap_ancilla"][1:])          # Stage 7 / B3 naming of the ancilla SWAP test

RC = {
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
    "font.family": "serif", "font.serif": ["STIXGeneral", "DejaVu Serif"], "mathtext.fontset": "stix",
    "font.size": 8, "axes.labelsize": 8, "axes.titlesize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 6.5, "legend.frameon": False, "legend.handlelength": 2.2,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.minor.width": 0.4,
    "ytick.minor.width": 0.4, "xtick.direction": "in", "ytick.direction": "in", "xtick.top": True, "ytick.right": True,
    "lines.linewidth": 1.0, "lines.markersize": 3.5, "errorbar.capsize": 1.5,
    "axes.spines.top": True, "axes.spines.right": True, "axes.grid": False,
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "axes.unicode_minus": True, "text.color": "black", "axes.labelcolor": "black", "xtick.color": "black",
    "ytick.color": "black", "image.cmap": "cividis",
}


def apply() -> None:
    plt.rcParams.update(RC)


def panel_label(ax, letter: str, x: float = -0.16, y: float = 1.04) -> None:
    ax.text(x, y, f"({letter})", transform=ax.transAxes, fontsize=9, fontweight="bold", va="bottom", ha="left")


def marker_kw(est: str, size: float | None = None) -> dict:
    label, c, m, ls, filled = EST[est]
    kw = {"color": c, "marker": m, "linestyle": ls, "label": label, "markeredgecolor": c,
          "markerfacecolor": c if filled else "white"}
    if size is not None:
        kw["markersize"] = size
    return kw
