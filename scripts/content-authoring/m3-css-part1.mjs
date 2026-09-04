/**
 * Author Module 3 (CSS Foundations) — part 1: lessons 1–6.
 * Challenge test code is written via JSON.stringify — no shell escaping.
 * Run: node scripts/content-authoring/m3-css-part1.mjs
 */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";

const DIR =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/css-foundations/lessons";

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

/* ── 3.1 What CSS Is & How to Add It ─────────────────────────────────── */

writeLesson(
  "what-css-is",
  "What CSS Is & How to Add It",
  "Meet CSS: what it does, what a rule looks like, and the three ways to attach it to a page — and why one of them is the right answer.",
  8,
  "beginner",
  ["style-the-page"],
  `
Your HTML pages work — every element has a sensible default look. But "sensible default"
is not "yours". CSS is the language that takes over appearance.

## What CSS does

CSS (*Cascading Style Sheets*) is a list of **rules**. Each rule says: *when an element
matches this selector, apply these declarations.*

\`\`\`css
h1 {
  color: seagreen;
}
\`\`\`

The anatomy, named:

- \`h1\` — the **selector**: which elements the rule targets.
- \`color: seagreen;\` — a **declaration**: a *property* (\`color\`), a colon, a *value*
  (\`seagreen\`), a semicolon.
- Everything between \`{ }\` is the **declaration block**.

Declarations always end with a semicolon. Forgetting one is the classic first CSS bug —
the rule silently stops making sense at that point. When your style "doesn't work",
check the semicolon and the braces before anything else.

## Three ways to attach CSS

**1. Inline styles** — a \`style\` attribute on one element:

\`\`\`html
<p style="color: seagreen">Green text</p>
\`\`\`

**2. Internal stylesheet** — a \`<style>\` block in the \`<head>\`:

\`\`\`html
<head>
  <style>
    p { color: seagreen; }
  </style>
</head>
\`\`\`

**3. External stylesheet** — a separate \`.css\` file, linked from the \`<head>\`:

\`\`\`html
<head>
  <link rel="stylesheet" href="styles.css" />
</head>
\`\`\`

## Why external wins

Inline styles fight everything you will learn: they cannot be reused, they override
your stylesheet in ways that cause confusion, and they bury appearance inside content.
Internal styles are fine for quick experiments but live trapped in one file.

An external stylesheet is cached by the browser and shared by every page of your site:
write \`h1 { ... }\` once, and every page that links the file follows. It also enforces
the separation this course keeps returning to — content in HTML, appearance in CSS.

From here on, every example assumes an external \`styles.css\`.

## What you learned

- Rules: selector + declaration block; property: value; semicolons matter
- Inline, internal, and external CSS — and why external is the professional default
- The \`<link rel="stylesheet">\` pattern you will use for the rest of the course

**Next:** the selector zoo — how to target *exactly* the elements you mean.
`,
);

writeChallenge("what-css-is", {
  id: "style-the-page",
  title: "First Stylesheet",
  prompt: 'Write your first external-stylesheet pattern, inline in one file:\n\n- A `<style>` block containing a rule for `h1` that sets `color` (any color you like).\n- A second rule for `p` that sets `font-size` to a value with units (e.g. `18px`).\n- Every declaration must end with a semicolon.',
  difficulty: "beginner",
  boilerplate: "<style>\n  /* your rules here */\n</style>\n\n<h1>My styled page</h1>\n<p>Paragraphs deserve nice type too.</p>\n",
  tests: [
    {
      name: "has a style block",
      code: `if (!/<style[\\s>][\\s\\S]*?<\\/style>/i.test(code)) {
  throw new Error("Put your CSS in a <style> block.");
}`,
      hint: "Internal styles live between <style> and </style> — usually in the <head>.",
    },
    {
      name: "h1 rule sets color",
      code: `const rule = code.match(/h1\\s*{([^}]*)}/i);
if (!rule) {
  throw new Error("No h1 rule found — write h1 { ... }.");
}
if (!/color\\s*:\\s*[^;]+;/i.test(rule[1])) {
  throw new Error("The h1 rule must set color — and end the declaration with a semicolon.");
}`,
      hint: "h1 { color: seagreen; } — property, colon, value, semicolon.",
    },
    {
      name: "p rule sets font-size with units",
      code: `const rule = code.match(/p\\s*{([^}]*)}/i);
if (!rule) {
  throw new Error("No p rule found — write p { ... }.");
}
if (!/font-size\\s*:\\s*\\d+(px|rem|em|%)/i.test(rule[1])) {
  throw new Error("The p rule must set font-size with units, e.g. font-size: 18px;");
}`,
      hint: "font-size: 18px; — a bare number is not a size.",
    },
  ],
});

