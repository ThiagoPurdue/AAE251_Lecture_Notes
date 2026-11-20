#!/usr/bin/env python3
"""Write the chapter and standard data of the book from the course's single source.

The book has five chapters, one for each group of technical standards, and one page per
standard. Nothing about a standard is typed on a page: this script reads
../_syllabus_build/standards.py (outside the book, in the course folder) and writes

  scripts/standards.json              chapters, standards, page slugs (read by the other scripts)
  notes/_parts/standards/<id>.md      the box that states the standard at the top of its page
  notes/_parts/chapters.md            the list of chapters and standards on the About page, and
                                      after the standards of a chapter, any other page that
                                      myst.yml places in that chapter (a page no standard assesses)

Run from the book folder after any change to the standards:

  python3 scripts/make_standards.py            write the files
  python3 scripts/make_standards.py --toc      also print the full toc block for myst.yml
  python3 scripts/make_standards.py --check    write nothing; stop if a file is out of date
  python3 scripts/make_standards.py --sources  write nothing; list the lecture decks behind each page

The files are committed, so the GitHub build does not need the course folder. In a copy
of the book outside the course folder, set AAE251_COURSE to the course folder. Dates,
Standards Check names and homework references are left out on purpose: the notes carry no
dates and no assignments.
"""
import json
import os
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
# The course folder is the book's parent. In a copy of the book elsewhere, set AAE251_COURSE.
COURSE = Path(os.environ.get("AAE251_COURSE", BOOK.parent))
if not (COURSE / "_syllabus_build" / "standards.py").exists():
    raise SystemExit(f"no _syllabus_build/standards.py in {COURSE}: run this in the course folder, "
                     "or set AAE251_COURSE to the course folder")
sys.dont_write_bytecode = True
sys.path.insert(0, str(COURSE / "_syllabus_build"))
import standards as S  # noqa: E402


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def chapter_title(module_text):
    """'Module 3: May the Force Be with You (Aerodynamics), Lectures 10-13' -> name and topic."""
    m = re.match(r"Module \d+: (.+?) \((.+)\), Lectures ([\d-]+)$", module_text)
    if not m:
        raise SystemExit(f"cannot read the module title: {module_text}")
    return m.group(1), m.group(2), m.group(3)


def collect():
    chapters = []
    for key in "12345":
        name, topic, lectures = chapter_title(S.MODULES[key])
        stds = []
        for s in S.STANDARDS:
            if s[1] != key:
                continue
            short = S.short_name(s[0])
            stds.append({"id": s[0], "name": short, "slug": slug(short), "statement": s[2],
                         "page": f"notes/chapter-{key}/{slug(short)}.md"})
        chapters.append({"number": int(key), "title": f"Chapter {key}: {topic}", "topic": topic,
                         "module": name, "lectures": lectures, "folder": f"notes/chapter-{key}",
                         "standards": stds})
    return chapters


def page_title(page):
    """The `title` of a page's front matter (notes/chapter-N/<page>.md), without quotes."""
    text = (BOOK / page).read_text(encoding="utf-8")
    front = re.match(r"---\n(.*?)\n---\n", text, re.S)
    m = re.search(r'^title:\s*(.+?)\s*$', front.group(1), re.M) if front else None
    if not m:
        raise SystemExit(f"{page}: no title in the front matter")
    return m.group(1).strip().strip('"').strip("'")


def toc_pages():
    """Chapter number -> the files myst.yml lists under that chapter's toc entry, in order."""
    pages, chapter, indent = {}, None, None
    for line in (BOOK / "myst.yml").read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        depth = len(line) - len(line.lstrip())
        m = re.match(r'\s*- title:\s*"?Chapter (\d+):', line)
        if m:
            chapter, indent = int(m.group(1)), depth
            pages[chapter] = []
            continue
        if chapter is not None and depth <= indent:
            chapter = None
        m = re.match(r"\s*- file:\s*(\S+)", line)
        if chapter is not None and m:
            pages[chapter].append(m.group(1))
    return pages


