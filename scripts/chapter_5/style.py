"""The record of printed values and the figure saver of Chapter 5, Aircraft Performance and Propulsion.

Page modules do not import this file directly; they use the one import line

    from chapter_5.common import *

which brings Chapter 1's style (line weights, fills, arrow kinds, `pt`, `kind_arrow`,
`flow_arrow`, `moment_arrow`, `legend_key`) and then rebinds `record`, `write_values`,
`save_figure`, `VALUES`, `WRITTEN` and `PAGES` to Chapter 5's own record (this module).
"""
import re as _re
import sys
from pathlib import Path

if __name__ not in ("chapter_5.style", "__main__"):
    raise ImportError("import this module as chapter_5.style (or through chapter_5.common)")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import figkit as _figkit  # noqa: E402
from figkit import Chapter  # noqa: E402
from make_figures import NOTES  # noqa: E402,F401

# Widen figkit's word-subscript pattern so multi-letter subscripts such as $T_{R,\min}$,
# $P_{R,\min}$, $V_{T_R,\min}$, $C_{L,\max}$, $m_{\mathrm{ad}}$, and $s_{\mathrm{LO}}$ stay at
# SUB_WORD (0.88 of the main size, at least 10 pt on the page). Rebinding here affects only a
# run that imports Chapter 5, so Chapters 1 to 3 draw identically to before.
_figkit._WORD_SUB = _re.compile(
    r"_\{?\\(?:mathrm\{[A-Za-z]{2,}\}|infty)"
    r"|_\\(?:max|min)"
    r"|_\{[^{}]*(?:\\max|\\min|\\mathrm\{[A-Za-z]{2,}\})[^{}]*\}"
    r"|_\{[^{}]*[A-Za-z][^{}]*[A-Za-z][^{}]*\}"
    r"|_.*_"
)

PAGES = {
    "p51": "thrust-and-power",
    "p52": "range-and-endurance",
    "p53": "climb-and-ceiling",
    "p54": "engines",
    "p55": "constraint-diagram-and-field-length",
}
CHAPTER = Chapter(5, PAGES, Path(__file__).resolve().parent)
VALUES, VALUES_FILE, WRITTEN = CHAPTER.VALUES, CHAPTER.VALUES_FILE, CHAPTER.WRITTEN
record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure

__all__ = ["NOTES", "PAGES", "CHAPTER", "VALUES", "VALUES_FILE", "WRITTEN", "record", "write_values", "save_figure"]
