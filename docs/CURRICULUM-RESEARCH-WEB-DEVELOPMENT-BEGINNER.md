# Curriculum Research — Web Development Beginner

**Internal research document** · Phase 8 · 2026-09-04
**Purpose:** evidence base for the first complete Code Journey course. Sources are surveyed for
structure and pedagogy; **no lesson text is copied** — all Code Journey content is original.

## 1. Sources researched

| Source                                                                                                          | What was examined                                                                                                                                                                       | Use                  |
| --------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| freeCodeCamp — Responsive Web Design (v9) curriculum + legacy (2022)                                            | Module ordering, project cadence, semantic-HTML/forms emphasis                                                                                                                          | Structure & scope    |
| The Odin Project — Foundations course                                                                           | Section order (Intro → Git Basics → HTML → CSS → Flexbox → JS Basics), project-per-section cadence, "set up real tools early" philosophy                                                | Structure & ordering |
| MDN Learn Web Development / MDN Curriculum                                                                      | "Getting started with the web" → HTML → CSS ("first steps, styling the box, styling text, layout") → JS ("first steps, building blocks, DOM…") progression; depth calibration per topic | Ordering & depth     |
| W3C WAI — Introduction to Web Accessibility; WCAG 2.1 (perceivable/operable/understandable/robust); Easy Checks | A11y framing as fundamentals-not-bonus; the beginner-teachable core: alt text, labels, headings, contrast, keyboard                                                                     | A11y thread design   |
| web.dev (Learn)                                                                                                 | Responsive/modern-CSS presentation, mobile-first framing                                                                                                                                | Responsive thread    |
| Learner retrospectives surfaced in search (fCC forum, r/webdev, r/FreeCodeCamp)                                 | Where beginners report getting stuck                                                                                                                                                    | Friction avoidance   |

## 2. Major curriculum patterns discovered

1. **Web-first orientation before syntax.** Every respected curriculum opens with "how the web
   works" (browser/server, URLs, HTTP) and a tiny first page — learners need a mental model to
   attach syntax to (MDN "Getting started", Odin "Introduction").
2. **HTML → CSS → JS sequencing is universal.** Content → presentation → behavior. JS is always
   third; DOM/events come after language fundamentals, not before.
3. **Projects are the spine.** fCC and Odin both punctuate each section with a project; the
   project is where knowledge consolidates. Odin places projects at the end of each section.
4. **Git/tooling appears early (Odin) or late (fCC/MDN).** Evidence from beginner
   retrospectives: terminal + Git on day one is a common abandonment point. **Decision:** teach
   terminal + Git _after_ the learner has built real pages (they now have something worth
   version-controlling), before the final project.
5. **Semantic HTML and accessibility are core, not appendix** (fCC v9 makes semantic HTML,
   forms, and a11y explicit; WAI treats them as fundamentals).
6. **Layout: Flexbox then Grid** (fCC, Odin, web.dev) — flex for 1-D problems first, grid for
   2-D after the box model and display are solid.
7. **Forms get their own treatment** — the learner's first genuinely stateful,
   accessibility-sensitive UI (labels, error states, keyboard).
8. **APIs/fetch close the beginner arc** — after promises/async, fetch + JSON is the bridge to
   "real" web apps.

## 3. Common beginner problems (and our mitigations)

| Problem                                           | Mitigation in this course                                                                                |
| ------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Tutorial hell — following along without retention | Short lessons (5–15 min), 1–2 graded challenges per lesson, challenges verify behavior not exact strings |
| Cascade/specificity confusion                     | Dedicated lesson + a debugging challenge where a rule silently loses                                     |
| Box-model size surprises                          | Dedicated lesson with a prediction challenge (content-box math)                                          |
| Positioning confusion                             | One lesson, honest guidance (use layout systems; reserve absolute for overlays/tooltips)                 |
| `this`/scope in JS                                | Scope taught with functions early; arrow functions deferred until after named functions                  |
| Event-object overwhelm                            | Only the events learners need first (click/input/submit/keydown), `preventDefault` introduced at forms   |
| Regex/framework shortcuts in graders              | Challenge tests accept any valid implementation of the requirement                                       |

