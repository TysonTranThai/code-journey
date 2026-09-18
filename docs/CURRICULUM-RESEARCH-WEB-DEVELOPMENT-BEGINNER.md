# Curriculum Research — Web Development Beginner

**Internal research document** · Phase 8 (2026-09-04) · **revised Phase 10 (2026-09-05): Learn/Practice separation + practice density**
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

---

## 9. Revision research (Phase 10): practice density, deliberate practice, and Learn/Practice separation

**Trigger:** live private-beta learner feedback — "too much theory, not enough hands-on coding".
The original course averaged ~0.9 challenges per lesson and left 9 lessons with **zero** coding
after them; learners read for long stretches before writing code.

### 9.1 What the evidence says

- **Deliberate practice beats re-reading** (Ericsson et al. 1993; *Make It Stick*, Brown/Roediger/McDaniel 2014):
  skill grows from repeatedly _retrieving and applying_ a specific skill just beyond comfort, with
  immediate feedback — exactly what an auto-graded, hint-supported coding challenge provides.
- **Testing/retrieval effect**: actively producing code (recall + construction) produces far better
  retention than re-watching or re-reading examples. Auto-graded practice converts every concept
  into a retrieval event.
- **Spacing + interleaving within a skill**: practice is most effective when it follows the
  concept _immediately_ (micro-practice), then recurs later at higher difficulty (climb), rather
  than being batched at a module's end.
- **Cognitive load theory (Sweller)**: worked examples help novices, but the worked-example effect
  fades — learners must move to problem-solving quickly. This supports the
  **imitation → guided → independent → combination** climb inside each practice set: scaffold
  early, remove it deliberately, then require synthesis and transfer (debugging, real-world,
  mini-build).
- **Project-based learning anchoring**: curated practice that directly precedes a project
  (the same constructs the project needs) measurably improves project completion for novices —
  the origin of our "project preparation" sets before each project.
- **Benchmark curricula in practice**: fCC's RWD cert has ~70+ coding steps for ~30 hours of
  content; The Odin Project intersperses exercises throughout rather than at section ends; Exercism
  and Codecademy structure learning as concept → small exercise → larger exercise. The consistent
  shape is **concept → tiny practice**, not **concept-block → practice-block**.

### 9.2 Information-architecture decision

Three candidate models were evaluated against the existing architecture (track → course → module
→ lesson → challenges, zod-validated, progress events typed by content kind):

1. *Practice section per module* (all practice at module end) — rejected: separates concept from
   practice by hours of reading; contradicts micro-practice evidence.
2. *Challenges bolted onto lessons* (status quo) — rejected: practice is invisible in the IA and
   UX; learners perceive it as "the bottom of a lesson", and it cannot carry its own difficulty
   arc or progress display.
3. **Practice set as a first-class content type, interleaved via `afterLesson` anchors** (chosen):
   module flow renders Lesson → Practice → Lesson → Practice, practice gets dedicated pages,
   difficulty levels, and progress, and lessons stay pure theory. It reuses the existing
   challenge-execution/progress machinery (no second grading system) and keeps all 51 original
   lesson challenges and URLs intact.

### 9.3 Difficulty model (deliberate-practice levels)

The seven levels (imitation, guided, independent, combination, real-world, debugging, mini-build)
operationalize the scaffold-fading sequence above; every practice set is ordered as a climb.
Distribution shipped in this revision: 52 guided · 10 imitation · 10 debugging · 7 independent ·
6 mini-build · 2 real-world · 1 combination (88 practice challenges). Debugging is treated as
first-class practice per the learner-feedback directive: beginners should practice _fixing_ code,
not only writing it.

### 9.4 Practice-density outcome (rationale for 91 challenges)

Target range from the phase directive was 100–150 meaningful challenges, to be set by research,
not a quota. The revision lands at **91** (3 checkpoint challenges stay lesson-attached; 88
practice challenges across 52 sets, including the 48 original lesson challenges migrated into
their lesson's practice set): every lesson is now followed by coding practice (was: 9 lessons with
none), every set climbs the level model, and 16 near-duplicate challenges that the interim
expansion added on top of migrated ones were culled — each remaining challenge has a distinct
retrieval target, no "create h1…h6" padding. Estimated learner time rises from ~13 h to ~21 h with
essentially all of the increase spent coding.
