// Accessibility check for the built book (WCAG 2.1 A and AA rules of axe-core).
//
// Usage, from a folder where axe-core and puppeteer-core are installed:
//   npm i axe-core puppeteer-core
//   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
//     node /path/to/scripts/check_accessibility.mjs /path/to/_build/html [screenshot_dir]
//
// Every page is checked in light mode and in dark mode, at two widths:
//   - 1280 px, a desktop screen;
//   - 320 px, a phone, which is also what a 1280 px screen shows at 400% zoom
//     (WCAG 1.4.10 Reflow). At this width the page must not scroll sideways:
//     a page wider than the window counts as a violation.
// Every same-origin iframe of a page (the quizzes, quickcheck/*.html) is checked
// with axe inside the frame, in four states: a question shown; question 1
// answered wrongly (the wrong-answer colors, "your answer" and the verdict
// "Not correct." with the explanation); question 2 answered rightly (the
// right-answer colors and "Correct."); and the score screen with its review
// links. The quiz is driven by clicking its own controls, so both answered
// states are reached on every run.
//
// The script exits with status 1 if axe reports any violation or a page
// scrolls sideways at 320 px, and 0 otherwise. With a screenshot folder, it
// also saves a full-page PNG of each page in each mode for a visual check:
// <page>-light.png and <page>-dark.png at 1280 px, <page>-light-320.png and
// <page>-dark-320.png at 320 px.
import { createRequire } from "node:module";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const require = createRequire(path.join(process.cwd(), "noop.js"));
const puppeteer = require("puppeteer-core");
const axeSource = fs.readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const root = path.resolve(process.argv[2] || "_build/html");
const shots = process.argv[3];
const chrome = process.env.CHROME ||
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css",
  ".json": "application/json", ".svg": "image/svg+xml", ".png": "image/png",
  ".jpg": "image/jpeg", ".ico": "image/x-icon", ".woff2": "font/woff2" };

// On GitHub Pages the site is built with BASE_URL=/<repository>; strip it here.
const baseUrl = (process.env.BASE_URL || "").replace(/\/$/, "");
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (baseUrl && p.startsWith(baseUrl)) p = p.slice(baseUrl.length) || "/";
  let f = path.join(root, p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, "index.html");
  if (!fs.existsSync(f)) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "Content-Type": types[path.extname(f)] || "application/octet-stream" });
  fs.createReadStream(f).pipe(res);
});
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;

const pages = fs.readdirSync(root)
  .filter((d) => fs.existsSync(path.join(root, d, "index.html")))
  .map((d) => `/${d}/`);
pages.unshift("/");

const WIDTHS = [{ width: 1280, height: 900 }, { width: 320, height: 640 }];
const RULES = { runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"] } };

// Run axe in one document (the page or a frame) and print its result.
async function audit(target, label, opts) {
  if (!(await target.evaluate(() => typeof window.axe !== "undefined"))) await target.evaluate(axeSource);
  const result = await target.evaluate(async (o) => await window.axe.run(document, o), opts);
  const n = result.violations.reduce((s, v) => s + v.nodes.length, 0);
  console.log(`${label} violations: ${n}` +
    `  (passed rules: ${result.passes.length}, needs review: ${result.incomplete.length})`);
  for (const v of result.violations) {
    console.log(`   - ${v.id} [${v.impact}] ${v.help}`);
    for (const node of v.nodes.slice(0, 5)) console.log(`       ${node.target.join(" ")}`);
  }
  return n;
}

// Drive a quiz frame one step: answer the question shown, with a wrong option
// (right = false) or the right one (option 0 of the data, right = true), or move
// on after the verdict. Returns the state reached.
const step = (frame, right) => frame.evaluate((right) => {
  const result = document.getElementById("result");
  if (result && !result.hidden) return "score";
  const pick = document.querySelector(`input[name=answer]${right ? '[value="0"]' : ':not([value="0"])'}:not(:disabled)`);
  if (pick) pick.click();
  const go = document.getElementById("go");
  if (!go) return "none";
  go.click();
  if (result && !result.hidden) return "score";
  return document.querySelector("input[name=answer]:disabled") ? "answered" : "question";
}, right);

// Chrome can take more than the default 30 s to start on a busy GitHub runner.
const browser = await puppeteer.launch({ executablePath: chrome, headless: true,
  args: ["--no-sandbox"], timeout: 120000 });
let total = 0;
for (const scheme of ["light", "dark"]) {
  for (const size of WIDTHS) {
    const tag = size.width === 1280 ? "" : ` @${size.width}px`;
    for (const p of pages) {
      const page = await browser.newPage();
      await page.setViewport(size);
      await page.emulateMediaFeatures([{ name: "prefers-color-scheme", value: scheme }]);
      await page.goto(base + baseUrl + p, { waitUntil: "load", timeout: 120000 });
      await new Promise((r) => setTimeout(r, 1500));   // let the page hydrate; the site is static
      const label = `${scheme.padEnd(5)} ${(p + tag).padEnd(30)}`;
      // The page itself; its frames are checked on their own below, in each state.
      total += await audit(page, label, { ...RULES, iframes: false });
      if (size.width < 1280) {
        const wide = await page.evaluate(() => document.documentElement.scrollWidth);
        if (wide > size.width) {
          total += 1;
          console.log(`   - reflow: the page is ${wide} px wide in a ${size.width} px window (scrolls sideways)`);
        }
      }
      for (const frame of page.frames()) {
        if (frame === page.mainFrame() || !frame.url().startsWith(base)) continue;
        const name = path.basename(new URL(frame.url()).pathname);
        const flabel = `${scheme.padEnd(5)}   ${name} in ${p}${tag}`;
        total += await audit(frame, `${flabel}, question`.padEnd(36), RULES);
        let state = await step(frame, false);                       // question 1, wrong
        const shows = (sel) => frame.evaluate((sel) => !!document.querySelector(sel), sel);
        if (state === "answered" && await shows(".verdict.bad")) total += await audit(frame, `${flabel}, answered (wrong)`.padEnd(36), RULES);
        else { total += 1; console.log(`   - ${name}: question 1 could not be answered`); }
        state = await step(frame, true);                            // on to question 2
        state = await step(frame, true);                            // question 2, right
        if (state === "answered" && await shows(".verdict.ok")) total += await audit(frame, `${flabel}, answered (right)`.padEnd(36), RULES);
        else { total += 1; console.log(`   - ${name}: question 2 could not be answered`); }
        for (let k = 0; k < 60 && state !== "score" && state !== "none"; k++) state = await step(frame, k % 4 === 0);
        if (state === "score") total += await audit(frame, `${flabel}, score`.padEnd(36), RULES);
        else { total += 1; console.log(`   - ${name}: could not reach the score screen`); }
      }
      if (shots) {
        fs.mkdirSync(shots, { recursive: true });
        const name = (p === "/" ? "index" : p.replaceAll("/", "")) + `-${scheme}` +
          (size.width === 1280 ? "" : `-${size.width}`) + ".png";
        await page.reload({ waitUntil: "load" });           // the quiz back at its first question
        await new Promise((r) => setTimeout(r, 1000));
        await page.screenshot({ path: path.join(shots, name), fullPage: true });
      }
      await page.close();
    }
  }
}
await browser.close();
server.close();
console.log(total === 0 ? "No WCAG 2.1 A/AA violations found." : `${total} violations found.`);
process.exit(total === 0 ? 0 : 1);
