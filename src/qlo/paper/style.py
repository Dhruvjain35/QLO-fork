"""One figure style for every paper figure: white background, serif text with STIX math, vector PDF output.

Colours are the Okabe-Ito colour-blind-safe set; every series also differs in marker and line style, so the figures
still read in grayscale. Ordered noise strengths use cividis (monotone luminance).

Sizes follow the Quantum Science and Technology figure guidelines (Phase 8 guidance, section 4): figures are drawn at
their final width, 8.5 cm for one column or 15 cm for the full width, so every font size below is the printed size,
and all text is between 8 and 12 pt. `check` enforces both rules; the builder refuses a figure that breaks them.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

CM = 1 / 2.54                         # inches per cm
SINGLE, DOUBLE = 8.5 * CM, 15.0 * CM  # final printed widths: one column, full width
MIN_PT, MAX_PT = 8.0, 12.0            # allowed text sizes at the final width

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
    "font.size": 8, "axes.labelsize": 9, "axes.titlesize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
    "legend.fontsize": 8, "legend.frameon": False, "legend.handlelength": 2.0, "legend.borderaxespad": 0.3,
    "legend.labelspacing": 0.3, "legend.columnspacing": 1.0,
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
    ax.text(x, y, f"({letter})", transform=ax.transAxes, fontsize=10, fontweight="bold", va="bottom", ha="left")


def marker_kw(est: str, size: float | None = None) -> dict:
    label, c, m, ls, filled = EST[est]
    kw = {"color": c, "marker": m, "linestyle": ls, "label": label, "markeredgecolor": c,
          "markerfacecolor": c if filled else "white"}
    if size is not None:
        kw["markersize"] = size
    return kw


def check(fig) -> list[str]:
    """Return every way `fig` breaks the journal size rules (empty list = compliant)."""
    import matplotlib.text as mtext
    problems = []
    w = fig.get_size_inches()[0]
    if not any(abs(w - target) < 1e-9 for target in (SINGLE, DOUBLE)):
        problems.append(f"width {w / CM:.2f} cm is neither 8.5 cm nor 15 cm")
    fig.canvas.draw()                                      # creates the tick labels
    for t in fig.findobj(mtext.Text):
        if t.get_visible() and t.get_text().strip() and not MIN_PT <= t.get_fontsize() <= MAX_PT:
            problems.append(f"{t.get_fontsize():g} pt text {t.get_text()!r}")
    return problems
