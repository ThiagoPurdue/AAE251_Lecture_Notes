"""The record of printed values and the figure saver of Chapter 3, Aerodynamics.

Page modules do not import this file directly; they use the one import line

    from chapter_3.common import *

which brings Chapter 1's style (line weights, fills, arrow kinds, `pt`, `kind_arrow`,
`flow_arrow`, `moment_arrow`, `legend_key`) and then rebinds `record`, `write_values`,
`save_figure`, `VALUES`, `WRITTEN` and `PAGES` to Chapter 3's own record (this module).
"""
import sys
from pathlib import Path

if __name__ not in ("chapter_3.style", "__main__"):
    raise ImportError("import this module as chapter_3.style (or through chapter_3.common)")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from figkit import Chapter  # noqa: E402
from make_figures import NOTES  # noqa: E402,F401
import re as _re  # noqa: E402
import figkit as _figkit  # noqa: E402

# Subscripts of Chapter 3 symbols that hold two or more letters ($c_{m,c/4}$, $c_{m,\mathrm{ac}}$,
# $C_{D,0}$ is fine, $(L/D)_\max$, $\alpha_\mathrm{eff}$) are set at the kit's word-subscript size
# (figkit.SUB_WORD) so they read at 10 pt on the page; the kit's own pattern covers \mathrm{word}
# and \infty only. Rebinding the pattern here affects only a run that imports Chapter 3, so the
# figures of Chapters 1 and 2 are unchanged (their runners never import this module).
_figkit._WORD_SUB = _re.compile(r"_\{?\\(?:mathrm\{[A-Za-z]{2,}\}|infty)|_\\max|_\{[^{}]*[A-Za-z][^{}]*[A-Za-z][^{}]*\}"
                                r"|_\{[^{}]*\\mathrm\{[A-Za-z]{2,}\}[^{}]*\}")

PAGES = {
    "p31": "wind-tunnels",
    "p32": "airfoil-and-finite-wing",
    "p33": "drag-polar",
    "p34": "wing-loading",
}
CHAPTER = Chapter(3, PAGES, Path(__file__).resolve().parent)
VALUES, VALUES_FILE, WRITTEN = CHAPTER.VALUES, CHAPTER.VALUES_FILE, CHAPTER.WRITTEN
record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure

__all__ = ["NOTES", "PAGES", "CHAPTER", "VALUES", "VALUES_FILE", "WRITTEN", "record", "write_values", "save_figure"]
