#!/usr/bin/env python3
"""Check that every printed calculation on a page follows from the digits printed before it.

A worked step such as "$v_\\infty = 29.783 - 22.249 = 7.534$ km/s" must give its printed
result when a student redoes it with the printed operands. The script finds, on every page
of every chapter whose code has a values.json (notes/chapter-N/ for each
scripts/chapter_N/values.json; text, tables, captions and display math alike):

  - in a math span, a run "A = B" where A is an expression of printed numbers only
    (+, -, \\times, /, \\frac, \\sqrt, powers, parentheses, \\pi, \\exp, sin, cos and tan of
    degrees) and B is a single number: A, evaluated, must round to B at B's last digit;
  - a math span of printed numbers only followed in the text by "= number" (as in
    "$\\sqrt{56.76 + 121.5}$ = 13.35 km/s"): the same test.

Run from the book folder (check_values.py also runs it):

    python3 -B scripts/check_chains.py           all pages; status 1 on any miss
    python3 -B scripts/check_chains.py -v        also list every calculation checked

Each miss is printed as "page: expression = printed (computed value)". A printed result may
differ from the computed value by at most half a unit of its last printed digit.
"""
import math
import re
import sys
from pathlib import Path

BOOK = Path(__file__).resolve().parent.parent
# a printed result may be followed by its unit: these are stripped before the number is read
UNITS = (r"km|m|s|days?|kg|km/s|m/s|hours?|minutes?|AU"                      # Chapter 2
         r"|K|Pa|kPa|N|J|ft|ft/s|lb|nmi|mi|kt|knots?|h|hr|min|mm|cm|m/s²|m²|m³|kg/m³|kg/s|m³/s"
         r"|N/m²|lb/ft²|J/\(kg K\)|1/h|%")


def chapter_folders():
    """notes/chapter-N of every chapter whose code has a values.json, in order."""
    return [BOOK / "notes" / f"chapter-{vf.parent.name.split('_', 1)[1]}"
            for vf in sorted((BOOK / "scripts").glob("chapter_*/values.json"))]
MATH = re.compile(r"(:::\{math\}\n(?::[^\n]*\n)*(?P<blk>.*?)\n:::)|\$\$(?P<disp>.*?)\$\$|(?<!\$)\$(?P<inl>[^$\n]+?)\$(?!\$)", re.S)
NUMBER = re.compile(r"^-?\d+(?:\.\d+)?$")


def plain(tex):
    """LaTeX of numbers and operators -> a Python expression, or None if it holds a symbol."""
    s = tex
    s = re.sub(r"\\text\{([\d,.]+)\}", r"\1", s)                       # \text{6,778}
    s = s.replace("{,}", "").replace("{}", " ")                         # {} - 0.047 on a continued line
    s = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", s)                          # 6,778 -> 6778
    s = re.sub(r"\\(?:,|;|:|!|quad|qquad)", " ", s)
    s = re.sub(r"\\ ", " ", s)
    s = re.sub(r"\\text\{\s*[A-Za-z][^}]*\}", " ", s)                   # units: \text{km/s}
    s = re.sub(r"\\(?:left|right|big|Big|bigl|bigr)", "", s)
    s = s.replace("\\times", "*").replace("\\cdot", "*").replace("−", "-")
    s = s.replace("^\\circ", "").replace("°", "").replace("\\%", "")
    s = s.replace("\\pi", "(pi)")
    s = re.sub(r"\\(sin|cos|tan|exp)\b", r" \1", s)
    for _ in range(4):                                                  # \frac{a}{b}, \sqrt{x}
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"**(\1)", s)
        s = re.sub(r"(?<!\\frac)(?<!\\sqrt)(?<!\})\{([^{}]*)\}", r"(\1)", s)
    s = re.sub(r"\^(\d)", r"**\1", s)
    s = s.replace("[", "(").replace("]", ")")
    if re.search(r"\\|[A-Za-z_]", re.sub(r"\b(sqrt|pi|sin|cos|tan|exp)\b", "", s)):
        return None
    if not re.search(r"\d", s) or not re.search(r"[-+*/(]|sqrt|sin|cos|tan|exp", s.strip().lstrip("-")):
        return None
    # implicit multiplication: 2(7.669), )(, 2 pi, ) sqrt
    s = re.sub(r"(\d|\))\s*(?=\(|sqrt|pi|sin|cos|tan|exp)", r"\1*", s)
    s = re.sub(r"\)\s*(?=\d)", ")*", s)
    # trig of degrees: "cos 40" or "cos(40)"
    s = re.sub(r"\b(sin|cos|tan)\s*\(", r"\1d(", s)
    s = re.sub(r"\b(sin|cos|tan)\s+(\d+(?:\.\d+)?)", r"\1d(\2)", s)
    return s