/* ── 3.2 Selectors, Classes & the Cascade ────────────────────────────── */

writeLesson(
  "selectors-and-cascade",
  "Selectors, Classes & the Cascade",
  "Target exactly the elements you mean with element, class, ID, and descendant selectors — and learn how the cascade decides who wins.",
  14,
  "beginner",
  ["selector-scavenger-hunt", "fix-the-cascade-bug"],
  `
CSS is only as precise as its selectors. This lesson is the targeting system.

## Element, class, ID

\`\`\`css
p { }          /* every <p> */
.note { }      /* every element with class="note" */
#signup { }    /* the one element with id="signup" */
\`\`\`

- **Element selectors** paint with a roller — good for base typography.
- **Classes** are the workhorse: reusable, multiple per element
  (\`class="card highlight"\`), and they carry *no* built-in meaning, so you name them by
  purpose (\`.site-nav\`, \`.price\`), not by looks (\`.big-red\` — renames hurt).
- **IDs** select one element. They are *more specific* than classes (see the cascade
  below), which makes them dangerous to style with — a single ID rule can quietly beat
  any number of class rules. Use IDs for anchors and JS hooks; style with classes.

## Descendant selectors

Target by ancestry:

\`\`\`css
nav a {
  color: darkslateblue;
}
\`\`\`

Read it right-to-left: "any \`a\` inside a \`nav\`". Links elsewhere are untouched. This
is how you style *regions*: \`nav a\`, \`article p\`, \`footer a\`.

## Grouping

\`\`\`css
h1,
h2,
h3 {
  font-family: Georgia, serif;
}
\`\`\`

One declaration block shared by several selectors — commas, not repetition.

## The cascade: who wins?

"CSS" literally contains *cascading*: when several rules target the same element, the
browser resolves conflicts in a definite order. For beginner purposes:

1. **Later beats earlier** — at equal specificity, the last rule written wins.
2. **More specific beats less specific** — ID (1,0,0) > class (0,1,0) > element (0,0,1).
   Count like this: \`#signup .note p\` is (1,1,1) — it beats any \`.note\` rule.
3. **Inline styles beat both** (style="…" counts as (1,0,0,0) — avoid them).

\`\`\`css
p { color: gray; }      /* (0,0,1) */
.note { color: blue; }  /* (0,1,0) — wins over p for .note elements */
#hero { color: teal; }  /* (1,0,0) — wins over everything above */
\`\`\`

One important exception — \`!important\` forces a declaration to win regardless. It
exists for edge cases (user style overrides, utility frameworks). In hand-written CSS
it is a code smell: if you need \`!important\` to win, your selectors are fighting each
other — fix the specificity, not the symptom.

## Inheritance, the quiet one

Some properties flow down the tree automatically: \`color\`, \`font-family\`,
\`line-height\`. Set \`font-family\` once on \`body\`, and every child inherits it — that
is why global typography lives on \`body\`. Layout properties like \`margin\` and
\`border\` do *not* inherit: each box gets its own.

## What you learned

- Element / class / ID selectors and when each is appropriate
- Descendant selectors style by region; grouping shares a block
- Cascade resolution: source order, then specificity (ID > class > element), inline on top
- \`!important\` is a smell; inheritance explains body-level typography

**Next:** units and colors — how CSS measures and paints.
`,
);

