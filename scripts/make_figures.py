"""Shared helpers for the figures of the AAE251 lecture notes.

Each chapter has its own figure script, scripts/make_chapter_N_figures.py, with one
function per figure. A figure script imports this module:

    from make_figures import plt, np, save, INK, GOLD, AGED, STEEL, SERIES

    def lift_curve():
        fig, ax = plt.subplots(figsize=(6.4, 4.2))
        ...
        save(fig, "lift-curve", chapter=3)

save() writes notes/chapter-N/figures/<name>.svg with the text kept as text
(svg.fonttype = none), so it scales, can be selected and is read by a screen reader.
Set FIG_PREVIEW=<folder> to also write a PNG copy, and look at it before using the figure.
A rerun writes identical files (fixed hash salt, no date in the metadata).

A figure drawn from data asserts the effect it exists to show. Values that also appear
on the page are computed here and never typed twice.
"""
import os
from pathlib import Path

import numpy as np  # noqa: F401  (imported by the figure scripts)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NOTES = Path(__file__).resolve().parents[1] / "notes"
PREVIEW = os.environ.get("FIG_PREVIEW")  # optional PNG copies for checking

plt.rcParams.update({
    "svg.fonttype": "none",
    "svg.hashsalt": "aae251-lecture-notes",
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 12,
    "axes.edgecolor": "#000000",
    "axes.labelcolor": "#000000",
    "xtick.color": "#000000",
    "ytick.color": "#000000",
    "savefig.facecolor": "white",
})

INK = "#000000"
# Purdue palette for schematics: gold fills and rules, aged gold and steel for lines and text.
GOLD, DUST, LIGHT, AGED, STEEL = "#CFB991", "#EBD99F", "#F5EFDC", "#8E6F3E", "#555960"
# Okabe-Ito colors for data series, in the order to use them. Pair each with a marker
# or a line style: color is never the only way a series is told apart.
SERIES = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#000000"]


def save(fig, name, chapter):
    """Write notes/chapter-<chapter>/figures/<name>.svg (and a PNG preview when asked)."""
    out = NOTES / f"chapter-{chapter}" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / f"{name}.svg", bbox_inches="tight", pad_inches=0.1, metadata={"Date": None})
    if PREVIEW:
        Path(PREVIEW).mkdir(parents=True, exist_ok=True)
        fig.savefig(Path(PREVIEW) / f"{name}.png", dpi=110, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    print("wrote", f"chapter-{chapter}/figures/{name}.svg")
