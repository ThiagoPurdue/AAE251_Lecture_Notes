# AAE251 Lecture Notes

Lecture notes for AAE 25100 Introduction to Aerospace Design, Purdue University, built with
[Jupyter Book 2](https://jupyterbook.org) (MyST). The book has five chapters, one for each
group of course standards, and one page per standard. A chapter may also have a page on
material that no standard assesses. The book carries no dates and no assignments.

Status: Chapter 1, Systems Engineering and Fundamental Thoughts (seven pages, 63 figures,
six quizzes), Chapter 2, Introduction to Orbits (five pages, 37 figures, four quizzes),
Chapter 3, Aerodynamics (four pages, 29 figures and a photograph, three quizzes),
Chapter 4, Rocket Design (five pages, four of them for a standard and one on engines and
tanks, 35 figures and two photographs, four quizzes), and Chapter 5, Aircraft Performance
and Propulsion (five pages, 25 figures, four quizzes), are written and published. The site is published at
https://thiagopurdue.github.io/AAE251_Lecture_Notes/.

## Layout

| Path | Contents |
|---|---|
| `myst.yml` | Book configuration and table of contents |
| `notes/index.md`, `glossary.md`, `accessibility.md` | The About page, the glossary and the accessibility statement |
| `notes/chapter-N/` | One folder per chapter (N = 1 to 5): one page per standard and a `figures/` folder |
| `notes/_parts/standards/<id>.md` | The box that states a standard at the top of its page. Written by `make_standards.py`; do not edit |
| `notes/_parts/chapters.md` | The list of chapters and standards on the About page, with any other page `myst.yml` places in a chapter (a page no standard assesses) after its standards. Written by `make_standards.py`; do not edit |
| `notes/_static/site.css`, `logo.svg`, `favicon.ico` | The site style and marks |
| `quickcheck/` | Self-contained HTML widgets shown in a page: the quizzes (`quiz-<id>.html`) and the quick checks |
| `scripts/make_standards.py` | Reads `../_syllabus_build/standards.py` and writes the standard boxes, the chapter list (which also lists a chapter's other pages from `myst.yml`) and `scripts/standards.json` |
| `scripts/make_figures.py` | Shared figure helpers. Each chapter has its own `make_chapter_N_figures.py` |
| `scripts/figkit.py` | The figure kit every chapter shares: Arial math, number formatting, the text, arrow and dimension helpers, the layout check that every figure must pass, `save_figure` and the record of printed values (one `Chapter` object per chapter) |
| `scripts/render_svg.py` | Renders figure SVGs to PNG through headless Chrome, as a browser shows them (`--gray` adds a grayscale copy) |
| `scripts/chapter_N/` | The figure and value code of a chapter: shared modules (constants, formulas, drawing helpers on top of `figkit.py`) and one module per page. Every number printed on a page is computed here and recorded in `values.json`. See the `README.md` in each `scripts/chapter_N/` |
| `scripts/check_values.py`, `scripts/check_chains.py` | Stop when a recorded value is missing from its page, or when a printed calculation step does not reproduce from the digits printed before it |
| `scripts/make_quizzes.py`, `scripts/quizzes/<id>.json` | The quiz of each standard, built from question data |
| `scripts/check_pages.py` | Stops on a date, an assignment, a dash, a figure with no alt text or a figure or table with no caption |
| `scripts/check_links.py` | Stops when an internal link of the built site opens nothing (a page link MyST could not resolve stays a `.md` path) |
| `scripts/fix_theme_a11y.py` | Post-build fix for two theme labeling issues (WCAG 2.5.3) and the iframe titles of the quizzes (read from `quickcheck/`, whatever the working directory) |
| `scripts/check_accessibility.mjs` | Runs the axe accessibility engine on the built site, in light and dark mode, at 1280 px and at 320 px (where a page that scrolls sideways also fails), and inside every quiz iframe in four states (question, a wrong answer, a right answer, score) |
| `.github/workflows/deploy.yml` | Checks, builds and publishes the site to GitHub Pages on every push to `main` |

## Chapters

The chapter titles, the page of each standard and the text of each standard come from
`_syllabus_build/standards.py` in the course folder. After any change there:

```bash
python3 scripts/make_standards.py            # rewrite the boxes, the chapter list and standards.json
python3 scripts/make_standards.py --toc      # also print the full toc block for myst.yml
python3 scripts/make_standards.py --sources  # the lecture decks behind each page
python3 scripts/make_standards.py --check    # stop if anything is out of date
```

## Build and check

This folder is synced by OneDrive, which truncates files that are being written. Never build
here. The script of the `make-notes` skill copies the book to a scratch folder, checks the
pages, the numbers and the quizzes, builds, patches the theme and runs the accessibility
check:

```bash
.claude/skills/make-notes/scripts/build_check.sh AAE251_Lecture_Notes <scratch> [<screenshot folder>]
```

It needs Python 3, Node and Google Chrome. The first run installs `jupyter-book==2.1.7`,
`axe-core` and `puppeteer-core` in the scratch folder.

To redraw the figures of a chapter and recompute its numbers (needs `matplotlib` and
`numpy`; run it in a scratch copy, then copy the figures and `values.json` back):

```bash
python3 -B scripts/make_chapter_1_figures.py     # all figures of a chapter, strict layout check, values.json
python3 -B scripts/make_chapter_2_figures.py
python3 -B scripts/make_chapter_3_figures.py
python3 -B scripts/make_chapter_4_figures.py
python3 -B scripts/make_chapter_5_figures.py
python3 -B scripts/check_values.py --strict      # values on their pages, calculation steps
python3 -B scripts/make_quizzes.py               # rebuild the quizzes from scripts/quizzes/
```

## Add a page

Follow the project skill `make-notes` (`.claude/skills/make-notes/SKILL.md`). In short: write
`notes/chapter-N/<page>.md` with the standard box at the top, its figures in
`notes/chapter-N/figures/` and its quiz in `scripts/quizzes/<id>.json`; add the page to the
`toc` in `myst.yml`; run `make_standards.py` so the About page links to it; build and check.

## Publishing

The site is https://thiagopurdue.github.io/AAE251_Lecture_Notes/, built from the GitHub
repository `ThiagoPurdue/AAE251_Lecture_Notes`. GitHub Pages deploys from GitHub Actions on
every push to `main`. On the instructor's computer the git directory is kept outside
OneDrive (`~/GitRepos/AAE251_Lecture_Notes.git`, attached with
`git init --separate-git-dir`). The workflow does not
publish the site when a page breaks a rule of `check_pages.py`, a number fails
`check_values.py`, a quiz is out of date, an internal link is broken, or the accessibility check finds a WCAG 2.1 A or AA
violation.

The site is public. Nothing from the problem bank, the Standards Checks, the homework
solutions or the project solutions may ever be copied into this folder.