writeChallenge("selectors-and-cascade", {
  id: "selector-scavenger-hunt",
  title: "Selector Scavenger Hunt",
  prompt: "The boilerplate has a small page. Without touching the HTML, write CSS that:\n\n- Sets `color` on every `<h2>` (element selector).\n- Sets a `background-color` on elements of class `card`.\n- Sets `color` on links *only inside* the nav (descendant selector).\n- Sets `font-family` on the single element with id `tagline`.",
  difficulty: "beginner",
  boilerplate: "<nav>\n  <a href=\"#top\">Home</a>\n  <a href=\"#posts\">Posts</a>\n</nav>\n\n<h2>Latest posts</h2>\n\n<p id=\"tagline\">Notes from a beginner who ships.</p>\n\n<div class=\"card\">First post</div>\n<div class=\"card\">Second post</div>\n\n<a href=\"https://example.com\">An outside link</a>\n\n<style>\n  /* write your rules here */\n</style>\n",
  tests: [
    {
      name: "h2 colored via element selector",
      code: `const rule = code.match(/(?:^|[\\s,])(h2)\\s*{([^}]*)}/im);
if (!rule || !/color\\s*:\\s*[^;]+;/i.test(rule[2])) {
  throw new Error("Add an h2 { color: ...; } rule.");
}
if (/[.#]h2/i.test(code)) {
  throw new Error("Use the plain element selector h2 — no dots or hashes.");
}`,
      hint: "Element selectors are bare tag names: h2 { color: …; }.",
    },
    {
      name: "card class gets background",
      code: `const rule = code.match(/\\.card\\s*{([^}]*)}/i);
if (!rule) {
  throw new Error('No .card rule — classes are selected with a leading dot.');
}
if (!/background(-color)?\\s*:\\s*[^;]+;/i.test(rule[1])) {
  throw new Error("The .card rule must set a background-color (or background).");
}`,
      hint: ".card { background-color: …; } — the dot means 'class'.",
    },
    {
      name: "nav links via descendant selector",
      code: `const rule = code.match(/nav\\s+a\\s*{([^}]*)}/i);
if (!rule) {
  throw new Error("Add a descendant selector: nav a { ... }.");
}
if (!/color\\s*:\\s*[^;]+;/i.test(rule[1])) {
  throw new Error("The nav a rule must set color.");
}
if (/(^|[\\s,])a\\s*{[^}]*color\\s*:/im.test(code)) {
  throw new Error("You styled ALL links — scope it to nav a so the outside link keeps its color.");
}`,
      hint: "nav a { … } reads 'any <a> inside <nav>' — the outside link is untouched.",
    },
    {
      name: "tagline id styled",
      code: `const rule = code.match(/#tagline\\s*{([^}]*)}/i);
if (!rule) {
  throw new Error("No #tagline rule — IDs are selected with a leading hash.");
}
if (!/font-family\\s*:\\s*[^;]+;/i.test(rule[1])) {
  throw new Error("The #tagline rule must set font-family.");
}`,
      hint: "#tagline { font-family: Georgia, serif; } — the hash means 'id'.",
    },
  ],
});

writeChallenge("selectors-and-cascade", {
  id: "fix-the-cascade-bug",
  title: "Debug: The Losing Rule",
  prompt: "A developer complains: 'my `.price` color rule is ignored!'. The stylesheet has a more specific rule that also sets color on the same element. Find the fight and fix it the *right* way — make the class rule win by lowering the other rule's specificity or scoping it, NOT with !important.",
  difficulty: "beginner",
  boilerplate: "<div class=\"product\">\n  <p class=\"price\">$49</p>\n</div>\n\n<style>\n  #main div p {\n    color: gray;\n  }\n\n  .price {\n    color: crimson;\n  }\n</style>\n",
  tests: [
    {
      name: "price displays crimson",
      code: `const price = code.match(/\\.price\\s*{([^}]*)}/i);
if (!price) {
  throw new Error("Keep the .price rule.");
}
if (!/crimson/i.test(price[1])) {
  throw new Error("Keep .price's color crimson.");
}
const idFight = code.match(/#[\\w-]+[^{]*{[^}]*color\\s*:/i);
if (idFight) {
  throw new Error("The ID rule still out-specifies .price — lower its specificity (e.g. drop the ID from the selector) or scope it so it no longer hits .price.");
}
if (/!important/i.test(code)) {
  throw new Error("No !important — fix the specificity, not the symptom.");
}`,
      hint: "An ID in the selector (1,0,x) beats any class (0,1,0). Weaken the fighting selector until the meaningful .price rule wins.",
    },
    {
      name: "no important flag",
      code: `if (/!important/i.test(code)) {
  throw new Error("!important is banned here — resolve the conflict properly.");
}`,
      hint: "Real fixes reorder or rescope rules; !important hides the design problem.",
    },
  ],
});

/* ── 3.3 Units, Colors & Values ──────────────────────────────────────── */

