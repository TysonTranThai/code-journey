/**
 * Author Module 3 (CSS Foundations) — part 2: lessons 7–12 + module.json.
 * Run: node scripts/content-authoring/m3-css-part2.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const DIR =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/css-foundations/lessons";
const MOD =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/css-foundations";

function writeLesson(id, title, description, minutes, difficulty, challenges, mdx) {
  const lessonDir = path.join(DIR, id);
  mkdirSync(lessonDir, { recursive: true });
  writeFileSync(
    path.join(DIR, `${id}.json`),
    JSON.stringify(
      { id, title, description, minutes, difficulty, contentPath: `./${id}.mdx`, challenges },
      null,
      2,
    ) + "\n",
  );
  writeFileSync(path.join(DIR, `${id}.mdx`), mdx.trimStart() + "\n");
  console.log("lesson:", id);
}

function writeChallenge(lessonId, challenge) {
  const dir = path.join(DIR, lessonId, "challenges");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, `${challenge.id}.json`), JSON.stringify(challenge, null, 2) + "\n");
  console.log("  challenge:", challenge.id);
}

/* ── 3.6 Display & Flow ──────────────────────────────────────────────── */

writeLesson(
  "css-display-flow",
  "Display & Flow",
  "Block, inline, and inline-block: the invisible rule that decides whether elements sit beside or stack on top of each other.",
  10,
  "beginner",
  ["display-sorting"],
  `
Why does a \`<p>\` claim its own line while a \`<strong>\` shares one with its neighbors?
The answer is the \`display\` property — the most consequential property in CSS.

## The two defaults

**display: block** — paragraphs, headings, divs, sections. A block box:
- takes the **full width** available by default,
- starts on a **new line**,
- respects all box-model properties (width, height, margin, padding).

**display: inline** — strong, em, a, span, img (mostly). An inline box:
- flows **within the text line**, taking only the space it needs,
- ignores \`width\`/\`height\`,
- accepts horizontal padding/margin; vertical padding paints but does not push lines
  apart (a classic confusion).

\`\`\`html
<p>HTML is <strong>content</strong>, CSS is <em>style</em>.</p>
\`\`\`

Both \`strong\` and \`em\` flow inside the paragraph's line — that is inline.

## The useful hybrid: inline-block

\`\`\`css
.tag {
  display: inline-block;
  padding: 4px 10px;
  width: auto;
}
\`\`\`

\`inline-block\` boxes flow like words *and* accept \`width\`, \`height\`, full padding —
badges, tags, buttons-in-a-row. Flexbox (soon) supersedes most layout uses, but
\`inline-block\` remains the honest answer for "make this little box sit in the flow".

## none — and why it beats visibility hacks

\`\`\`css
.mobile-only {
  display: none;
}
\`\`\`

\`display: none\` removes the box entirely: no space, not rendered, **not read by screen
readers, not focusable**. (Its cousin \`visibility: hidden\` keeps the space but blanks
it — and also hides from assistive tech. Choose deliberately: are you *removing*
content or *blinding* it? For responsive show/hide, \`display: none\` is correct.)

## Changing nature

CSS can reassign display: \`a { display: block; }\` makes a link fill its own line (a
whole-card link in a nav); \`li { display: inline; }\` lines up list items — the old
nav-bar trick. You will see both again.

## What you learned

- Block: full width, own line, full box-model control
- Inline: flows in text, no width/height, partial box-model
- inline-block: flows like text, sizes like a box
- display: none removes fully — a semantic decision, not just visual

**Next:** positioning — when layout systems are not the tool.
`,
);

writeChallenge("css-display-flow", {
  id: "display-sorting",
  title: "Prediction: Block or Inline?",
  prompt:
    "Predict, then prove. The boilerplate has three elements and empty predictions in CSS comments. Replace each prediction comment with the property that makes the statement true:\n\n1. Make the `.badge` keep its padding AND width while flowing beside the text → set `display` on `.badge`.\n2. Make the span-sized `.spacer` disappear entirely → set `display` on `.spacer`.\n3. Keep `.para` as a block — but prove it by setting `display` explicitly on `.para`.",
  difficulty: "beginner",
  boilerplate:
    '<style>\n  .badge {\n    /* display value here */\n    padding: 2px 8px;\n    width: 80px;\n  }\n\n  .spacer {\n    /* display value here */\n  }\n\n  .para {\n    /* display value here */\n  }\n</style>\n\n<p>Score: <span class="badge">99 points</span> and counting.</p>\n<p class="para">Blocks claim their own line.</p>\n',
  tests: [
    {
      name: "badge is inline-block",
      code: `const badge = code.match(/\\.badge\\s*{([^}]*)}/i);
if (!badge || !/display\\s*:\\s*inline-block\\s*;/i.test(badge[1])) {
  throw new Error("Set display: inline-block; on .badge — flows like text, sizes like a box.");
}`,
      hint: "inline keeps width ignored; block breaks the line — the hybrid is inline-block.",
    },
    {
      name: "spacer is none",
      code: `const spacer = code.match(/\\.spacer\\s*{([^}]*)}/i);
if (!spacer || !/display\\s*:\\s*none\\s*;/i.test(spacer[1])) {
  throw new Error("Set display: none; on .spacer — fully removed from rendering.");
}`,
      hint: "display: none removes the box entirely — no space, not rendered.",
    },
    {
      name: "para is explicitly block",
      code: `const para = code.match(/\\.para\\s*{([^}]*)}/i);
if (!para || !/display\\s*:\\s*block\\s*;/i.test(para[1])) {
  throw new Error("Set display: block; on .para explicitly.");
}`,
      hint: "Paragraphs are block by default — here you state it to prove the concept.",
    },
  ],
});

