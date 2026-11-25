#!/usr/bin/env python3
"""Make the figures and the printed values of Chapter 4, Rocket Design.

Runs every page module scripts/chapter_4/p4*_*.py (in name order): its make_all() draws
the figures into notes/chapter-4/figures/, then its values() records the numbers printed
on the page. Last, write_values() writes scripts/chapter_4/values.json, which
scripts/check_values.py compares with the pages. Run from the book folder:

    python3 -B scripts/make_chapter_4_figures.py            all pages
    python3 -B scripts/make_chapter_4_figures.py p41 p42    only these pages (values.json
                                                            keeps the other pages' entries)

Set FIG_PREVIEW=<folder> to also write a PNG of each figure, and look at every one.
Set FIG_LAYOUT=warn to list every layout problem and save the figure anyway (draft mode).
Shared code: scripts/chapter_4/ (API in scripts/chapter_4/README.md).
"""
import importlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from chapter_4 import style as O  # noqa: E402


def main(tags):
    modules = sorted(p.stem for p in (SCRIPTS / "chapter_4").glob("p4*_*.py"))
    if tags:
        unknown = [t for t in tags if not any(m.split("_")[0] == t for m in modules)]
        if unknown:
            raise SystemExit(f"no module for {', '.join(unknown)} in scripts/chapter_4 "
                             f"(found: {', '.join(modules) or 'none'})")
        modules = [m for m in modules if m.split("_")[0] in tags]
    for name in modules:
        print(f"== {name}")
        mod = importlib.import_module(f"chapter_4.{name}")
        ran = False
        for fn in ("make_all", "values"):
            if hasattr(mod, fn):
                getattr(mod, fn)()
                ran = True
        if not ran:
            print(f"   note: {name} has neither make_all() nor values()")
    O.write_values(only=[m.split("_")[0] for m in modules] if tags else None)

    # figures of the pages that ran which were not written in this run: renamed or dropped
    ran_tags = {m.split("_")[0] for m in modules}
    figdir = O.NOTES / "chapter-4" / "figures"
    stale = sorted(p.name for p in figdir.glob("p4*-*.svg")
                   if p.stem.split("-")[0] in ran_tags and p.stem not in O.WRITTEN)
    for s in stale:
        print(f"   stale figure, not written in this run: notes/chapter-4/figures/{s}")
    print(f"done: {len(modules)} page modules, {len(O.WRITTEN)} figures")


if __name__ == "__main__":
    main(sys.argv[1:])
