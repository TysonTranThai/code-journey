/**
 * Author CSS practice content part 2 (Course 1 revision, wave 2).
 * Same contract as author-css-practices.mjs: writes set+challenge JSON,
 * appends solutions to practice-solutions.mjs, verifies immediately.
 *
 * Run: node scripts/content-authoring/author-css-practices-2.mjs
 */
import { mkdirSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import path from "node:path";
import vm from "node:vm";

const BASE =
  "src/content/tracks/web-development/courses/web-development-beginner/modules/css-foundations/practices";
const SOLUTIONS_FILE = "scripts/content-authoring/practice-solutions.mjs";
const P = (id) => path.join(BASE, id, "challenges");

const SETS = [
  {
    file: "css-flexbox-practice.json",
    id: "css-flexbox-practice",
    title: "Flexbox Layout Drills",
    description:
      "Flex containers in the wild: a centered card, a spaced navbar, and a card row that wraps — the three layouts you will build most often.",
    afterLesson: "css-flexbox",
    minutes: 16,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-flex-center-card",
        title: "Center a Card Perfectly",
        prompt: `Make \`.stage\` a flex container that centers \`.card\` both horizontally and vertically, and give \`.stage\` a \`min-height: 100vh\` so centering has room.

Rules:
- \`display: flex\`, \`justify-content: center\`, \`align-items: center\` on \`.stage\`.`,
        difficulty: "beginner",
        boilerplate: "<!-- Center the card in the stage -->\n",
        tests: [
          {
            name: "stage is a flex container",
            code: `if (!/\\.stage\\s*\\{[^}]*display\\s*:\\s*flex\\s*;/i.test(code)) throw new Error("Set display: flex on .stage.");`,
            hint: "Flex properties only work on a flex container: display: flex.",
          },
          {
            name: "horizontal centering",
            code: `if (!/\\.stage\\s*\\{[^}]*justify-content\\s*:\\s*center\\s*;/i.test(code)) throw new Error("Center along the main axis with justify-content: center.");`,
            hint: "justify-content: center centers items on the main (horizontal) axis.",
          },
          {
            name: "vertical centering with room to center",
            code: `if (!/\\.stage\\s*\\{[^}]*align-items\\s*:\\s*center\\s*;/i.test(code)) throw new Error("Center the cross axis with align-items: center.");
if (!/\\.stage\\s*\\{[^}]*min-height\\s*:\\s*100vh\\s*;/i.test(code)) throw new Error("Give .stage min-height: 100vh so vertical centering has space.");`,
            hint: "align-items: center handles the vertical axis; min-height: 100vh gives it a stage.",
          },
        ],
      },
      {
        id: "practice-flex-navbar",
        title: "A Spaced-Out Navbar",
        prompt: `Build the classic navbar: \`.nav\` is a flex row with \`justify-content: space-between\` and \`align-items: center\` so the brand sits left and the link list right, vertically centered.

Rules:
- \`.nav\`: flex, space-between, align-items center.
- \`.nav ul\`: also a flex row with \`gap: 1rem\` and \`list-style: none\`.`,
        difficulty: "beginner",
        boilerplate: "<!-- Style the navbar -->\n",
        tests: [
          {
            name: "nav is flex with space-between",
            code: `const nav = code.match(/\\.nav\\s*\\{[^}]*\\}/i)[0];
if (!/display\\s*:\\s*flex\\s*;/i.test(nav)) throw new Error("display: flex on .nav first.");
if (!/justify-content\\s*:\\s*space-between\\s*;/i.test(nav)) throw new Error("Push brand and links apart with justify-content: space-between.");
if (!/align-items\\s*:\\s*center\\s*;/i.test(nav)) throw new Error("Align vertically with align-items: center.");`,
            hint: "Three declarations on .nav: display: flex; justify-content: space-between; align-items: center;",
          },
          {
            name: "the link list is a spaced flex row",
            code: `const ul = code.match(/\\.nav\\s+ul\\s*\\{[^}]*\\}/i);
if (!ul) throw new Error("Add a .nav ul rule.");
if (!/display\\s*:\\s*flex\\s*;/i.test(ul[0])) throw new Error(".nav ul needs display: flex too.");
if (!/gap\\s*:\\s*1rem\\s*;/i.test(ul[0])) throw new Error("Space the links with gap: 1rem.");
if (!/list-style\\s*:\\s*none\\s*;/i.test(ul[0])) throw new Error("Remove the bullets with list-style: none.");`,
            hint: ".nav ul { display: flex; gap: 1rem; list-style: none; }",
          },
          {
            name: "no margin hacks on li",
            code: `if (/\\.nav\\s+li[^{]*\\{[^}]*margin/i.test(code)) {
  throw new Error("No margin hacks on the list items — gap on the flex container does it cleanly.");
}`,
            hint: "Use gap: 1rem on .nav ul instead of margins between items.",
          },
        ],
      },
      {
        id: "practice-flex-card-row",
        title: "Card Row That Wraps",
        prompt: `\`.row\` lays out equal cards that wrap on small screens: \`display: flex\`, \`flex-wrap: wrap\`, \`gap: 1rem\`. Each \`.card\` gets \`flex: 1\` and \`min-width: 200px\` so cards grow but never shrink below 200px — wrapping instead of squashing.

Rules:
- Container: flex + wrap + gap.
- Cards: flex: 1 and min-width: 200px.`,
        difficulty: "beginner",
        boilerplate: "<!-- Flexible card row -->\n",
        tests: [
          {
            name: "container wraps with gap",
            code: `const row = code.match(/\\.row\\s*\\{[^}]*\\}/i)[0];
if (!/display\\s*:\\s*flex\\s*;/i.test(row)) throw new Error(".row needs display: flex.");
if (!/flex-wrap\\s*:\\s*wrap\\s*;/i.test(row)) throw new Error("Allow wrapping with flex-wrap: wrap.");
if (!/gap\\s*:\\s*1rem\\s*;/i.test(row)) throw new Error("Space cards with gap: 1rem.");`,
            hint: ".row { display: flex; flex-wrap: wrap; gap: 1rem; }",
          },
          {
            name: "cards grow but keep a floor",
            code: `const card = code.match(/\\.card\\s*\\{[^}]*\\}/i)[0];
if (!/flex\\s*:\\s*1\\s*;/i.test(card)) throw new Error("Cards share space equally with flex: 1.");
if (!/min-width\\s*:\\s*200px\\s*;/i.test(card)) throw new Error("Set the floor with min-width: 200px.");`,
            hint: ".card { flex: 1; min-width: 200px; } — grow, but never below 200px.",
          },
          {
            name: "no fixed width on cards",
            code: `const card = code.match(/\\.card\\s*\\{[^}]*\\}/i)[0];
if (/(^|[^-])width\\s*:\\s*\\d/i.test(card)) throw new Error("No fixed width — flex: 1 plus min-width handles sizing.");`,
            hint: "Let flexbox size the cards: flex: 1 + min-width, not width.",
          },
        ],
      },
    ],
  },
  {
    file: "css-grid-practice.json",
    id: "css-grid-practice",
    title: "Grid Layout Drills",
    description:
      "Two-dimensional layout: a three-column gallery, a full-width feature spanning the grid, and a responsive auto-fitting grid.",
    afterLesson: "css-grid",
    minutes: 14,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-grid-gallery",
        title: "A Three-Column Gallery",
        prompt: `Make \`.gallery\` a grid with three equal columns and a \`gap: 1rem\`: \`grid-template-columns: repeat(3, 1fr)\`.

Rules:
- \`display: grid\`, three \`1fr\` columns, gap.`,
        difficulty: "beginner",
        boilerplate: "<!-- Grid the gallery -->\n",
        tests: [
          {
            name: "gallery is a grid",
            code: `if (!/\\.gallery\\s*\\{[^}]*display\\s*:\\s*grid\\s*;/i.test(code)) throw new Error("Set display: grid on .gallery.");`,
            hint: "display: grid turns the container into a grid.",
          },
          {
            name: "three equal columns",
            code: `if (!/\\.gallery\\s*\\{[^}]*grid-template-columns\\s*:\\s*repeat\\(\\s*3\\s*,\\s*1fr\\s*\\)\\s*;/i.test(code)) {
  throw new Error("Use grid-template-columns: repeat(3, 1fr) for three equal columns.");
}`,
            hint: "repeat(3, 1fr) is shorthand for three 1fr columns.",
          },
          {
            name: "gap between cells",
            code: `if (!/\\.gallery\\s*\\{[^}]*gap\\s*:\\s*1rem\\s*;/i.test(code)) throw new Error("Add gap: 1rem to .gallery.");`,
            hint: "gap: 1rem spaces both rows and columns.",
          },
        ],
      },
      {
        id: "practice-grid-feature",
        title: "Feature That Spans the Grid",
        prompt: `Starting from the three-column gallery, make \`.featured\` span the entire first row: \`grid-column: 1 / -1\`. The other images keep their normal cells.

Rules:
- \`.gallery\` keeps its grid setup.
- \`.featured\` spans all columns.`,
        difficulty: "beginner",
        boilerplate: `<style>
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
</style>

<div class="gallery">
  <div class="featured">Feature</div>
  <div>Two</div>
  <div>Three</div>
  <div>Four</div>
</div>
`,
        tests: [
          {
            name: "gallery grid survives",
            code: `if (!/\\.gallery\\s*\\{[^}]*display\\s*:\\s*grid\\s*;[^}]*grid-template-columns\\s*:\\s*repeat\\(\\s*3\\s*,\\s*1fr\\s*\\)\\s*;/i.test(code)) {
  throw new Error("Keep .gallery as a three-column grid.");
}`,
            hint: "Don't touch the gallery rule — add a new one for .featured.",
          },
          {
            name: "featured spans every column",
            code: `if (!/\\.featured\\s*\\{[^}]*grid-column\\s*:\\s*1\\s*\\/\\s*-1\\s*;/i.test(code)) {
  throw new Error("Add .featured { grid-column: 1 / -1; } — from the first line to the last.");
}`,
            hint: "grid-column: 1 / -1 means 'start at line 1, end at the last line'.",
          },
        ],
      },
      {
        id: "practice-grid-auto-fit",
        title: "Grid That Fits Itself",
        prompt: `Replace fixed column counts with the responsive one-liner: \`.gallery\` uses \`grid-template-columns: repeat(auto-fit, minmax(180px, 1fr))\` — as many 180px-minimum columns as fit, each sharing space equally.

Rules:
- Keep \`display: grid\` and \`gap: 1rem\`.
- Swap the template to the auto-fit form.`,
        difficulty: "beginner",
        boilerplate: `<style>
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
</style>
`,
        tests: [
          {
            name: "auto-fit with a 180px minimum",
            code: `if (!/\\.gallery\\s*\\{[^}]*grid-template-columns\\s*:\\s*repeat\\(\\s*auto-fit\\s*,\\s*minmax\\(\\s*180px\\s*,\\s*1fr\\s*\\)\\s*\\)\\s*;/i.test(code)) {
  throw new Error("Use grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));");
}`,
            hint: "repeat(auto-fit, minmax(180px, 1fr)) — columns appear only when they fit.",
          },
          {
            name: "grid and gap survive",
            code: `if (!/\\.gallery\\s*\\{[^}]*display\\s*:\\s*grid\\s*;/i.test(code)) throw new Error("Keep display: grid.");
if (!/\\.gallery\\s*\\{[^}]*gap\\s*:\\s*1rem\\s*;/i.test(code)) throw new Error("Keep gap: 1rem.");`,
            hint: "Only the grid-template-columns line changes.",
          },
          {
            name: "no media query needed",
            code: `if (/@media/i.test(code)) {
  throw new Error("No media query required — auto-fit handles the responsiveness inside the grid itself.");
}`,
            hint: "The whole point of auto-fit: responsiveness without media queries.",
          },
        ],
      },
    ],
  },
  {
    file: "css-responsive-practice.json",
    id: "css-responsive-practice",
    title: "Responsive Building Blocks",
    description:
      "Mobile-first media queries: one column by default, two from 640px, three from 1024px — plus fluid images that never overflow.",
    afterLesson: "css-responsive",
    minutes: 16,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-responsive-columns",
        title: "One, Two, Three Columns",
        prompt: `\`.cards\` is a single-column grid by default. Write TWO min-width media queries — \`@media (min-width: 640px)\` to make it two columns, and \`@media (min-width: 1024px)\` for three. (That's mobile-first: base styles are the phone styles.)

Rules:
- Base: \`grid-template-columns: 1fr\`.
- 640px: two columns; 1024px: three. Nothing inside a max-width query.`,
        difficulty: "beginner",
        boilerplate: `<style>
.cards {
  display: grid;
  gap: 1rem;
}
/* add the base template + your media queries */
</style>
`,
        tests: [
          {
            name: "single column by default",
            code: `if (!/\\.cards\\s*\\{[^}]*grid-template-columns\\s*:\\s*1fr\\s*;/i.test(code)) {
  throw new Error("The base .cards rule needs grid-template-columns: 1fr (the phone layout).");
}`,
            hint: "Mobile-first: the un-media-queried rule is the small-screen layout — one column.",
          },
          {
            name: "two columns from 640px",
            code: `const q1 = code.match(/@media\\s*\\(\\s*min-width\\s*:\\s*640px\\s*\\)\\s*\\{[\\s\\S]*?\\n?\\}/i);
if (!q1 || !/grid-template-columns\\s*:\\s*repeat\\(\\s*2\\s*,\\s*1fr\\s*\\)/i.test(q1[0])) {
  throw new Error("Add @media (min-width: 640px) { .cards { grid-template-columns: repeat(2, 1fr); } }");
}`,
            hint: "@media (min-width: 640px) containing .cards { grid-template-columns: repeat(2, 1fr); }",
          },
          {
            name: "three columns from 1024px",
            code: `const q2 = code.match(/@media\\s*\\(\\s*min-width\\s*:\\s*1024px\\s*\\)\\s*\\{[\\s\\S]*?\\n?\\}/i);
if (!q2 || !/grid-template-columns\\s*:\\s*repeat\\(\\s*3\\s*,\\s*1fr\\s*\\)/i.test(q2[0])) {
  throw new Error("Add @media (min-width: 1024px) { .cards { grid-template-columns: repeat(3, 1fr); } }");
}`,
            hint: "@media (min-width: 1024px) containing .cards { grid-template-columns: repeat(3, 1fr); }",
          },
          {
            name: "mobile-first (no max-width queries)",
            code: `if (/max-width\\s*:/i.test(code)) {
  throw new Error("Found a max-width query — this exercise is mobile-first: min-width only.");
}`,
            hint: "Mobile-first means min-width queries; leave max-width behind for now.",
          },
        ],
      },
      {
        id: "practice-fluid-images",
        title: "Images That Never Overflow",
        prompt: `Two declarations make images behave on every screen. Add to \`img\`: \`max-width: 100%\` (never wider than its container) and \`height: auto\` (keep proportions while shrinking).

Rules:
- Both declarations on a plain \`img\` element selector.`,
        difficulty: "beginner",
        boilerplate: "<!-- Fluid images -->\n",
        tests: [
          {
            name: "images cap at container width",
            code: `if (!/img\\s*\\{[^}]*max-width\\s*:\\s*100%\\s*;/i.test(code)) throw new Error("Add max-width: 100% to img.");`,
            hint: "img { max-width: 100%; } — an image can shrink, never overflow.",
          },
          {
            name: "proportions preserved",
            code: `if (!/img\\s*\\{[^}]*height\\s*:\\s*auto\\s*;/i.test(code)) throw new Error("Add height: auto to img so images don't squish.");`,
            hint: "img { height: auto; } keeps the aspect ratio while the width shrinks.",
          },
        ],
      },
    ],
  },
  {
    file: "css-typography-practice.json",
    id: "css-typography-practice",
    title: "Type That Reads Well",
    description:
      "Readable body text and a clear hierarchy: font stack, line length and line height, then a scale from h1 to small text.",
    afterLesson: "css-typography",
    minutes: 12,
    difficulty: "beginner",
    challenges: [
      {
        id: "practice-readable-body",
        title: "Make the Page Comfortable to Read",
        prompt: `Set \`body\` to a friendly reading setup: \`font-family: Georgia, "Times New Roman", serif\`, \`line-height: 1.6\`, and \`max-width: 60ch\` with \`margin-inline: auto\` on the content wrapper (apply the max-width + centering to \`main\`).

Rules:
- body: font-family + line-height.
- main: max-width 60ch, centered with margin-inline: auto.`,
        difficulty: "beginner",
        boilerplate: "<!-- Comfortable reading -->\n",
        tests: [
          {
            name: "serif stack with fallbacks",
            code: `if (!/body\\s*\\{[^}]*font-family\\s*:\\s*Georgia\\s*,\\s*"Times New Roman"\\s*,\\s*serif\\s*;/i.test(code)) {
  throw new Error("body { font-family: Georgia, \\"Times New Roman\\", serif; } — always end with a generic family.");
}`,
            hint: "List Georgia first, then the fallback, ending in the generic serif.",
          },
          {
            name: "breathing line height",
            code: `if (!/body\\s*\\{[^}]*line-height\\s*:\\s*1\\.6\\s*;/i.test(code)) throw new Error("Add line-height: 1.6 to body.");`,
            hint: "line-height: 1.6 — generous but not airy.",
          },
          {
            name: "measure capped and centered",
            code: `const main = code.match(/main\\s*\\{[^}]*\\}/i);
if (!main) throw new Error("Add a main rule.");
if (!/max-width\\s*:\\s*60ch\\s*;/i.test(main[0])) throw new Error("Cap the line length with max-width: 60ch.");
if (!/margin-inline\\s*:\\s*auto\\s*;/i.test(main[0])) throw new Error("Center it with margin-inline: auto.");`,
            hint: "main { max-width: 60ch; margin-inline: auto; } — 60 characters per line, centered.",
          },
        ],
      },
      {
        id: "practice-type-scale",
        title: "A Clear Type Scale",
        prompt: `Give the page hierarchy: \`h1 { font-size: 2.5rem; }\`, \`h2 { font-size: 1.5rem; }\`, and \`.small { font-size: 0.875rem; }\`. Nothing else changes size.

Rules:
- Exactly those three rules (plus the font sizes given).`,
        difficulty: "beginner",
        boilerplate: "<!-- Type scale -->\n",
        tests: [
          {
            name: "h1 at 2.5rem",
            code: `if (!/h1\\s*\\{[^}]*font-size\\s*:\\s*2\\.5rem\\s*;/i.test(code)) throw new Error("h1 { font-size: 2.5rem; }");`,
            hint: "h1 { font-size: 2.5rem; }",
          },
          {
            name: "h2 at 1.5rem",
            code: `if (!/h2\\s*\\{[^}]*font-size\\s*:\\s*1\\.5rem\\s*;/i.test(code)) throw new Error("h2 { font-size: 1.5rem; }");`,
            hint: "h2 { font-size: 1.5rem; }",
          },
          {
            name: "small text at 0.875rem",
            code: `if (!/\\.small\\s*\\{[^}]*font-size\\s*:\\s*0\\.875rem\\s*;/i.test(code)) throw new Error(".small { font-size: 0.875rem; }");`,
            hint: ".small { font-size: 0.875rem; } — a class, not an element.",
          },
        ],
      },
    ],
  },
];