def files(chapters):
    out = {}
    in_toc = toc_pages()
    out[BOOK / "scripts" / "standards.json"] = json.dumps({"chapters": chapters}, indent=2, ensure_ascii=False) + "\n"
    # MyST resolves a link in an included file from the page that includes it, so the links
    # of the chapter list are written relative to notes/index.md, not to notes/_parts/.
    lines = []
    for c in chapters:
        lines.append(f"**{c['title']}**")
        lines.append("")
        for s in c["standards"]:
            if (BOOK / s["page"]).exists():
                lines.append(f"- [{s['id']} {s['name']}](chapter-{c['number']}/{s['slug']}.md)")
            else:
                lines.append(f"- {s['id']} {s['name']}")
        standard_pages = {s["page"] for s in c["standards"]}
        for page in in_toc.get(c["number"], []):
            if page not in standard_pages and (BOOK / page).exists():
                lines.append(f"- [{page_title(page)}]({page.removeprefix('notes/')})")
        lines.append("")
        for s in c["standards"]:
            box = (f":::{{admonition}} Standard {s['id']}: {s['name']}\n:class: standard\n"
                   f"{s['statement']}\n:::\n")
            out[BOOK / "notes" / "_parts" / "standards" / f"{s['id']}.md"] = box
    out[BOOK / "notes" / "_parts" / "chapters.md"] = "\n".join(lines).rstrip() + "\n"
    return out


def toc(chapters):
    lines = ["  toc:", "    - file: notes/index.md"]
    for c in chapters:
        lines.append(f'    - title: "{c["title"]}"')
        lines.append("      children:")
        for s in c["standards"]:
            lines.append(f"        - file: {s['page']}")
    lines += ["    - file: notes/glossary.md", "    - file: notes/accessibility.md"]
    return "\n".join(lines)


def sources():
    """Print, for each standard, the lectures that feed it (standards.py) and their decks."""
    decks = COURSE / "Lectures_Spring2027"
    used = set()
    for s in S.STANDARDS:
        if s[1] not in "12345":
            continue
        part = s[5].split(";")[0].strip()
        numbers = []
        m = re.match(r"Lectures? (.+)$", part)
        if m:
            for piece in re.split(r",| and ", m.group(1)):
                a, _, b = piece.strip().partition("-")
                numbers += list(range(int(a), int(b or a) + 1))
        print(f"{s[0]} {S.short_name(s[0])}: {part if numbers else 'no lecture listed in standards.py'}")
        for n in numbers:
            used.add(n)
            for deck in sorted((decks / f"Lecture_{n:02d}").glob("*.pptx")):
                print(f"    {deck.relative_to(COURSE)}")
    rest = [d for d in sorted(decks.glob("Lecture_*/*.pptx"))
            if not (re.fullmatch(r"Lecture_(\d+)", d.parent.name) and int(d.parent.name[8:]) in used)]
    print("Decks that no standard lists:")
    for deck in rest:
        print(f"    {deck.relative_to(COURSE)}")


def check_myst(chapters):
    """Chapter titles and standard pages named in myst.yml must match the source."""
    text = (BOOK / "myst.yml").read_text(encoding="utf-8")
    errors = []
    wanted = {c["title"] for c in chapters}
    for title in re.findall(r'title:\s*"?(Chapter \d+: [^"\n]+)"?', text):
        if title.strip() not in wanted:
            errors.append(f'myst.yml: chapter title "{title.strip()}" is not in standards.py')
    pages = {s["page"] for c in chapters for s in c["standards"]}
    for page in re.findall(r"file:\s*(notes/chapter-\d/[\w-]+\.md)", text):
        if not (BOOK / page).exists():
            errors.append(f"myst.yml: {page} does not exist")
        elif page in pages:
            sid = next(s["id"] for c in chapters for s in c["standards"] if s["page"] == page)
            if f"_parts/standards/{sid}.md" not in (BOOK / page).read_text(encoding="utf-8"):
                errors.append(f"{page}: the box of Standard {sid} is not included")
    return errors


if __name__ == "__main__":
    if "--sources" in sys.argv:
        sources()
        sys.exit(0)
    chapters = collect()
    wanted = files(chapters)
    if "--check" in sys.argv:
        stale = [str(p.relative_to(BOOK)) for p, text in wanted.items()
                 if not p.exists() or p.read_text(encoding="utf-8") != text]
        errors = [f"{p} is out of date: run scripts/make_standards.py" for p in stale] + check_myst(chapters)
        for e in errors:
            print("ERROR:", e)
        print(f"standards: {sum(len(c['standards']) for c in chapters)} in {len(chapters)} chapters, "
              f"{'ok' if not errors else str(len(errors)) + ' problems'}")
        sys.exit(1 if errors else 0)
    for path, text in wanted.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(wanted)} files for {sum(len(c['standards']) for c in chapters)} standards in {len(chapters)} chapters")
    for e in check_myst(chapters):
        print("ERROR:", e)
    if "--toc" in sys.argv:
        print(toc(chapters))
