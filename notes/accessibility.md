---
title: Accessibility
---

These notes are written to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at Level AA, the standard adopted under Title II of the Americans with Disabilities Act for the web content of public universities.

## What the site does

- Every figure has alt text that describes what it shows, and a visible caption. The words inside a figure are part of the picture, so the alt text and the caption repeat what the figure says.
- Equations are written in MathML, so screen readers can read them. Powers of ten, degree values, and word subscripts are marked up so that each is read as one item. In running text, a subscript such as the 3 in the airfoil name NACA 64<span class="sr-only">, subscript,</span><sub>3</sub>-618 carries a hidden word "subscript" for screen readers.
- Tables are HTML tables with header rows and captions. Every column header names its column in words, with the symbol beside it where there is one. Seven tables that compare items across and down also have row headers: four in Chapter 1 (the ratings of the needs, hazards against project risks, the blocked-instrument readings, and the decision matrix), two in Chapter 3 (open- and closed-circuit wind tunnels compared, and wind tunnels by Mach number), and one in Chapter 5 (air-breathing propulsion families compared).
- Color is never the only way information is given. Lines in a plot also differ by line style or marker, and each curve is labeled or named in the caption and the alt text.
- Text meets a contrast ratio of at least 4.5:1 against its background. Lines and marks in figures that carry information meet at least 3:1 against white. A light fill that marks a region of a figure is never the only cue: the region is also outlined, patterned, or named.
- Pages use headings in order, so a screen reader can move through them by section.
- The site and its quizzes can be used with a keyboard alone. In a quiz, the arrow keys choose an answer and Enter checks it; the verdict and the explanation are placed in a live region, which screen readers read out. On the score screen, each link opens the section it names.
- The site follows the reader's light or dark mode setting. Text can be enlarged to 400%, and pages can be read on a screen 320 pixels wide, without scrolling sideways; wide tables and equations scroll inside their own box. On a small screen, figures take the full width of the text.

## How the site is checked

- Before it is published, every page is checked with the axe accessibility engine against the WCAG 2.1 A and AA rules, in light and dark mode, at a desktop width and at 320 pixels. At 320 pixels the check also fails a page that scrolls sideways. Each quiz is checked inside its page in four states: a question, a wrong answer with its explanation, a right answer with its explanation, and the score screen.
- By hand: every alt text was read beside its figure; the quizzes were worked through with the keyboard alone; pages were checked for reading order as a screen reader presents them; and the contrast of every color in the drawn figures was computed. The pages were looked at in screenshots at a desktop width and at 320 pixels, in light and dark mode, and measured at 200% zoom for sideways scrolling and for equations cut off at the edge.

## Known limitations

- Figures are drawings of a fixed shape, except one photograph on page 3.2. The labels of a drawing are part of the picture, so on a phone they are smaller than the text even when the figure fills the width of the screen. Zoom in on the figure, or use its alt text and caption.
- In the quizzes, symbols and short formulas are written as text (for example v∞), not as MathML. A superscript carries a hidden "to the power" for screen readers, so a quiz power of ten such as 10⁵ is read as "10 to the power 5".
- The notes have not yet been tested with screen readers by people who use them. The checks above rest on the automated engine and on the structure of the pages.
- Videos linked from a page, where there are any, are hosted by their publishers, who provide the captions.
- Linked external documents and sites are outside the control of this site.

## Report a barrier

If any part of these notes is hard to use with your browser, screen reader, or other assistive technology, contact the instructor, Prof. Thiago Guimarães, School of Aeronautics and Astronautics, Purdue University; his Purdue email address is listed in the [Purdue directory](https://www.purdue.edu/directory/). Students in the course can also write through Brightspace. Name the page and describe the problem. You will get the content in a form you can use. Purdue students can also request accommodations through the Purdue Disability Resource Center.
