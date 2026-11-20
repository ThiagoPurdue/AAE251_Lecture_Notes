#!/usr/bin/env python3
"""Check the pages of the book against its standing rules. Needs only the book folder.

  python3 scripts/check_pages.py

Stops with status 1 when a page under notes/ has

  - a date: a month with a day or a year, a weekday, a semester ("Spring 2027"), a week
    number ("Week 5"). The notes carry no dates, so they stay right from year to year.
    A year in a reference ("Anderson (2016)") is fine.
  - an assignment: a homework set (HW3), a project milestone (PM2), a Standards Check
    (SC4) or a due date. The notes do not hold or announce assignments.
  - an em-dash or en-dash in prose (a page range in the References section is fine).
  - a figure with no alt text, or a figure or table with no caption.

Code blocks and math are skipped.
"""
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
MONTH = (r"(?:January|February|March|April|May|June|July|August|September|October|November|December|"
         r"Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.?")
RULES = [
    ("date", re.compile(rf"\b{MONTH} \d{{1,2}}\b|\b\d{{1,2}} {MONTH}(?= |,|\.|$)|\b{MONTH},? 20\d\d\b")),
    ("weekday", re.compile(r"\b(?:Mon|Tues|Wednes|Thurs|Fri|Satur|Sun)day\b")),
    ("semester", re.compile(r"\b(?:Spring|Summer|Fall|Autumn|Winter) 20\d\d\b|\bWeek \d+\b|\bfinals week\b", re.I)),
    ("assignment", re.compile(r"\bHW ?\d+[AB]?\b|\bPM ?\d\b|\bSC ?\d{1,2}\b|\bStandards Checks?\b|"
                              r"\bhomework\b|\bproject milestones?\b|\bdue (?:on|by|date)\b", re.I)),
    ("dash", re.compile("[—–]")),
]


def strip(text):
    """Blank out what the rules do not apply to, keeping the line numbers."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    text = re.sub(r"\A---\n.*?\n---\n", blank, text, flags=re.S)       # front matter
    text = re.sub(r"```.*?```", blank, text, flags=re.S)               # code blocks
    text = re.sub(r"\$\$.*?\$\$", blank, text, flags=re.S)             # display math
    text = re.sub(r"\$[^$\n]+\$", blank, text)                         # inline math
    return text


def check(path):
    raw = path.read_text(encoding="utf-8")
    text = strip(raw)
    errors = []
    refs = re.search(r"^## References\s*$", text, re.M)
    ref_line = text[:refs.start()].count("\n") + 1 if refs else 10 ** 9
    for n, line in enumerate(text.split("\n"), 1):
        for name, rule in RULES:
            if name == "dash" and n > ref_line:
                continue
            m = rule.search(line)
            if m:
                errors.append(f"{path.relative_to(BOOK)}:{n}: {name}: \"{m.group(0)}\"")
    # figures: alt text and a caption line; tables: a caption on the directive line
    for m in re.finditer(r"^:::+\{figure\}[^\n]*\n(.*?)^:::+\s*$", raw, re.S | re.M):
        n = raw[:m.start()].count("\n") + 1
        body = m.group(1)
        if not re.search(r"^:alt:\s*\S", body, re.M):
            errors.append(f"{path.relative_to(BOOK)}:{n}: figure with no :alt: text")
        if not [x for x in body.split("\n") if x.strip() and not x.startswith(":")]:
            errors.append(f"{path.relative_to(BOOK)}:{n}: figure with no caption")
    for m in re.finditer(r"^:::+\{table\}([^\n]*)$", raw, re.M):
        if not m.group(1).strip():
            errors.append(f"{path.relative_to(BOOK)}:{raw[:m.start()].count(chr(10)) + 1}: table with no caption")
    return errors


if __name__ == "__main__":
    pages = sorted(p for p in (BOOK / "notes").rglob("*.md") if "_parts" not in p.parts)
    errors = [e for p in pages for e in check(p)]
    for e in errors:
        print("ERROR:", e)
    print(f"pages: {len(pages)} checked, {'ok' if not errors else str(len(errors)) + ' problems'}")
    sys.exit(1 if errors else 0)