/* ── 3.7 Positioning ─────────────────────────────────────────────────── */

writeLesson(
  "css-positioning",
  "Positioning",
  "Position is the escape hatch, not the layout system: relative, absolute, fixed — and the one pattern you will actually use weekly.",
  10,
  "beginner",
  ["badge-the-card"],
  `
Honest framing first: **layout is the job of Flexbox and Grid** (next lessons).
\`position\` solves a different, smaller problem: *placing a box relative to something*.
Beginners who reach for position first produce brittle pages; here is the right-sized
dose.

## The values

**static** — the default. The box sits in normal flow; offset properties are ignored.

**relative** — the box stays in flow, and \`top\`/\`right\`/\`bottom\`/\`left\` nudge it
*visually* from where it would have been (the original space is preserved):

\`\`\`css
.callout {
  position: relative;
  top: 4px;      /* drawn 4px lower than its flow position */
}
\`\`\`

**absolute** — the box is removed from flow and positioned against its nearest
**positioned ancestor** (one with position other than static). If none exists, the
page itself. This is *the* pattern:

\`\`\`css
.card {
  position: relative;   /* anchor — now a containing block */
}
.card .badge {
  position: absolute;   /* placed against .card */
  top: 8px;
  right: 8px;
}
\`\`\`

The badge floats over the card's top-right corner regardless of the card's size —
because the card is \`relative\`, it is the coordinate system. **Forget the
\`position: relative\` on the parent and the badge positions against the page** — the
most common positioning bug, and now you know its name.

**fixed** — removed from flow, positioned against the *viewport*: stays put while the
page scrolls. Sticky headers and cookie banners use it — and so do the popups everyone
hates. Use sparingly.

**sticky** — a hybrid: flows normally until a scroll threshold, then sticks. Great for
table headers; a bonus, not a requirement today.

## When to reach for position

- Overlay a badge, tooltip, or close button on a component → absolute + relative parent.
- Persistent header/footer chrome → fixed/sticky (with a11y care).
- Anything else — especially multi-column or stacked layouts → Flexbox/Grid, not
  absolute. Absolute-positioned layouts do not reflow and cannot respond to content
  size: the opposite of responsive.

## What you learned

- static default; relative nudges and (crucially) anchors children
- absolute positions against the nearest positioned ancestor — always pair it with a
  relative parent
- fixed pins to the viewport; sticky sticks on scroll
- Position is for overlays; layout belongs to flex/grid

**Next:** Flexbox — the one-dimensional layout system.
`,
);