writeLesson(
  "units-colors-values",
  "Units, Colors & Values",
  "Pixels vs rem, the color notations you will actually use, and CSS custom properties — the variables that keep a design consistent.",
  10,
  "beginner",
  ["theme-with-custom-properties"],
  `
CSS values look simple — and then \`62.5%\` of a font renders differently than you
expected. The unit system is worth ten careful minutes.

## Lengths: absolute and relative

- \`px\` — pixels. Predictable, but *rigid*: it does not respect a user's browser font
  settings.
- \`rem\` — "root em": a multiple of the **root element's font size** (browsers default
  to 16px, but users can change it). \`1.5rem\` = 1.5 × that size.
- \`em\` — a multiple of the *current element's* font size. Powerful, compounding —
  subtle. Beginners: prefer \`rem\`.
- \`%\` — relative to the parent (commonly widths).

**Why rem matters:** a low-vision user who raises their default font size to 24px sees
an all-\`rem\` site scale gracefully — text, padding, everything. An all-\`px\` site
stays frozen. Modern guidance: font sizes in \`rem\`, fine-grained visual details may
use \`px\`.

\`\`\`css
body {
  font-size: 1rem;      /* 16px at default settings */
}
h1 {
  font-size: 2rem;      /* twice the root size — scales with user settings */
}
\`\`\`

## Colors

Three notations cover everything:

\`\`\`css
a { color: rebeccapurple; }              /* named */
a { color: #4b2e83; }                    /* hex: RR GG BB */
a { color: rgb(75 46 131); }             /* rgb() — same thing, decimal */
a { color: rgb(75 46 131 / 0.6); }       /* with alpha transparency */
\`\`\`

Hex is the everyday workhorse (\`#fff\` = white, \`#000\` = black). Modern syntax omits
the commas. Alpha — the last value, 0–1 — controls transparency.

One rule this course holds you to: **color contrast**. Text you can barely read is a
design failure, not a style choice. Light gray on white fails; WCAG 2.1 AA (the
standard Code Journey itself meets) wants roughly 4.5:1 for body text. Check yours.

## Custom properties: CSS variables

\`\`\`css
:root {
  --brand: #4b2e83;
  --space: 1rem;
}

a {
  color: var(--brand);
}
.button {
  background-color: var(--brand);
  padding: var(--space);
}
\`\`\`

Declare on \`:root\` (the root element), use with \`var()\`. Change \`--brand\` once and
every usage follows. This is how real stylesheets avoid fifteen slightly-different
purples — and you will meet it again as the backbone of theming.

## What you learned

- \`px\` is rigid; \`rem\` scales with user font settings — prefer it for type
- Named, hex, and \`rgb()\` colors, plus alpha transparency
- Contrast is a requirement, not a preference
- Custom properties (\`--name\`, \`var(--name)\`) centralize design decisions

**Next:** typography — fonts, line length, and readable text.
`,
);

writeChallenge("units-colors-values", {
  id: "theme-with-custom-properties",
  title: "Build a Mini Theme",
  prompt: "Create a small theme with custom properties:\n\n- On `:root`, declare `--brand` (any color) and `--space` (a rem value).\n- Style `.button` using `var(--brand)` as its background-color and `var(--space)` as its padding.\n- Style `p` with a `font-size` in `rem` (no px).",
  difficulty: "beginner",
  boilerplate: "<style>\n  /* your theme here */\n</style>\n\n<p>Modern type scales with the reader.</p>\n<button class=\"button\">Join now</button>\n",
  tests: [
    {
      name: "custom properties declared on :root",
      code: `const root = code.match(/:root\\s*{([^}]*)}/i);
if (!root) {
  throw new Error("Declare your variables on :root { ... }.");
}
if (!/--brand\\s*:/i.test(root[1])) {
  throw new Error("Declare --brand on :root.");
}
if (!/--space\\s*:/i.test(root[1])) {
  throw new Error("Declare --space on :root.");
}`,
      hint: ":root { --brand: #4b2e83; --space: 1rem; }",
    },
    {
      name: "button uses both variables",
      code: `const btn = code.match(/\\.button\\s*{([^}]*)}/i);
if (!btn) {
  throw new Error("Add a .button rule.");
}
if (!/background(-color)?\\s*:\\s*var\\(--brand\\)/i.test(btn[1])) {
  throw new Error("The .button background must come from var(--brand).");
}
if (!/padding\\s*:\\s*var\\(--space\\)/i.test(btn[1])) {
  throw new Error("The .button padding must come from var(--space).");
}`,
      hint: "var(--name) reads a custom property — .button { background-color: var(--brand); padding: var(--space); }",
    },
    {
      name: "rem font size",
      code: `const p = code.match(/(?:^|[\\s,])(p)\\s*{([^}]*)}/im);
if (!p || !/font-size\\s*:\\s*[\\d.]+rem\\s*;/i.test(p[2])) {
  throw new Error("Give p a rem font-size, e.g. font-size: 1rem;");
}`,
      hint: "font-size: 1rem; — rem scales with the reader's settings, px does not.",
    },
  ],
});