ENV = {"sqrt": math.sqrt, "pi": math.pi, "exp": math.exp,
       "sind": lambda x: math.sin(math.radians(x)), "cosd": lambda x: math.cos(math.radians(x)),
       "tand": lambda x: math.tan(math.radians(x)), "__builtins__": {}}


def evaluate(expr):
    try:
        return float(eval(" ".join(expr.split()), ENV))
    except Exception:
        return None


def number(tex):
    """A printed single number (with its last-digit unit), or None."""
    s = re.sub(r"\\text\{([\d,.]+)\}", r"\1", tex).replace("{,}", "").replace(",", "")
    s = re.sub(r"\\(?:,|;|:|!|quad|qquad)|\\ ", " ", s)
    s = re.sub(r"\\text\{\s*[A-Za-z][^}]*\}", " ", s)
    s = s.replace("^\\circ", "").replace("°", "").replace("−", "-").replace("{", "").replace("}", "")
    s = re.sub(rf"\s+(?:{UNITS})\.?$", "", s.strip()).strip().rstrip(".,")
    if not NUMBER.match(s):
        return None
    d = len(s.split(".")[1]) if "." in s else 0
    return float(s), 10.0 ** (-d)


def split_top(tex, sep="="):
    out, depth, cur = [], 0, ""
    for ch in tex:
        if ch in "{([":
            depth += 1
        elif ch in "})]":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    out.append(cur)
    return out


def checks(text):
    """Yield (expression, printed text, computed, ok) for every printed calculation."""
    for m in MATH.finditer(text):
        body = m.group("blk") or m.group("disp") or m.group("inl") or ""
        body = re.sub(r"\\begin\{aligned\}|\\end\{aligned\}|&|\\\\", " ", body)
        for part in re.split(r"\\Longrightarrow|\\qquad|,\s*\\quad|\\quad", body):
            segs = split_top(part)
            for a, b in zip(segs, segs[1:]):
                expr, res = plain(a), number(b)
                if expr is None or res is None:
                    continue
                val = evaluate(expr)
                if val is None:
                    continue
                yield a.strip(), b.strip(), val, abs(val - res[0]) <= 0.5 * res[1] * (1 + 1e-9) + 1e-12
        if m.group("inl"):                                              # "$\sqrt{a + b}$ = c"
            after = re.match(r"\s*=\s*(-?[\d,]+(?:\.\d+)?)", text[m.end():])
            last = split_top(m.group("inl"))[-1]
            expr = plain(last)
            if after and expr is not None:
                res, val = number(after.group(1)), evaluate(expr)
                if res and val is not None:
                    yield last.strip(), after.group(1), val, abs(val - res[0]) <= 0.5 * res[1] * (1 + 1e-9) + 1e-12


def main(argv):
    verbose = "-v" in argv
    misses = total = 0
    for page in sorted(p for folder in chapter_folders() for p in folder.glob("*.md")):
        n = 0
        for expr, res, val, ok in checks(page.read_text(encoding="utf-8")):
            n += 1
            if verbose or not ok:
                print(f"{page.stem}: {'ok  ' if ok else 'MISS'} {expr} = {res} ({val:.6g})")
            misses += not ok
        total += n
        print(f"{page.stem}: {n} calculations")
    print(f"check_chains: {total} calculations checked, {'ok' if not misses else str(misses) + ' do not follow'}")
    return 1 if misses else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
