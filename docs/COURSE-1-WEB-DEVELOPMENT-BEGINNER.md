# Course 1 — Web Development — Beginner

**Source of truth for Course 1** · Phase 10 (Course 1 revision: Learn/Practice separation + practice expansion) · 2026-09-05
Implemented as the course `web-development-beginner` in track `web-development`
(`src/content/tracks/web-development/`). The former 5-lesson `web-development-foundations`
course is absorbed: module/lesson/challenge ids and all existing challenges are preserved, so
existing progress events, achievements, discussions, and E2E anchors keep working.

**Revision basis (learner feedback from the live private beta):** the original course had too
much theory relative to hands-on coding. This revision (a) separates **Learn** and **Practice**
into distinct first-class experiences, (b) interleaves practice sets directly after the lessons
that teach the concept, (c) migrates **every** lesson-attached coding challenge into the practice
layer (lessons are pure theory; checkpoints keep their understanding checks), and (d) expands the
course from 51 to **91 challenges** (+40 practice challenges, 16 near-duplicates culled), taking
it from ~13 h to ~21 h with the majority of new time spent coding.

## Identity

| Field          | Value                                                                                                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------- || Track / course | `web-development` / `web-development-beginner`                                                                             |
| Title          | Web Development — Beginner (the beginner level of the Web Development path; Intermediate/Advanced/Professional are future courses, not created here) |
| Audience       | Complete beginners — no coding, no Git, no terminal experience assumed                                                     |
| Outcome        | Build and deploy a responsive, interactive, accessible website; explain how the web works; independently continue learning |
| Prerequisites  | None. A computer with a modern browser. (Node.js/Git needed only for Module 5+, with install links provided.)              |
| Estimated time | ~21 hours total: 12.8 h lessons + 8.0 h practice sets (excl. projects/checkpoints)                                         |
| Difficulty     | beginner → intermediate (functions/data-structures onward)                                                                 |

## Modules

| #   | Module                                                                                                                                         | Lessons       | Checkpoint/Project                                              | Level |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | --------------------------------------------------------------- | ----- |
| 1   | `the-web-and-your-first-website` — internet vs web, browser/server, URLs, HTML/CSS/JS roles, DevTools, first page                              | 4             | Project: First Personal Web Page                                | L1    |
| 2   | `html-foundations` — elements, attributes, links, images, lists/tables, semantics, forms, a11y                                                 | 10 (5 ported) | Project: Personal Profile; Checkpoint: HTML Understanding Check | L1–2  |
| 3   | `css-foundations` — syntax, selectors/cascade, units, typography, box model, display, positioning, Flexbox, Grid, responsive, transitions      | 12            | Checkpoint: CSS Understanding Check                             | L2    |
| 4   | `javascript-foundations` — variables, control flow, functions, arrays, objects, DOM, events, forms+validation, localStorage, async, fetch/APIs | 18            | Checkpoints: JS Fundamentals; Project: Interactive Web App      | L2–3  |
| 5   | `developer-tools-git-and-github` — terminal, Git, branching, GitHub, Pages deploy                                                              | 6             | Checkpoint: Git; Project: Publish a Website                     | L3–4  |
| 6   | `how-modern-websites-work` — frontend/backend, HTTP, databases/auth concepts, deployment/DNS/HTTPS                                             | 4             | — (conceptual)                                                  | L4    |
| 7   | `final-project` — planning + capstone                                                                                                          | 2             | Project: Portfolio/Business Website                             | L5    |

**Totals: 7 modules · 56 lessons · 91 challenges (88 practice + 3 checkpoint) · 52 practice sets · 6 projects · 4 checkpoints.**

## Learn / Practice architecture (revision core)

- **Learn** = lessons (unchanged content type, URLs, and MDX bodies).
- **Practice** = a new first-class content type, the **practice set**: module-level sibling of
  lessons, stored at `modules/<module>/practices/<set>.json` plus a `challenges/` directory.
  Each set declares `afterLesson` (the lesson it follows in the module flow), `minutes`,
  `difficulty`, and its ordered `challenges`.
- The course page renders the **interleaved flow**: Lesson → Practice → Lesson → Practice → …
  with a persistent visual distinction (Learn vs Practice vs Project badges).
- Lesson pages surface a callout to the practice set anchored after them; practice hubs are
  dedicated pages (`/learn/<track>/<course>/<module>/practice/<set>`) that state the concept,
  difficulty, per-challenge level (deliberate-practice levels below), and set progress.
- Practice challenge URLs are `/learn/<track>/<course>/<module>/practice/<set>/<challenge>`
  (7 segments — see route note in the challenge page source for why there is no `challenge/`
  segment: an 8-segment dynamic route overflows in Next 16.3.4 Turbopack dev).
- **Progress semantics:** passing every challenge of a set anchored after a lesson is required
  for that lesson's completion; practice passes are recorded as `challenge` progress events
  (existing schema — no progress-data migration) and shown on the dashboard.

### Deliberate-practice levels (every practice challenge is tagged)

