"""The record of printed values and the figure saver of Chapter 4, Rocket Design.

Page modules do not import this file directly; they use the one import line

    from chapter_4.common import *

which brings Chapter 1's style (line weights, fills, arrow kinds, `pt`, `kind_arrow`,
`flow_arrow`, `legend_key`) and then rebinds `record`, `write_values`, `save_figure`, `VALUES`,
`WRITTEN` and `PAGES` to Chapter 4's own record (this module).
"""
import sys
from pathlib import Path

if __name__ not in ("chapter_4.style", "__main__"):
    raise ImportError("import this module as chapter_4.style (or through chapter_4.common)")

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from figkit import Chapter  # noqa: E402
from make_figures import NOTES  # noqa: E402,F401
import re as _re  # noqa: E402
import figkit as _figkit  # noqa: E402

# Word subscripts of Chapter 4 symbols are set at the kit's word-subscript size (figkit.SUB_WORD),
# so they read at 10 pt on the page and pass the kit's SVG check (10.5 pt for a word subscript).
# The kit's own pattern covers \mathrm{word} and \infty. This adds, as Chapter 3's style does,
# a braced subscript of two or more letters ($I_{sp}$, $m_{pay}$, $f_{inert}$, $c_{m,ac}$), \max,
# and \text{word} ($I_\text{sp}$, the form the pages use in their own math). The change is made
# at import of chapter_4, so Chapters 1 to 3 (whose runners never import it) draw as before.
# A label with two or more subscripts ("$p_e < p_a$", "Area ratio, $A_e/A_t$") is set at the same size:
# matplotlib writes the small glyphs of one label next to each other in the SVG, and the kit's SVG check
# then reads two single-letter subscripts as one word subscript ("ea"); at 0.88 of a 12 pt label they pass
# (10.6 pt). Such a label must be 12 pt (FS_LABEL): at 11 pt the subscripts are 9.7 pt and the check stops it.
_figkit._WORD_SUB = _re.compile(r"_\{?\\(?:mathrm\{[A-Za-z]{2,}\}|infty)|_\\max|_\{[^{}]*[A-Za-z][^{}]*[A-Za-z][^{}]*\}"
                                r"|_\{[^{}]*\\mathrm\{[A-Za-z]{2,}\}[^{}]*\}|_\{?\\text\{[A-Za-z ]{2,}\}|_[^_$]*\$?[^_]*_")

PAGES = {
    "p41": "thrust-and-specific-impulse",
    "p42": "rocket-equation",
    "p43": "multistage-rockets",
    "p44": "propellant-selection",
    "p45": "engines-and-tanks",
}
CHAPTER = Chapter(4, PAGES, Path(__file__).resolve().parent)
VALUES, VALUES_FILE, WRITTEN = CHAPTER.VALUES, CHAPTER.VALUES_FILE, CHAPTER.WRITTEN
record, write_values, save_figure = CHAPTER.record, CHAPTER.write_values, CHAPTER.save_figure

__all__ = ["printed", "NOTES", "PAGES", "CHAPTER", "VALUES", "VALUES_FILE", "WRITTEN", "record", "write_values", "save_figure"]


def printed(x, sig=4, **kw):
    """The printed string of x (chapter_1.style.fmt) and the value a reader takes from it, so that the
    next step of a worked example uses the digits shown. Example: printed(3168.63) -> ('3,169', 3169.0)"""
    from chapter_1.style import fmt
    s = fmt(x, sig, **kw)
    return s, float(s.replace(",", "").replace("\u2212", "-"))
