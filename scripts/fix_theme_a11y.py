"""Post-build accessibility fixes for the MyST book theme.

Run after `jupyter-book build --html`:  python3 scripts/fix_theme_a11y.py _build/html

The theme gives two kinds of links an aria-label that differs from their
visible text, which fails WCAG 2.1 success criterion 2.5.3 (Label in Name):

1. Figure, table, definition and exercise number links in captions
   ("Figure 1:") are labelled "Link to this figure" and so on. The label is kept only for the pilcrow anchors next
   to headings, whose visible text is a symbol.
2. Previous and next page links in the footer are labelled "Next: <title>".
   Without the label, their name is their visible text.

It also restores the row headers of tables written in HTML (WCAG 1.3.1): MyST
drops scope="row" from <th>, so every <th> in a row that also holds a <td> gets
scope="row" again.

Both the server-rendered HTML and the JavaScript bundle are patched, so the
pages stay correct after client-side navigation.

Last, the search index (myst.search.json) loses the hidden words that a subscript
carries for screen readers ("NACA 64, subscript,3-618" becomes "NACA 64₃-618"), so
search results show the text as it reads on the page. The script stops with an
error if the theme code has changed and a patch no longer applies.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "_build/html")
# The quiz and quick-check widgets, read from the book folder (this script's parent's
# parent), so the script works from any working directory.
QUICKCHECK = Path(__file__).resolve().parent.parent / "quickcheck"

# Regular expressions, not literal strings: the minifier renames variables and
# switches between "..." and `...` quotes from one theme release to the next.
# The bundle sits in build/ (themes before November 2026) or _assets/ (after).
JS_PATCHES = [
    ("caption link label",
     re.compile(r'title:(\w+),"aria-label":\1,children:(\w+)\}\)'),
     r'title:\1,"aria-label":\2==="\\xB6"?\1:void 0,children:\2})'),
    ("footer link label",
     re.compile(r'"aria-label":`\$\{\w+\?["`]Previous: ["`]:["`]Next: ["`]\}\$\{\w+\}`,'),
     ""),
    # Row headers (WCAG 1.3.1). A table written in HTML marks its row headers
    # <th scope="row">, but MyST keeps only "header" on a cell and drops the scope.
    # A header cell in a row that also holds data cells gets scope="row" again:
    # the row passes it to its cells, and the cell writes it on the <th>.
    ("row header scope, row",
     re.compile(r'(tableRow\(\{node:(\w+),className:\w+\}\)\{return[^}]*?'
                r'children:\(0,[\w$]+\.jsx\)\([\w$]+,\{ast:)\2\.children\}'),
     r'\1\2.children.some(c=>!c.header)?\2.children.map(c=>c.header&&!c.scope?'
     r'{...c,scope:"row"}:c):\2.children}'),
    ("row header scope, cell",
     re.compile(r'((\w+)\.header\?\(0,[\w$]+\.jsx\)\(`th`,Object\.assign\(\{)'),
     r'\1scope:\2.scope,'),
]

applied = {name: 0 for name, _, _ in JS_PATCHES}
for js in [*root.glob("build/**/*.js"), *root.glob("_assets/**/*.js")]:
    text = js.read_text(encoding="utf-8")
    new = text
    for name, pattern, rep in JS_PATCHES:
        new, n = pattern.subn(rep, new)
        applied[name] += n
    if new != text:
        js.write_text(new, encoding="utf-8")

missing = [name for name, n in applied.items() if n == 0]
if missing:
    sys.exit("Theme code changed; patch not applied: " + "; ".join(missing))

caption_label = re.compile(
    r'(<a [^>]*title="Link to this [A-Za-z ]+") aria-label="Link to this [A-Za-z ]+"(>(?!¶))')
footer_label = re.compile(r' aria-label="(?:Next|Previous): [^"]*"')
# The {iframe} directive writes no title attribute (WCAG 4.1.2). Quick-check
# widgets get the <title> of their own HTML file; anything else a plain name.
iframe_tag = re.compile(r'<iframe(?![^>]*\btitle=)([^>]*\bsrc="([^"]*?)([^"/]+)\.html"[^>]*)>')
title_tag = re.compile(r"<title>(.*?)</title>", re.S)
# The same row-header rule for the server-rendered pages: a <th> without a scope
# in a row that also holds a <td>.
table_row = re.compile(r"<tr\b[^>]*>.*?</tr>", re.S)
bare_th = re.compile(r"<th\b(?![^>]*\bscope=)")


def row_scope(m):
    row = m.group(0)
    return bare_th.sub('<th scope="row"', row) if "<td" in row else row


def iframe_title(m):
    folder, name = m.group(2), m.group(3)
    title = "Embedded content"
    if "quickcheck/" in folder:
        src = QUICKCHECK / f"{name}.html"
        if not src.exists():
            sys.exit(f"fix_theme_a11y: {src} is missing; an iframe on a page points to it")
        found = title_tag.search(src.read_text(encoding="utf-8"))
        if found:
            title = found.group(1).strip()
    return f'<iframe title="{title}"{m.group(1)}>'


pages = 0
for html in root.glob("**/*.html"):
    text = html.read_text(encoding="utf-8")
    new = caption_label.sub(r"\1\2", text)
    new = footer_label.sub("", new)
    new = iframe_tag.sub(iframe_title, new)
    new = table_row.sub(row_scope, new)
    if new != text:
        html.write_text(new, encoding="utf-8")
        pages += 1

# The site search is built from the text of each page, hidden text included, so a subscript
# that carries a hidden word for screen readers (NACA 64<span class="sr-only">, subscript,</span>
# <sub>3</sub>-618) shows in the search results as "NACA 64\n\n, subscript,3-618". Every string
# of the search index gets the subscript back as one character ("NACA 64₃-618"), whatever
# spaces and line breaks the index puts around the hidden words.
hidden_sub = re.compile(r"(\d)\s*,\s*subscript\s*,\s*(\d+)")
SUB_DIGITS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def search_text(value):
    global searched
    if isinstance(value, str):
        new, n = hidden_sub.subn(lambda m: m.group(1) + m.group(2).translate(SUB_DIGITS), value)
        searched += n
        return new
    if isinstance(value, list):
        return [search_text(v) for v in value]
    if isinstance(value, dict):
        return {k: search_text(v) for k, v in value.items()}
    return value


searched = 0
for index in root.glob("**/myst.search.json"):
    data = json.loads(index.read_text(encoding="utf-8"))
    new = search_text(data)
    if new != data:
        index.write_text(json.dumps(new, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    if re.search(r"\d(?:\s|\\n)*,\s*subscript\s*,", json.dumps(new, ensure_ascii=False)):
        sys.exit(f"fix_theme_a11y: hidden subscript text is still in {index}")

print(f"Patched the theme bundle ({sum(applied.values())} changes), {pages} HTML pages, "
      f"and {searched} hidden subscripts in the search index.")