/* ── 3.4 Typography ──────────────────────────────────────────────────── */

writeLesson(
  "css-typography",
  "Typography & Readability",
  "Fonts, sizes, line-height, and line length — the four decisions that decide whether people finish reading your page.",
  10,
  "beginner",
  ["make-it-readable"],
  `
Most of the web is text. Typography is not decoration; it is the difference between a
page people read and a page they flee.

## Font stacks

\`\`\`css
body {
  font-family: Georgia, "Times New Roman", serif;
}
\`\`\`

A font stack is a fallback list: the browser uses Georgia if installed, otherwise
Times New Roman, otherwise any serif. Always end with a generic family (\`serif\`,
\`sans-serif\`, \`monospace\`). Multi-word names go in quotes.

Most sites use the system fonts already on the device — they load instantly and look
native:

\`\`\`css
font-family: system-ui, sans-serif;
\`\`\`

Loading custom fonts from files is a real technique (later concern — and it costs
bandwidth and a flash of fallback text).

## Size and line-height

\`\`\`css
body {
  font-size: 1rem;
  line-height: 1.6;
}
\`\`\`

Line-height as a bare number (not px!) means "1.6 × the font size" — and it scales if
the size changes. Dense single-spaced text is the most common amateur tell; 1.5–1.7
is comfortable for body text.

## Line length

Reading research is blunt: **45–75 characters per line**, ~66 ideal. On a desktop,
a full-width paragraph is 120+ characters — eyes lose the line when jumping back.
Later, the layout module gives you the tools to cap content width; until then, note
that wide paragraphs are a layout problem, not a font-size problem.

## Weight, style, decoration

- \`font-weight: bold\` (or \`700\`) / \`normal\` (\`400\`).
- \`font-style: italic\`.
- \`text-decoration: underline\` — and the beginner rule that matters: **links should
  look like links**. Removing link underlines is acceptable *only* if something else
  (color + weight) clearly distinguishes them; color alone fails contrast-sensitive
  and color-blind users.

## Aligning

\`\`\`css
text-align: left;   /* default for LTR text */
\`\`\`

Leave body text left-aligned: fully-justified text creates "rivers" of white space
that punish dyslexic readers hardest. Centered text is for headings and short lines.

## What you learned

- Font stacks end in a generic family; system-ui is the fast default
- \`line-height\` as a unitless number; 1.5–1.7 for body text
- 45–75 characters per line; width control comes with layout
- Links stay visually distinct; body text stays left-aligned

**Next:** the box model — how CSS measures every element.
`,
);

