"""Check every internal link of the built site.

    python3 scripts/check_links.py _build/html

Reads each built page and tests every link that points inside the site: the target page or
file must exist in the build, and a link must not still end in ".md" (a page link that MyST
could not resolve is left as the source path and opens nothing). Links to other sites are
not followed. The site may be built for a base URL (BASE_URL=/name); the base is read from
the pages themselves. Exit status 1 when a link is broken.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        elif tag in ("img", "iframe", "script") and a.get("src"):
            self.links.append(a["src"])
        elif tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon"):
            self.links.append(a["href"])


def main():
    root = Path(sys.argv[1]).resolve()
    pages = sorted(root.glob("index.html")) + sorted(root.glob("*/index.html"))
    if not pages:
        sys.exit(f"check_links: no pages in {root}")
    # The base URL is the common prefix of the site's own stylesheet link.
    first = pages[0].read_text(encoding="utf-8")
    m = re.search(r'href="([^"]*)/myst-theme\.css', first)
    base = m.group(1) if m else ""
    broken, tested = [], 0
    for page in pages:
        here = "/" + page.parent.relative_to(root).as_posix().strip(".")
        here = here.rstrip("/") + "/"
        parser = Links()
        parser.feed(page.read_text(encoding="utf-8"))
        for href in parser.links:
            parts = urlsplit(href)
            if parts.scheme or parts.netloc or href.startswith(("#", "mailto:", "data:")):
                continue
            path = unquote(parts.path)
            if not path:
                continue
            if path.startswith("/"):
                if base and not (path == base or path.startswith(base + "/")):
                    broken.append((here, href, "outside the site's base URL"))
                    continue
                rel = path[len(base):].lstrip("/")
            else:
                rel = (Path(here.lstrip("/")) / path).as_posix()
            tested += 1
            parts_rel = []
            for piece in rel.split("/"):
                if piece == "..":
                    if parts_rel:
                        parts_rel.pop()
                elif piece not in ("", "."):
                    parts_rel.append(piece)
            target = root.joinpath(*parts_rel)
            if path.endswith(".md"):
                broken.append((here, href, "unresolved page link (still a .md path)"))
            elif not (target.is_file() or (target / "index.html").is_file()):
                broken.append((here, href, "target not in the build"))
    for here, href, why in broken:
        print(f"BROKEN  {here}  ->  {href}   ({why})")
    print(f"links: {tested} internal links on {len(pages)} pages, "
          + ("ok" if not broken else f"{len(broken)} broken"))
    sys.exit(1 if broken else 0)


if __name__ == "__main__":
    main()