## 4. Recommended topic ordering (and why)

**Orientation → HTML → CSS → JS → DOM/events/forms → storage/APIs → tooling (terminal/Git/GitHub) → architecture → final project.**

- Orientation first: mental model + first page = motivation (all sources).
- HTML before CSS before JS: universal; dependencies are strict.
- Checkpoints after HTML, CSS, JS fundamentals, DOM/events, and Git: fCC/Odin section reviews map
  to "understanding checks"; on Code Journey these are graded challenge-lessons.
- Terminal/Git after real pages exist: preserves early momentum while still landing tooling
  before the capstone (splits the Odin-early/fCC-late disagreement using learner evidence).
- Modern-web-architecture as a _conceptual_ module before the final project: the learner deploys
  via GitHub Pages in the tooling module and can then name the moving parts they just used.

## 5. Topics intentionally excluded (beginner scope)

- **Frameworks** (React/Next/Vue), **TypeScript**, **Tailwind**, **npm/bundler tooling** —
  future courses; fundamentals before abstraction (phase directive).
- **Backend implementation, databases, auth implementation** — conceptual architecture only.
- **CSS pre-processors, container queries, view transitions** — post-beginner.
- **JS classes/prototype deep-dive; closures beyond a mention** — post-beginner.
- **npm dependency workflows** — one conceptual mention; not operational.

## 6. Pedagogical decisions

1. **Explain → show → practice, per lesson.** Each lesson: why it matters → concept → examples
   → 1–2 auto-graded challenges (guided, independent, modification, prediction, or debug types).
2. **Challenge variety mandated** (phase directive §10): every module mixes guided,
   independent, modification, prediction, and debugging challenges.
3. **Accept any valid implementation.** Tests verify the _behavior/structure of the
   requirement_, never one exact authored string — with deliberately generous assertions on
   freeform content.
4. **A11y woven in, checkpointed once.** Alt text at images, link text at links, labels at
   forms, heading hierarchy at structure, contrast in CSS, then an a11y-focused challenge set at
   the HTML checkpoint and in the final project requirements.
5. **Responsive woven in from CSS onward**, with a dedicated responsive module before JS.
6. **Checkpoints = lessons with one graded multi-part challenge** — flows through the existing
   server-verified progress path (challenge verdict → progress event) with zero platform changes.
7. **Difficulty progression L1→L5** (§14): `beginner` tags through Module 4's midpoint,
   `intermediate` from functions/data-structures through the capstone.
8. **Real-world context rule** (§16): every construct is introduced with its _purpose_ — labels
   exist for assistive tech, flexbox exists for nav bars, etc.

## 7. Code Journey differentiation

- **Auto-graded from lesson one** — practice is verified by real execution, not quizzes.
- **Test-verified projects** — module projects are challenges with structural tests, so "done"
  means verified, not self-assessed.
- **Hint-ladder mentor** (existing platform behavior) aligned to the anti-solution-dump policy.
- **Original content, purpose-first explanations, no filler** (phase directives §20–21).

## 8. Technical standards taught

Semantic HTML5, modern CSS (custom properties, logical flow, Flexbox/Grid, media queries,
`prefers-reduced-motion`), modern JS (const/let, arrow functions, template literals, fetch +
async/await), browser DevTools, Git + GitHub + GitHub Pages.

**Sources cited:** freeCodeCamp RWD curriculum (freecodecamp.org/learn); The Odin Project
Foundations (theodinproject.com/paths/foundations); MDN Learn Web Development
(developer.mozilla.org/en-US/docs/Learn); W3C WAI Introduction to Web Accessibility + WCAG 2.1
(w3.org/WAI, w3.org/TR/WCAG21); web.dev Learn.