writeChallenge("css-typography", {
  id: "make-it-readable",
  title: "Make It Readable",
  prompt: "Fix a deliberately uncomfortable page of text. Set:\n\n- A `font-family` stack on `body` that ends with a generic family (`sans-serif` or `serif`).\n- `line-height` on `body` as a bare number between 1.4 and 2.\n- `h1` with a `font-size` in `rem`.\n- Link color that is not the default (your choice) — keep the underline present (do not set text-decoration: none on links).",
  difficulty: "beginner",
  boilerplate: "<style>\n  body {\n    line-height: 1;\n  }\n\n  a {\n    text-decoration: none;\n  }\n</style>\n\n<h1>A very dense article</h1>\n<p>This paragraph is cramped, single-spaced, and hard to track line by line. Readers abandon dense pages quickly, and low-vision readers abandon them faster.</p>\n<p><a href=\"https://example.com\">A link that lost its affordance</a></p>\n",
  tests: [
    {
      name: "body font stack ends generic",
      code: `const body = code.match(/body\\s*{([^}]*)}/i);
if (!body || !/font-family\\s*:[^;]+(sans-serif|serif|monospace)\\s*;/i.test(body[1])) {
  throw new Error("Set font-family on body, ending with a generic family like sans-serif;");
}`,
      hint: 'font-family: system-ui, sans-serif; — the generic family is the safety net.',
    },
    {
      name: "healthy line-height",
      code: `const body = code.match(/body\\s*{([^}]*)}/i);
const m = body && body[1].match(/line-height\\s*:\\s*([\\d.]+)/i);
if (!m) {
  throw new Error("Set line-height on body.");
}
const n = Number(m[1]);
if (!(n >= 1.4 && n <= 2)) {
  throw new Error("line-height should be a number between 1.4 and 2 (got " + m[1] + ").");
}`,
      hint: "line-height: 1.6; — a unitless number multiplies the font size.",
    },
    {
      name: "rem heading size",
      code: `const h1 = code.match(/h1\\s*{([^}]*)}/i);
if (!h1 || !/font-size\\s*:\\s*[\\d.]+rem\\s*;/i.test(h1[1])) {
  throw new Error("Give h1 a font-size in rem.");
}`,
      hint: "font-size: 2rem; scales with the reader's settings.",
    },
    {
      name: "links keep their affordance",
      code: `const link = code.match(/a\\s*{([^}]*)}/i);
if (link && /text-decoration\\s*:\\s*none/i.test(link[1])) {
  throw new Error("Links must keep their underline — restore it (or omit text-decoration entirely).");
}
if (!link || !/color\\s*:\\s*[^;]+;/i.test(link[1])) {
  throw new Error("Give links a color of your choice.");
}`,
      hint: "Underlines are how everyone recognizes links at a glance — style color, keep the affordance.",
    },
  ],
});

/* ── 3.5 The Box Model ───────────────────────────────────────────────── */

writeLesson(
  "css-box-model",
  "The Box Model",
  "Every element is a box of content, padding, border, and margin — understand the math and the sizing surprises disappear.",
  14,
  "beginner",
  ["box-model-prediction", "space-the-card"],
  `
Layout bugs are usually box-model bugs. This lesson removes the surprise permanently.

## Every element is four boxes nested together

\`\`\`
┌─────────────────────────────────┐
│  margin (transparent, outside)  │
│  ┌───────────────────────────┐  │
│  │  border                   │  │
│  │  ┌─────────────────────┐  │  │
│  │  │  padding            │  │  │
│  │  │  ┌───────────────┐  │  │  │
│  │  │  │  content      │  │  │  │
│  │  │  └───────────────┘  │  │  │
│  │  └─────────────────────┘  │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
\`\`\`

- **content** — the text/image itself; sized by \`width\`/\`height\`.
- **padding** — space *inside* the border, between content and edge. Padding carries
  the element's background.
- **border** — the line. \`border: 2px solid\`.
- **margin** — transparent space *outside* the border, pushing neighbors away.

\`\`\`css
.card {
  padding: 1rem;
  border: 2px solid gray;
  margin: 1rem;
}
\`\`\`

Padding and margin each take 1–4 values (top/right/bottom/left, clockwise): \`padding:
4px 8px\` = 4 top & bottom, 8 left & right. There are also single sides: \`margin-top\`,
\`padding-left\`, ….

## The prediction every beginner gets wrong

With default \`box-sizing: content-box\`, \`width\` sizes only the *content* box:

\`\`\`css
.box {
  width: 200px;
  padding: 20px;   /* both sides */
  border: 4px solid;
}
\`\`\`

Real rendered width = 200 + 20 + 20 + 4 + 4 = **248px**. Not 200. Set two of these
side by side and they wrap when you were sure they would fit.

## The universal fix

\`\`\`css
*,
*::before,
*::after {
  box-sizing: border-box;
}
\`\`\`

With \`border-box\`, \`width\` includes padding and border — \`width: 200px\` means the
whole box is 200px. This single rule (at the top of every stylesheet on earth) removes
the entire class of surprise. You will put it in every project stylesheet from now on.

## Margin collapse (know it exists)

Vertical margins between siblings *merge* instead of adding: a \`margin-bottom: 32px\`
above a \`margin-top: 16px\` yields 32px of gap, not 48. Not a bug — a feature you
work with. Practical rule: space sections with one consistent direction of margin.

## What you learned

- content → padding → border → margin, and which carry background
- \`width\` excludes padding/border under default sizing — the 200px ≠ 200px trap
- \`box-sizing: border-box\` on everything is the professional default
- Adjacent vertical margins collapse to the larger

**Next:** \`display\` — how elements decide to stack or flow.
`,
);