writeChallenge("css-positioning", {
  id: "badge-the-card",
  title: "Badge the Card",
  prompt:
    "Put a 'NEW' badge over the offer card's top-right corner:\n\n- Give `.card` the position value that makes it an anchor for absolutely-positioned children.\n- Give `.badge` absolute positioning, 8px from the top and right of the card.\n- The badge must be positioned against the CARD — not the page.",
  difficulty: "beginner",
  boilerplate:
    '<style>\n  .card {\n    width: 280px;\n    padding: 24px;\n    border: 1px solid silver;\n    margin: 48px;\n  }\n\n  .badge {\n    padding: 2px 8px;\n    background: gold;\n  }\n</style>\n\n<div class="card">\n  <span class="badge">NEW</span>\n  <h3>Spring offer</h3>\n  <p>Three months half price.</p>\n</div>\n',
  tests: [
    {
      name: "card is the anchor",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card || !/position\\s*:\\s*relative\\s*;/i.test(card[1])) {
  throw new Error("Give .card position: relative; — it becomes the coordinate system for the badge.");
}`,
      hint: "An absolutely-positioned child looks for the nearest positioned ancestor — make the card one.",
    },
    {
      name: "badge is absolute with offsets",
      code: `const badge = code.match(/\\.badge\\s*{([^}]*)}/i);
if (!badge) {
  throw new Error("Keep the .badge rule.");
}
if (!/position\\s*:\\s*absolute\\s*;/i.test(badge[1])) {
  throw new Error("Set .badge to position: absolute;");
}
if (!/top\\s*:\\s*8px\\s*;/i.test(badge[1]) || !/right\\s*:\\s*8px\\s*;/i.test(badge[1])) {
  throw new Error("Offset the badge 8px from top and right.");
}`,
      hint: "top: 8px; right: 8px; measure from the positioned ancestor's edges.",
    },
  ],
});

/* ── 3.8 Flexbox ─────────────────────────────────────────────────────── */

writeLesson(
  "css-flexbox",
  "Flexbox",
  "The one-dimensional layout system: rows and columns that align, space, and wrap — the tool behind nav bars, toolbars, and card rows.",
  16,
  "beginner",
  ["flex-the-navbar", "flex-the-card-row"],
  `
Flexbox answers the question block layout never could: *how do I arrange these boxes
in a line and control the space between them?* Nav bars, toolbars, card rows, centering
— flex is the tool.

## Container and items

\`\`\`css
.nav {
  display: flex;
}
\`\`\`

The element with \`display: flex\` is a **flex container**; its direct children become
**flex items** laid out along a **main axis** (a row by default).

## The core properties

On the container:

\`\`\`css
.container {
  display: flex;
  flex-direction: row;        /* row | column */
  justify-content: space-between; /* along the MAIN axis */
  align-items: center;        /* along the CROSS axis */
  gap: 1rem;                  /* space BETWEEN items — no margin hacks */
  flex-wrap: wrap;            /* allow a second line when space runs out */
}
\`\`\`

\`justify-content\` is the one to internalize: \`flex-start\` (default), \`center\`,
\`space-between\` (first/last flush, even gaps), \`space-around\`, \`space-evenly\`.

\`gap\` is the modern answer to spacing. Before \`gap\`, people used child margins —
then spent careers fixing the edges. \`gap\` only spaces *between* items. Use it.

On the items:

\`\`\`css
.item {
  flex: 1;          /* grow to share free space equally */
}
.sidebar {
  flex: 0 0 200px;  /* don't grow, don't shrink, fixed 200px */
}
\`\`\`

\`flex: 1\` is the workhorse: "share the leftover space equally". A sidebar with
\`flex: 0 0 200px\` stays exactly 200px while the main column flexes.

## The two alignments, memorized

Main axis = the direction items flow in. Cross axis = the other one.

- \`justify-content\` → main axis
- \`align-items\` → cross axis

Flip \`flex-direction\` to \`column\` and the two swap *meanings* — this is why
"why is align-items left-right now?!" happens. Always ask: which way do the items flow?

## Vertical centering, finally trivial

\`\`\`css
.hero {
  display: flex;
  align-items: center;     /* cross axis */
  justify-content: center; /* main axis */
  min-height: 200px;
}
\`\`\`

The pattern that used to require hacks is now three honest lines.

## A nav bar, assembled

\`\`\`css
.nav {
  display: flex;
  justify-content: space-between; /* brand left, links right */
  align-items: center;
  gap: 1rem;
}
.nav ul {
  display: flex;
  gap: 1rem;
  list-style: none;
}
\`\`\`

\`\`\`html
<nav class="nav">
  <strong>MySite</strong>
  <ul>
    <li><a href="#">Home</a></li>
    <li><a href="#">About</a></li>
  </ul>
</nav>
\`\`\`

You now know the skeleton of every navigation bar on the web.

## What you learned

- Container: \`display: flex\`; children become flex items
- \`justify-content\` (main) vs \`align-items\` (cross) — and direction flips meanings
- \`gap\` for spacing; \`flex: 1\` to share space; \`flex-wrap: wrap\` to overflow gracefully
- The space-between navbar and the double-centering hero patterns

**Next:** Grid — two-dimensional layout.
`,
);

writeChallenge("css-flexbox", {
  id: "flex-the-navbar",
  title: "Flex the Navbar",
  prompt:
    "Turn the boilerplate's nav into a flex navbar:\n\n- `.nav` becomes a flex container with `space-between` (brand left, links right) and vertically centered items.\n- `.nav ul` also becomes flex, with a `1rem` gap between links and no list bullets.\n- Style links without underline on `.nav a` (in a nav, color+weight carry the affordance) — and set `color` explicitly.",
  difficulty: "beginner",
  boilerplate:
    '<nav class="nav">\n  <strong>MySite</strong>\n  <ul>\n    <li><a href="#">Home</a></li>\n    <li><a href="#">About</a></li>\n    <li><a href="#">Contact</a></li>\n  </ul>\n</nav>\n\n<style>\n  /* flex it */\n</style>\n',
  tests: [
    {
      name: "nav is flex with space-between",
      code: `const nav = code.match(/\\.nav\\s*{([^}]*)}/i);
if (!nav) {
  throw new Error("Add a .nav rule.");
}
if (!/display\\s*:\\s*flex/i.test(nav[1])) {
  throw new Error(".nav needs display: flex;");
}
if (!/justify-content\\s*:\\s*space-between/i.test(nav[1])) {
  throw new Error("Use justify-content: space-between to push brand and links apart.");
}
if (!/align-items\\s*:\\s*center/i.test(nav[1])) {
  throw new Error("Center the items vertically with align-items: center;");
}`,
      hint: "display: flex; justify-content: space-between; align-items: center; — the navbar trio.",
    },
    {
      name: "ul is flex with gap and no bullets",
      code: `const ul = code.match(/\\.nav\\s+ul\\s*{([^}]*)}/i);
if (!ul) {
  throw new Error("Add a .nav ul rule.");
}
if (!/display\\s*:\\s*flex/i.test(ul[1])) {
  throw new Error("The ul must also be a flex container.");
}
if (!/gap\\s*:\\s*1rem\\s*;/i.test(ul[1])) {
  throw new Error("Space the links with gap: 1rem;");
}
if (!/list-style\\s*:\\s*none/i.test(ul[1])) {
  throw new Error("Remove the bullets with list-style: none;");
}`,
      hint: "Flex containers nest: .nav ul { display: flex; gap: 1rem; list-style: none; }",
    },
    {
      name: "links styled, underline dropped deliberately",
      code: `const a = code.match(/\\.nav\\s+a\\s*{([^}]*)}/i);
if (!a) {
  throw new Error("Add a .nav a rule.");
}
if (!/color\\s*:\\s*[^;]+;/i.test(a[1])) {
  throw new Error("Set an explicit color on nav links.");
}
if (!/text-decoration\\s*:\\s*none/i.test(a[1])) {
  throw new Error("Set text-decoration: none on .nav a — inside the nav, color carries the affordance.");
}`,
      hint: ".nav a { color: …; text-decoration: none; } — scoped to the nav, not all links.",
    },
  ],
});

writeChallenge("css-flexbox", {
  id: "flex-the-card-row",
  title: "Independent: Card Row",
  prompt:
    "Build a responsive-ish card row with flex:\n\n- `.row` is a flex container whose items wrap when space runs out, with a `1rem` gap.\n- Each `.card` has `flex: 1` and a minimum width of `200px` (hint: flex-basis or min-width) so cards can't shrink into slivers.\n- All three cards end up the same width on wide screens (flex handles it).",
  difficulty: "beginner",
  boilerplate:
    '<div class="row">\n  <div class="card">One</div>\n  <div class="card">Two</div>\n  <div class="card">Three</div>\n</div>\n\n<style>\n  /* your layout */\n</style>\n',
  tests: [
    {
      name: "row wraps with gap",
      code: `const row = code.match(/\\.row\\s*{([^}]*)}/i);
if (!row) {
  throw new Error("Add a .row rule.");
}
if (!/display\\s*:\\s*flex/i.test(row[1])) {
  throw new Error(".row needs display: flex;");
}
if (!/flex-wrap\\s*:\\s*wrap/i.test(row[1])) {
  throw new Error("Allow wrapping with flex-wrap: wrap;");
}
if (!/gap\\s*:\\s*1rem\\s*;/i.test(row[1])) {
  throw new Error("Space cards with gap: 1rem;");
}`,
      hint: "display: flex; flex-wrap: wrap; gap: 1rem;",
    },
    {
      name: "cards share space with a floor",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card) {
  throw new Error("Add a .card rule.");
}
if (!/flex\\s*:\\s*1\\s*;/i.test(card[1])) {
  throw new Error("Give cards flex: 1; so they share space equally.");
}
if (!/(min-width\\s*:\\s*200px|flex-basis\\s*:\\s*200px)/i.test(card[1])) {
  throw new Error("Give cards a 200px floor (min-width or flex-basis).");
}`,
      hint: ".card { flex: 1; min-width: 200px; } — equal share, never thinner than 200px.",
    },
  ],
});

/* ── 3.9 Grid ────────────────────────────────────────────────────────── */

writeLesson(
  "css-grid",
  "CSS Grid",
  "Two-dimensional layout: define columns and rows once, place items into cells, and build page scaffolds in a dozen lines.",
  14,
  "beginner",
  ["grid-the-gallery"],
  `
Flexbox arranges a line; **Grid** arranges the whole board — rows *and* columns at
once. Page scaffolds, galleries, dashboards: any place two dimensions matter.

## The mental model

\`\`\`css
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
\`\`\`

- \`grid-template-columns\` defines the columns: here, three tracks, each \`1fr\`
  ("one fraction of the free space" — equal thirds).
- \`repeat(3, 1fr)\` is shorthand for \`1fr 1fr 1fr\`.
- \`gap\` works exactly as in flex — between rows and columns.
- Items flow into cells automatically, left-to-right, top-to-bottom.

## Fractions and friends

\`\`\`css
grid-template-columns: 200px 1fr;   /* fixed sidebar, flexible main */
grid-template-columns: 1fr 2fr;     /* one part, two parts */
grid-template-columns: auto 1fr;    /* content-sized, then the rest */
\`\`\`

\`fr\` distributes *leftover* space after fixed sizes — the "sidebar + main" layout is
one line, no floats, no hacks.

## Explicit placement

\`\`\`css
.featured {
  grid-column: 1 / -1;  /* span from first to last line: full width */
}
\`\`\`

Grid lines, not cells: column line 1 to line -1 (the end). \`span 2\` also works:
\`grid-column: span 2\`. This is how one tile swallows a row in a gallery.

## The page scaffold

\`\`\`css
.page {
  display: grid;
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}
header  { grid-column: 1 / -1; }
aside   { grid-column: 1; }
main    { grid-column: 2; }
footer  { grid-column: 1 / -1; }
\`\`\`

\`\`\`html
<div class="page">
  <header>…</header>
  <aside>…</aside>
  <main>…</main>
  <footer>…</footer>
</div>
\`\`\`

Named areas (\`grid-template-areas\`) are the next step — when you need it, it reads
like ASCII art of the page. For now, line-based placement covers real needs.

## Flex or Grid?

Ask: **one dimension or two?** A row of buttons, a nav, a toolbar → flex (content
drives, items flow). A page scaffold, a gallery, a form grid → grid (the *container*
defines the structure, items slot in). They compose: a grid cell can be a flex
container. That combination is how modern pages are built.

## What you learned

- \`display: grid\` + \`grid-template-columns\`; \`fr\` fractions; \`repeat()\`
- \`gap\` for the whole board; items auto-flow into cells
- \`grid-column: 1 / -1\` spans the full width
- Flex = one dimension (content-driven); Grid = two dimensions (structure-driven)

**Next:** responsive design — the same layouts, adapting to every screen.
`,
);

writeChallenge("css-grid", {
  id: "grid-the-gallery",
  title: "Grid the Gallery",
  prompt:
    "Build a photo gallery board:\n\n- `.gallery` is a grid with **three equal columns** and a `1rem` gap between all cells.\n- The `.featured` tile spans the full width of the first row.\n- The remaining tiles flow into the grid automatically (no per-tile placement needed).",
  difficulty: "beginner",
  boilerplate:
    '<div class="gallery">\n  <div class="featured">Hero photo</div>\n  <div>Photo 2</div>\n  <div>Photo 3</div>\n  <div>Photo 4</div>\n  <div>Photo 5</div>\n  <div>Photo 6</div>\n</div>\n\n<style>\n  /* grid it */\n</style>\n',
  tests: [
    {
      name: "gallery is a 3-column grid with gap",
      code: `const g = code.match(/\\.gallery\\s*{([^}]*)}/i);
if (!g) {
  throw new Error("Add a .gallery rule.");
}
if (!/display\\s*:\\s*grid/i.test(g[1])) {
  throw new Error(".gallery needs display: grid;");
}
if (!/grid-template-columns\\s*:\\s*repeat\\(\\s*3\\s*,\\s*1fr\\s*\\)/i.test(g[1])) {
  throw new Error("Three equal columns: grid-template-columns: repeat(3, 1fr);");
}
if (!/gap\\s*:\\s*1rem\\s*;/i.test(g[1])) {
  throw new Error("Space cells with gap: 1rem;");
}`,
      hint: "display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;",
    },
    {
      name: "featured tile spans full width",
      code: `const f = code.match(/\\.featured\\s*{([^}]*)}/i);
if (!f || !/grid-column\\s*:\\s*(1\\s*\\/\\s*-1|span\\s*3)/i.test(f[1])) {
  throw new Error("Make .featured span all columns: grid-column: 1 / -1;");
}`,
      hint: "grid-column: 1 / -1 stretches from the first to the last column line.",
    },
  ],
});

/* ── 3.10 Responsive Design ──────────────────────────────────────────── */

writeLesson(
  "css-responsive",
  "Responsive Design",
  "Mobile-first CSS with media queries: one page that works from a 375px phone to a wide desktop — and why mobile comes first.",
  16,
  "beginner",
  ["make-it-responsive"],
  `
More than half of web visits are phones. A site that only works at desktop width is a
broken site. Responsive design is not a feature — it is the baseline.

## The viewport meta tag

Before any CSS: responsive pages need this in the \`<head>\`:

\`\`\`html
<meta name="viewport" content="width=device-width, initial-scale=1" />
\`\`\`

Without it, phones pretend to be ~980px wide and zoom out — your beautiful flexbox
renders as a tiny desktop page. This tag says "the device width *is* the viewport".

## Mobile-first

Write the phone layout with **no media query at all**, then add queries for bigger
screens:

\`\`\`css
/* base = mobile */
.gallery {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

/* tablet and up */
@media (min-width: 640px) {
  .gallery {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* desktop and up */
@media (min-width: 1024px) {
  .gallery {
    grid-template-columns: repeat(3, 1fr);
  }
}
\`\`\`

Why mobile-first? Two reasons. Technically, \`min-width\` queries layer additions
cleanly — each level only overrides what changes. Practically, designing for the
smallest screen forces priority: what matters most? A desktop-first page tries to
shrink a mansion into a studio.

Standard breakpoints (conventions, not laws): ~640px (phone → tablet), ~768px (large
tablet), ~1024px (desktop), ~1280px (wide). Pick few breakpoints and reuse them.

## What flexes and grids give you for free

You have already learned responsive tools:

- \`1fr\` tracks, \`flex: 1\`, and percentages scale with the screen.
- \`flex-wrap: wrap\` reflows a toolbar when items no longer fit.
- \`rem\` sizing respects user font settings at every width.
- \`max-width: 100%\` on images stops any image from overflowing its container:

\`\`\`css
img {
  max-width: 100%;
  height: auto;
}
\`\`\`

Media queries are the *trim*; fluid layout is the *fabric*. A page built on fr units
and wrapping flex needs fewer queries than you expect.

## The responsive navigation pattern

The honest beginner pattern — no JavaScript needed:

\`\`\`css
.nav ul {
  display: flex;
  flex-direction: column;   /* stacked on phones */
  gap: 0.5rem;
}

@media (min-width: 640px) {
  .nav ul {
    flex-direction: row;    /* in a row on bigger screens */
    justify-content: space-between;
  }
}
\`\`\`

(Hamburger menus require JS and a11y care — Module 4 gives you the tools; you will
build one in the final project.)

## What you learned

- The viewport meta tag is a prerequisite, not an option
- Mobile-first: base styles for phones, \`@media (min-width: …)\` to enhance upward
- Fluid units (fr, %, rem, max-width: 100%) do most of the work; queries trim
- Column-to-row nav flips: the beginner pattern that ships

**Next:** transitions — motion, and its accessibility bill.
`,
);

writeChallenge("css-responsive", {
  id: "make-it-responsive",
  title: "Make It Responsive",
  prompt:
    "Turn a desktop-only page responsive:\n\n- Base (mobile): `.cards` stacks as a single-column grid.\n- At `min-width: 640px`: two columns. At `min-width: 1024px`: three columns.\n- Give `img` (or the `.cards img`) fluid behavior: `max-width: 100%` and `height: auto`.",
  difficulty: "beginner",
  boilerplate:
    '<div class="cards">\n  <div class="card"><img src="https://example.com/a.jpg" alt="Red Ferrari on a coastal road">Red car</div>\n  <div class="card"><img src="https://example.com/b.jpg" alt="Blue sailboat at anchor">Blue boat</div>\n  <div class="card"><img src="https://example.com/c.jpg" alt="Green train crossing a viaduct">Green train</div>\n</div>\n\n<style>\n  /* mobile-first responsive rules */\n</style>\n',
  tests: [
    {
      name: "single column by default",
      code: `const base = code.match(/\\.cards\\s*{([^}]*)}(?![\\s\\S]*@media[\\s\\S]*\\.cards\\s*{[^}]*\\1)/i);
const anyCards = code.match(/\\.cards\\s*{([^}]*)}/i);
if (!anyCards) {
  throw new Error("Add a .cards rule.");
}
const isGrid = /display\\s*:\\s*grid/i.test(anyCards[1]);
const firstIsOneCol = /grid-template-columns\\s*:\\s*(1fr\\s*;|none)/i.test(anyCards[1]);
if (!(isGrid && firstIsOneCol)) {
  throw new Error("The base .cards rule (outside media queries) must be a one-column grid.");
}`,
      hint: "Mobile-first: the base rule IS the phone layout — grid-template-columns: 1fr;",
    },
    {
      name: "two columns at 640px",
      code: `const q = code.match(/@media\\s*\\(\\s*min-width\\s*:\\s*640px\\s*\\)\\s*{([^@]*)/i);
if (!q || !/grid-template-columns\\s*:\\s*repeat\\(\\s*2\\s*,\\s*1fr\\s*\\)/i.test(q[1])) {
  throw new Error('Add @media (min-width: 640px) with two columns for .cards.');
}`,
      hint: "@media (min-width: 640px) { .cards { grid-template-columns: repeat(2, 1fr); } }",
    },
    {
      name: "three columns at 1024px",
      code: `const q = code.match(/@media\\s*\\(\\s*min-width\\s*:\\s*1024px\\s*\\)\\s*{([^@]*)/i);
if (!q || !/grid-template-columns\\s*:\\s*repeat\\(\\s*3\\s*,\\s*1fr\\s*\\)/i.test(q[1])) {
  throw new Error('Add @media (min-width: 1024px) with three columns for .cards.');
}`,
      hint: "Same pattern, bigger breakpoint: @media (min-width: 1024px) { … repeat(3, 1fr) … }",
    },
    {
      name: "fluid images",
      code: `const img = code.match(/(^|[\\s,])(img|\\.cards img)\\s*{([^}]*)}/im);
if (!img || !/max-width\\s*:\\s*100%/i.test(img[3]) || !/height\\s*:\\s*auto/i.test(img[3])) {
  throw new Error("Give images max-width: 100% and height: auto so they never overflow.");
}`,
      hint: "img { max-width: 100%; height: auto; } — shrink, never stretch.",
    },
  ],
});

/* ── 3.11 Transitions ────────────────────────────────────────────────── */

writeLesson(
  "css-transitions",
  "Transitions & Motion",
  "Hover and focus states that respond smoothly — and prefers-reduced-motion, the accessibility courtesy that separates good from careless.",
  10,
  "beginner",
  ["polish-the-button"],
  `
Motion is communication: a button that brightens on hover says "I am clickable". CSS
transitions make that response smooth — cheaply, correctly.

## The transition property

\`\`\`css
.button {
  background-color: #4b2e83;
  transition: background-color 0.2s ease;
}
.button:hover {
  background-color: #6a4bb0;
}
\`\`\`

\`transition\` names: *which property* animates, *how long*, and the *timing function*
(\`ease\` is the friendly default; \`linear\` is the robot). The transition lives on the
**base state** — then any change (hover, focus, class change) animates.

Multiple properties, comma-separated:

\`\`\`css
transition: background-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
\`\`\`

## The hover + focus duo

\`\`\`css
.button:hover,
.button:focus-visible {
  background-color: #6a4bb0;
}
\`\`\`

Two rules from the accessibility playbook:

1. **Focus must be as visible as hover.** Keyboard users get no hover — if hover
   changes appearance, focus must too. (\`:focus-visible\` shows the ring for keyboard
   users without shouting at mouse users.)
2. **Never remove the focus outline without a replacement** (\`outline: none\` alone
   breaks keyboard navigation). Style the ring if you dislike it; do not delete it.

## transform: the cheap animators

\`\`\`css
.card:hover {
  transform: translateY(-4px);
}
\`\`\`

\`translateY/X\`, \`scale\`, \`rotate\` — transforms are GPU-accelerated and do not
distort layout. Animating \`top\`/\`left\`/\`width\` re-layouts the page every frame;
animating \`transform\` composites. Prefer transform for movement.

## prefers-reduced-motion

For some users — vestibular disorders, motion sickness — animation is not decoration,
it is nausea. CSS listens:

\`\`\`css
@media (prefers-reduced-motion: reduce) {
  * {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
\`\`\`

Motion still *works* (states still change) but without movement. Two lines, all your
animations covered. This is the courtesy that marks professional CSS.

## What you learned

- \`transition: property duration timing;\` on the base state
- Pair \`:hover\` with \`:focus-visible\`; never naked \`outline: none\`
- Animate \`transform\`, not layout properties
- \`prefers-reduced-motion: reduce\` is the accessibility default for motion

**Next module project:** assemble it all into a responsive portfolio.
`,
);

writeChallenge("css-transitions", {
  id: "polish-the-button",
  title: "Polish the Button",
  prompt:
    "Give a plain button professional interaction states:\n\n- A `transition` on `.button` covering background-color (0.2s).\n- A `:hover` state that changes the background-color.\n- A matching `:focus-visible` state (same selector list or separate rule) so keyboard users see it too.\n- A `prefers-reduced-motion` media block that neutralizes transitions.",
  difficulty: "beginner",
  boilerplate:
    '<style>\n  .button {\n    padding: 10px 20px;\n    background-color: #4b2e83;\n    color: white;\n    border: none;\n  }\n</style>\n\n<button class="button">Sign up</button>\n',
  tests: [
    {
      name: "transition declared on base",
      code: `const b = code.match(/\\.button\\s*{([^}]*)}/i);
if (!b || !/transition[^;]*background-color[^;]*0\\.2s/i.test(b[1])) {
  throw new Error("Add transition: background-color 0.2s ease; to .button.");
}`,
      hint: "The transition belongs on the base state: transition: background-color 0.2s ease;",
    },
    {
      name: "hover changes color",
      code: `if (!/\\.button\\s*:\\s*hover\\s*{[^}]*background-color\\s*:\\s*[^;]+;/i.test(code)) {
  throw new Error("Add .button:hover { background-color: …; }");
}`,
      hint: ".button:hover { background-color: …; } — the state change the transition animates.",
    },
    {
      name: "focus-visible gets parity",
      code: `if (!/\\.button\\s*:\\s*focus-visible\\s*{[^}]*background-color\\s*:\\s*[^;]+;/i.test(code) && !/\\.button\\s*:\\s*hover\\s*,\\s*\\.button\\s*:\\s*focus-visible\\s*{[^}]*background-color/i.test(code)) {
  throw new Error("Keyboard users need the same visual feedback: add :focus-visible to the hover rule.");
}`,
      hint: ".button:hover, .button:focus-visible { … } — one rule, both input methods.",
    },
    {
      name: "reduced motion respected",
      code: `if (!/@media\\s*\\(\\s*prefers-reduced-motion\\s*:\\s*reduce\\s*\\)\\s*{[\\s\\S]*transition/i.test(code)) {
  throw new Error("Add a prefers-reduced-motion: reduce block that neutralizes transitions.");
}`,
      hint: "@media (prefers-reduced-motion: reduce) { * { transition-duration: 0.01ms; } }",
    },
  ],
});

/* ── 3.12 Project + module file ──────────────────────────────────────── */

writeLesson(
  "css-project-portfolio",
  "Project: Responsive Portfolio",
  "The module project: style your profile page into a polished, responsive portfolio — box model, flex/grid, custom properties, media queries, and motion.",
  20,
  "beginner",
  ["style-the-portfolio"],
  `
Everything from this module converges on one page: **your** portfolio. You are styling
the profile page from Module 2 — or a fresh equivalent structure; the tests only check
the CSS and the page's structure hooks.

## The brief

1. **Foundation**: universal \`box-sizing: border-box\`; a \`font-family\` stack on
   \`body\`; \`line-height\` ≥ 1.5.
2. **Theme**: \`--brand\`, \`--accent\`, and \`--space\` custom properties on \`:root\`,
   used by at least three rules.
3. **Layout**: the page uses **flex or grid** for its main structure — a nav that is
   flex; sections that sit in a grid (or stack single-column on mobile via grid).
4. **Responsive**: mobile-first — base rules for phones, \`@media (min-width: 640px)\`
   enhancing the layout for larger screens.
5. **Polish**: \`border-radius\` on cards; padding that shows the box model is under
   control; links keep affordance; focus styles present.
6. **Motion**: a transition on at least one interactive element, plus a
   \`prefers-reduced-motion\` block.

## Why these requirements

Each one maps to a lesson you completed. A real client brief reads exactly like this —
verifiable outcomes, not vibes. Work through the list top to bottom, run the tests,
and read every failure as a pointer back to its lesson.

## What good looks like

Not "matches a screenshot" — the design is yours. Good means: resize the window from
phone to desktop and nothing breaks, overlaps, or overflows; every interactive element
responds to keyboard; the palette is consistent because it comes from variables.

**Next module:** JavaScript Foundations — the page starts to *do* things.
`,
);

writeChallenge("css-project-portfolio", {
  id: "style-the-portfolio",
  title: "Style Your Portfolio",
  prompt:
    "Deliver the module project: a themed, responsive, motion-polished portfolio stylesheet meeting the six brief requirements (foundation, theme variables, flex/grid layout, mobile-first media queries, polish, reduced motion).",
  difficulty: "beginner",
  boilerplate:
    '<!-- Page structure (style these or your own equivalents) -->\n<nav class="site-nav">\n  <strong>My Portfolio</strong>\n  <ul><li><a href="#work">Work</a></li><li><a href="#contact">Contact</a></li></ul>\n</nav>\n<main>\n  <section class="card"><h2>Work</h2><p>Things I have built.</p></section>\n  <section class="card" id="contact"><h2>Contact</h2><p>Say hello.</p></section>\n</main>\n\n<style>\n  /* your portfolio stylesheet */\n</style>\n',
  tests: [
    {
      name: "foundation: border-box, font stack, line-height",
      code: `if (!/box-sizing\\s*:\\s*border-box/i.test(code)) {
  throw new Error("Universal box-sizing: border-box is missing.");
}
const body = code.match(/body\\s*{([^}]*)}/i);
if (!body || !/font-family\\s*:[^;]+(sans-serif|serif|monospace)/i.test(body[1])) {
  throw new Error("Set font-family (ending in a generic family) on body.");
}
const lh = body && body[1].match(/line-height\\s*:\\s*([\\d.]+)/i);
if (!lh || Number(lh[1]) < 1.5) {
  throw new Error("body line-height must be ≥ 1.5 (unitless).");
}`,
      hint: "The foundation trio from the box model and typography lessons.",
    },
    {
      name: "theme: custom properties used in 3+ rules",
      code: `if (!/:root\\s*{[^}]*--brand\\s*:/i.test(code)) {
  throw new Error("Declare --brand (and friends) on :root.");
}
const varUses = (code.match(/var\\(--[\\w-]+\\)/gi) || []).length;
if (varUses < 3) {
  throw new Error("Use var(--…) in at least three rules (found " + varUses + ").");
}`,
      hint: "Define on :root, consume with var() — consistency comes free.",
    },
    {
      name: "layout: flex nav and grid/flex main",
      code: `if (!/\\.site-nav\\s*{[^}]*display\\s*:\\s*flex/i.test(code)) {
  throw new Error("The nav (.site-nav) must be a flex container.");
}
if (!/(main|\\.cards|\\.gallery|\\.layout)[^{]*{[^}]*display\\s*:\\s*(grid|flex)/i.test(code)) {
  throw new Error("Lay out the page structure with display: grid or flex on main (or a wrapper).");
}`,
      hint: "nav → flex; page sections → grid (or flex). The layout lessons, applied.",
    },
    {
      name: "responsive: mobile-first media query",
      code: `if (!/@media\\s*\\(\\s*min-width\\s*:\\s*\\d+px\\s*\\)\\s*{/i.test(code)) {
  throw new Error("Add a mobile-first @media (min-width: …) query.");
}
if (/@media[^{]*max-width/i.test(code)) {
  throw new Error("Use min-width (mobile-first) queries — not desktop-first max-width.");
}`,
      hint: "min-width queries layer the phone layout upward.",
    },
    {
      name: "motion: transition + reduced motion",
      code: `if (!/transition\\s*:[^;]+;/i.test(code)) {
  throw new Error("Add a transition to an interactive element.");
}
if (!/@media\\s*\\(\\s*prefers-reduced-motion\\s*:\\s*reduce\\s*\\)/i.test(code)) {
  throw new Error("Add the prefers-reduced-motion block.");
}`,
      hint: "transition + prefers-reduced-motion — polish with a conscience.",
    },
    {
      name: "polish: rounded cards and link affordance",
      code: `if (!/border-radius\\s*:\\s*[\\d.]+px/i.test(code)) {
  throw new Error("Round something — border-radius on .card or buttons.");
}
if (/a\\s*{[^}]*text-decoration\\s*:\\s*none/i.test(code)) {
  throw new Error("Links keep their underline (or gain another strong affordance) — no naked text-decoration: none on all links.");
}`,
      hint: "Cards round; links stay recognizable.",
    },
  ],
});

/* module.json */
mkdirSync(MOD, { recursive: true });
writeFileSync(
  path.join(MOD, "module.json"),
  JSON.stringify(
    {
      id: "css-foundations",
      title: "CSS Foundations",
      summary:
        "Make pages yours: selectors and the cascade, the box model, typography, Flexbox and Grid, responsive design, and motion with a conscience.",
      lessons: [
        { reference: "what-css-is" },
        { reference: "selectors-and-cascade" },
        { reference: "units-colors-values" },
        { reference: "css-typography" },
        { reference: "css-box-model" },
        { reference: "css-display-flow" },
        { reference: "css-positioning" },
        { reference: "css-flexbox" },
        { reference: "css-grid" },
        { reference: "css-responsive" },
        { reference: "css-transitions" },
        { reference: "css-project-portfolio" },
      ],
    },
    null,
    2,
  ) + "\n",
);
console.log("module.json written");