const REFS = {
  "practice-flex-center-card": `<style>
.stage {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
</style>`,
  "practice-flex-navbar": `<style>
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav ul {
  display: flex;
  gap: 1rem;
  list-style: none;
}
</style>`,
  "practice-flex-card-row": `<style>
.row {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.card {
  flex: 1;
  min-width: 200px;
}
</style>`,
  "practice-grid-gallery": `<style>
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
</style>`,
  "practice-grid-feature": `<style>
.gallery {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.featured {
  grid-column: 1 / -1;
}
</style>`,
  "practice-grid-auto-fit": `<style>
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
</style>`,
  "practice-responsive-columns": `<style>
.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

@media (min-width: 640px) {
  .cards {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .cards {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>`,
  "practice-fluid-images": `<style>
img {
  max-width: 100%;
  height: auto;
}
</style>`,
  "practice-readable-body": `<style>
body {
  font-family: Georgia, "Times New Roman", serif;
  line-height: 1.6;
}

main {
  max-width: 60ch;
  margin-inline: auto;
}
</style>`,
  "practice-type-scale": `<style>
h1 {
  font-size: 2.5rem;
}

h2 {
  font-size: 1.5rem;
}

.small {
  font-size: 0.875rem;
}
</style>`,
};

const WRONGL = {
  "practice-flex-center-card": ".stage { display: block; }",
  "practice-flex-navbar": ".nav { display: flex; }\n.nav ul { list-style: none; }",
  "practice-flex-card-row": ".row { display: flex; }\n.card { width: 200px; }",
  "practice-grid-gallery": ".gallery { display: flex; gap: 1rem; }",
  "practice-grid-feature":
    ".gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }\n.featured { grid-column: 1 / 2; }",
  "practice-grid-auto-fit":
    ".gallery { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; }",
  "practice-responsive-columns":
    "@media (max-width: 640px) { .cards { grid-template-columns: repeat(2, 1fr); } }",
  "practice-fluid-images": "img { width: 100%; }",
  "practice-readable-body": "body { font-family: Arial; }",
  "practice-type-scale": "h1 { font-size: 12px; }",
};