writeChallenge("css-box-model", {
  id: "box-model-prediction",
  title: "Prediction: Box Math",
  prompt: "A challenge in two parts.\n\nPART 1 — fix the sizing: the `.box` in the boilerplate has width: 200px but renders 248px wide. Add the universal border-box rule at the top of the stylesheet so width means what it says. Keep the .box rule exactly as it is.\n\nPART 2 — space it out: give `.box` a margin of `1rem` on all sides.",
  difficulty: "beginner",
  boilerplate: "<style>\n  .box {\n    width: 200px;\n    padding: 20px;\n    border: 4px solid dimgray;\n  }\n</style>\n\n<div class=\"box\">200 means 200</div>\n",
  tests: [
    {
      name: "universal border-box applied",
      code: `if (!/\\*\\s*,\\s*\\*::before\\s*,\\s*\\*::after\\s*{[^}]*box-sizing\\s*:\\s*border-box/i.test(code) && !/\\*\\s*{[^}]*box-sizing\\s*:\\s*border-box/i.test(code)) {
  throw new Error("Add the universal rule: *, *::before, *::after { box-sizing: border-box; }");
}
if (!/box-sizing\\s*:\\s*border-box/i.test(code)) {
  throw new Error("box-sizing: border-box is missing.");
}`,
      hint: "The universal selector (*) with box-sizing: border-box is the first rule of every stylesheet.",
    },
    {
      name: "box rule unchanged",
      code: `const box = code.match(/\\.box\\s*{([^}]*)}/i);
if (!box) {
  throw new Error("The .box rule went missing.");
}
if (!/width\\s*:\\s*200px/i.test(box[1]) || !/padding\\s*:\\s*20px/i.test(box[1]) || !/border\\s*:\\s*4px/i.test(box[1])) {
  throw new Error("Keep the .box rule exactly as given (width 200px, padding 20px, border 4px).");
}`,
      hint: "The point is that border-box changes the *interpretation* of width — the rule itself stays.",
    },
    {
      name: "margin all sides",
      code: `const box = code.match(/\\.box\\s*{([^}]*)}/i);
if (!box || !/margin\\s*:\\s*1rem\\s*;/i.test(box[1])) {
  throw new Error("Add margin: 1rem; to .box.");
}`,
      hint: "margin: 1rem; — one value applies to all four sides.",
    },
  ],
});

writeChallenge("css-box-model", {
  id: "space-the-card",
  title: "Modify: Space the Card",
  prompt: "The `.card` is cramped. Without changing its width or border:\n\n- Give the card `padding: 1.5rem` (breathing room *inside*).\n- Give it `margin: 0 auto 1.5rem` — centered horizontally (the `auto` does it), with bottom margin for the next section.\n- Give it a `border-radius` of `8px`.",
  difficulty: "beginner",
  boilerplate: "<style>\n  *, *::before, *::after { box-sizing: border-box; }\n\n  .card {\n    width: 400px;\n    border: 1px solid silver;\n  }\n</style>\n\n<div class=\"card\">\n  <h3>Club membership</h3>\n  <p>Everything a member needs, one flat rate.</p>\n</div>\n",
  tests: [
    {
      name: "padding added",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card || !/padding\\s*:\\s*1\\.5rem\\s*;/i.test(card[1])) {
  throw new Error("Give .card padding: 1.5rem;");
}`,
      hint: "padding sits between content and border — inside the box.",
    },
    {
      name: "centered with bottom margin",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card || !/margin\\s*:\\s*0\\s+auto\\s+1\\.5rem\\s*;/i.test(card[1])) {
  throw new Error("Set margin: 0 auto 1.5rem; on .card (top 0, sides auto, bottom 1.5rem).");
}`,
      hint: "auto horizontal margins + a definite width = centered block.",
    },
    {
      name: "rounded corners",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card || !/border-radius\\s*:\\s*8px\\s*;/i.test(card[1])) {
  throw new Error("Add border-radius: 8px;");
}`,
      hint: "border-radius rounds the box's corners.",
    },
    {
      name: "width and border untouched",
      code: `const card = code.match(/\\.card\\s*{([^}]*)}/i);
if (!card || !/width\\s*:\\s*400px/i.test(card[1]) || !/border\\s*:\\s*1px/i.test(card[1])) {
  throw new Error("Do not change the original width or border.");
}`,
      hint: "Modification challenges change only what the brief asks for.",
    },
  ],
});