| Level        | Meaning                                              | Count |
| ------------ | ---------------------------------------------------- | ----- |
| imitation    | apply the exact concept just taught                  | 16    |
| guided       | partial scaffolding provided                         | 15    |
| independent  | requirements only; learner decides implementation    | 9     |
| combination  | combine multiple recently learned concepts           | 2     |
| debugging    | fix broken code (broken-code-first challenges)       | 8     |
| real-world   | realistic mini-task with acceptance criteria         | 2     |
| mini-build   | build a small component/page                         | 4     |

Each practice set is ordered as a climb through these levels (imitation → … → mini-build),
never as N repetitions of the same difficulty.

## Progression model (L1→L5)

1. **Absolute beginner** — read/understand the web, write first tags (M1).
2. **Beginner** — build real content and style it; mobile-first responsive (M2–M3).
3. **Developing** — program behavior: JS fundamentals → DOM → events → data → APIs (M4).
4. **Independent beginner** — professional tooling and mental architecture (M5–M6).
5. **Capstone** — an unguided, requirements-driven build with meaningful decisions (M7).

## Learning outcomes (validated against the implemented curriculum)

Learners finishing this course can:

- explain how the web works at a beginner level (M1, M6)
- write semantic, accessible HTML including forms (M2 + HTML checkpoint)
- style pages with modern CSS: cascade, box model, Flexbox, Grid, responsive, transitions (M3 + CSS checkpoint)
- write modern JavaScript: variables, control flow, functions, arrays, objects (M4 + JS checkpoint)
- manipulate the DOM and handle events; validate forms with feedback (M4)
- persist state with localStorage; call APIs with fetch/async-await and handle loading/errors (M4)
- use terminal, Git, GitHub, and deploy via GitHub Pages (M5 + Git checkpoint)
- describe frontend/backend/HTTP/database/deployment architecture (M6)
- independently plan, build, and ship a complete responsive website (M7)

## Challenge design rules (binding for every challenge in this course)

1. Tests verify the **requirement's behavior/structure**, never one exact authored string.
2. Freeform personal content uses generous assertions (existence/plurality, not exact text).
3. Mix of challenge types per module: guided, independent, modification, prediction, debugging — **and when a concept can be practiced through code, a coding challenge is preferred over a multiple-choice check**.
4. Every test has an educational `hint` (what/why, not just what failed); failed runs point the learner at the requirement they missed without revealing the solution.
5. Checkpoints: one multi-part challenge combining concept-checks, prediction, and a build task.
6. JS challenges may execute the learner's `code` with `new Function` and assert behavior;
   HTML/CSS challenges assert structure with deliberately generous parsing.
7. Difficulty tags follow the progression model; `intermediate` starts at JS functions.

## Deliberate exclusions

Frameworks, TypeScript, Tailwind, npm tooling, backend implementation, databases, auth
implementation — see the research doc §5. Exclusions are stated to learners in Module 1 and
Module 6 ("where to go next") so the boundary is explicit, not hidden.

## Content conventions

- Lesson body: MDX, `## heading` sections, fenced code blocks, "What you learned" recap,
  no marketing language, no filler, purpose-first explanations.
- Every lesson JSON: `minutes` 5–15, `difficulty` per progression, description ≤ 400 chars.
- Practice set JSON: `afterLesson` anchor, `minutes`, `difficulty`, ordered `challenges`;
  every practice challenge JSON carries a `level` (deliberate-practice levels above).
- MDX files are imported in `src/lib/curriculum/mdx-map.ts` keyed `<moduleId>/<lessonId>.mdx`
  (map is auto-generated by `scripts/generate-mdx-map.mjs`).

## QA gates (binding)

- `node scripts/content-authoring/verify-challenges.mjs` — executes every challenge test
  against a reference solution (must pass) and a meaningful wrong solution (must fail).
  Currently **91/91 verified** (88 practice + 3 checkpoint).
- `npx tsx scripts/content-authoring/validate-content.ts` — curriculum integrity: unique ids,
  valid lesson↔practice references, no orphaned/unreachable content, every practice challenge
  level-tagged. Must print `Integrity: OK`.
- `tests/unit/curriculum-practices.test.ts` — interleave ordering, anchored-practice lookup,
  practice challenge resolution, level coverage.
- `tests/e2e/practice-flow.spec.ts` — practice hub (concept/difficulty/levels/progress),
  full run→verdict flow on a practice challenge, wrong-solution hint quality, mobile (390px),
  keyboard operability.

## Before/after (revision metrics)

| Metric                 | Before (Phase 8) | After (Phase 10)        |
| ---------------------- | ---------------- | ----------------------- |
| Modules                | 7                | 7                       |
| Lessons                | 56               | 56                      |
| Challenges             | 51               | **91** (88 practice + 3 checkpoint) |
| Practice sets          | 0 (implicit)     | **52**                  |
| Estimated theory time  | ~12.8 h          | ~12.8 h                 |
| Estimated practice time| ~4 h (challenges inside lessons) | ~16.8 h (8.0 h practice sets + checkpoint/project challenges) |
| Total estimated time   | ~13 h            | **~21 h**               |
| Lessons with zero coding after them | 9 | 0 — every lesson is followed by practice |