function runTest(testCode, studentCode) {
  const sandbox = { code: studentCode, result: undefined, setTimeout, clearTimeout };
  const ctx = vm.createContext(sandbox);
  return new vm.Script(
    `(async () => { try { ${testCode}\n result = "PASS"; } catch (err) { result = "FAIL: " + (err && err.message ? err.message : String(err)); } })()`,
  )
    .runInContext(ctx, { awaitPromise: true })
    .then(() => sandbox.result);
}

let appended = 0;
for (const set of SETS) {
  mkdirSync(path.join(BASE, set.id, "challenges"), { recursive: true });
  const setPath = path.join(BASE, set.file);
  if (!existsSync(setPath)) {
    writeFileSync(
      setPath,
      JSON.stringify(
        {
          id: set.id,
          title: set.title,
          description: set.description,
          afterLesson: set.afterLesson,
          minutes: set.minutes,
          difficulty: set.difficulty,
          challenges: set.challenges.map((c) => c.id),
        },
        null,
        2,
      ) + "\n",
    );
  }
  for (const ch of set.challenges) {
    const chPath = path.join(P(set.id), `${ch.id}.json`);
    if (!existsSync(chPath)) {
      writeFileSync(chPath, JSON.stringify(ch, null, 2) + "\n");
    }
    appendFileSync(
      SOLUTIONS_FILE,
      `R[${JSON.stringify(ch.id)}] = ${JSON.stringify(REFS[ch.id])};\nW[${JSON.stringify(ch.id)}] = ${JSON.stringify(WRONGL[ch.id])};\n`,
    );
    appended++;
    const results = [];
    for (const t of ch.tests) results.push(await runTest(t.code, REFS[ch.id]));
    const refOk = results.every((r) => r === "PASS");
    const wrongResults = [];
    for (const t of ch.tests) wrongResults.push(await runTest(t.code, WRONGL[ch.id]));
    const wrongOk = wrongResults.some((r) => r !== "PASS");
    console.log(
      `${refOk && wrongOk ? "OK " : "FAIL"} ${ch.id} [${results.filter((r) => r === "PASS").length}/${results.length}]`,
    );
    if (!refOk)
      results.forEach((r, i) => {
        if (r !== "PASS") console.log(`   ref [${ch.tests[i].name}]: ${r}`);
      });
    if (!wrongOk) console.log(`   wrong solution passed all tests!`);
  }
}
console.log(`appended ${appended} solution pairs`);
