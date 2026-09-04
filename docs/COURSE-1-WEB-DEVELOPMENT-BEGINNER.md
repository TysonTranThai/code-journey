# Course 1 — Web Development Beginner

**Source of truth for Course 1** · Phase 8 · 2026-09-04
Implemented as the course `web-development-beginner` in track `web-development`
(`src/content/tracks/web-development/`). The former 5-lesson `web-development-foundations`
course is absorbed: module/lesson/challenge ids and all existing challenges are preserved, so
existing progress events, achievements, discussions, and E2E anchors keep working.

## Identity

| Field | Value |
|---|---|
| Track / course | `web-development` / `web-development-beginner` |
| Title | Web Development Beginner |
| Audience | Complete beginners — no coding, no Git, no terminal experience assumed |
| Outcome | Build and deploy a responsive, interactive, accessible website; explain how the web works; independently continue learning |
| Prerequisites | None. A computer with a modern browser. (Node.js/Git needed only for Module 5+, with install links provided.) |
| Estimated time | ~25–30 hours (54 lessons × 8–12 min + practice + projects) |
| Difficulty | beginner → intermediate (functions/data-structures onward) |

## Modules

| # | Module | Lessons | Checkpoint/Project | Level |
|---|---|---|---|---|
| 1 | `the-web-and-your-first-website` — internet vs web, browser/server, URLs, HTML/CSS/JS roles, DevTools, first page | 4 | Project: First Personal Web Page | L1 |
| 2 | `html-foundations` — elements, attributes, links, images, lists/tables, semantics, forms, a11y | 9 (5 ported) | Checkpoint: HTML Understanding Check | L1–2 |
| 3 | `css-foundations` — syntax, selectors/cascade, units, typography, box model, display, positioning, Flexbox, Grid, responsive, transitions | 12 | Checkpoint: CSS Understanding Check | L2 |
| 4 | `javascript-foundations` — variables, control flow, functions, arrays, objects, DOM, events, forms+validation, localStorage, async, fetch/APIs | 17 | Checkpoints: JS Fundamentals; Project: Interactive Web App | L2–3 |
| 5 | `developer-tools-git-and-github` — terminal, Git, branching, GitHub, Pages deploy | 6 | Checkpoint: Git; Project: Publish a Website | L3–4 |
| 6 | `how-modern-websites-work` — frontend/backend, HTTP, databases/auth concepts, deployment/DNS/HTTPS | 4 | — (conceptual) | L4 |
| 7 | `final-project` — planning + capstone | 2 | Project: Portfolio/Business Website | L5 |

**Totals: 7 modules · 54 lessons · ~70 challenges · 6 projects · 4 checkpoints.**

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
3. Mix of challenge types per module: guided, independent, modification, prediction, debugging.
4. Every test has an educational `hint` (what/why, not just what failed).
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
- MDX files are imported in `src/lib/curriculum/mdx-map.ts` keyed `<moduleId>/<lessonId>.mdx`
  (map is auto-generated by `scripts/generate-mdx-map.mjs`).
