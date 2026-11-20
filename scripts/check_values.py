#!/usr/bin/env python3
"""Check that every number the figure code recorded is printed on its page.

The page modules of Chapter 2 record each number they compute for the page with
record(page, key, text); make_chapter_2_figures.py writes them to
scripts/chapter_2/values.json. This script requires each recorded string on its page,
notes/chapter-2/<page>.md. Run from the book folder:

    python3 -B scripts/check_values.py              all pages in values.json
    python3 -B scripts/check_values.py p21 p23      only these pages (tag or file stem)
    python3 -B scripts/check_values.py --strict     also fail when a page is not written yet

Before comparing, the page is normalized: "{,}" becomes ",", the math spaces "\\,", "\\;",
"\\:" and "\\ " and non-breaking spaces become a space, and runs of spaces become one.
A value must stand alone: "7.6" does not match inside "7.669", and "105" not inside "1,050".
Each miss is printed as "page: key: text"; the exit status is 1 on any miss.

It then runs scripts/check_chains.py on every page: every printed calculation (an
expression of printed numbers "= result") must give its printed result from the printed
operands. A miss there also sets the exit status to 1.
"""
import json
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
VALUES = BOOK / "scripts" / "chapter_2" / "values.json"
CHAPTER = BOOK / "notes" / "chapter-2"
TAGS = {"p21": "orbit-properties", "p22": "orbit-transfers", "p23": "launch-to-orbit",
        "p24": "patched-conics", "p25": "ground-tracks-and-orbit-lifetime"}


def normalize(s):
    s = s.replace("{,}", ",")
    # A number that carries a superscript is braced on the page, so that MathML reads it as
    # one number ({10}^{5}, {30.4}^\circ); compare it as 10^{5}. Only braces that hold
    # nothing but the number go, so a value still has to stand alone.
    s = re.sub(r"\{(\d[\d.,]*)\}(?=\^)", r"\1", s)
    s = re.sub(r"\\[,;:! ]", " ", s)
    s = s.replace(" ", " ").replace(" ", " ").replace(" ", " ")
    return re.sub(r"[ \t]+", " ", s)


def found(value, page):
    v = normalize(value).strip()
    pat = r"(?<![\d.,])" + re.escape(v) + r"(?![\d]|[.,]\d)"
    return re.search(pat, page) is not None


def main(argv):
    strict = "--strict" in argv
    want = {TAGS.get(a, a) for a in argv if not a.startswith("--")}
    if not VALUES.exists():
        print("check_values: no scripts/chapter_2/values.json; run scripts/make_chapter_2_figures.py first")
        return 1
    data = json.loads(VALUES.read_text(encoding="utf-8"))
    misses = n_checked = 0
    for page, vals in sorted(data.items()):
        if want and page not in want:
            continue
        path = CHAPTER / f"{page}.md"
        if not path.exists():
            print(f"{page}: page not written ({len(vals)} values not checked)")
            misses += 1 if strict else 0
            continue
        text = normalize(path.read_text(encoding="utf-8"))
        for key, value in sorted(vals.items()):
            n_checked += 1
            if not found(value, text):
                print(f"{page}: {key}: {value}")
                misses += 1
    print(f"check_values: {n_checked} values checked, {'ok' if not misses else str(misses) + ' missing'}")
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import check_chains                                       # noqa: E402
    chains = check_chains.main([])
    return 1 if misses or chains else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
