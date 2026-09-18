# Course 3 — Web Development Advanced

**Status:** In development — Section 1 (Advanced HTML) authored 2026-09-12; later sections planned.
**Track:** web-development (after web-development-beginner → web-development-intermediate)
**Predecessor specs:** docs/COURSE-1-WEB-DEVELOPMENT-BEGINNER.md, docs/COURSE-2-WEB-DEVELOPMENT-INTERMEDIATE.md

## Identity

- **Course id:** `web-development-advanced`
- **Title:** Web Development Advanced / **VI:** Lập trình Web — Nâng cao
- **Prerequisites:** `web-development-intermediate` (which itself requires `web-development-beginner`; enforced by the platform's prerequisite chain)
- **Audience:** Engineers who completed Intermediate and want professional-grade control: architecture, accessibility engineering, media, metadata, and security-aware markup.
- **Goal:** move from "I can build applications" to "I can engineer the platform layer: accessible, fast, secure, machine-readable documents — and extend it deliberately."

## Curriculum (Section 1 — Advanced HTML)

Module: `advanced-html` — Advanced HTML / HTML nâng cao

| # | Lesson | Minutes | Practice set |
| --- | --- | --- | --- |
| 1 | html-architecture | 12 | html-architecture-practice (3 challenges, 25 min) |
| 2 | accessible-names | 11 | accessible-names-practice (3 challenges, 25 min) |
| 3 | native-disclosure-dialogs | 11 | native-disclosure-dialogs-practice (3 challenges, 25 min) |
| 4 | popovers-invokers | 10 | popovers-invokers-practice (3 challenges, 25 min) |
| 5 | responsive-media | 11 | responsive-media-practice (3 challenges, 25 min) |
| 6 | sandboxed-embeds-metadata | 11 | sandboxed-embeds-metadata-practice (3 challenges, 25 min) |
| — | docs-hub-project | 20 | docs-hub-project-practice (3 challenges, 25 min) |

**Totals:** 7 lessons · 7 practice sets · 21 challenges · theory ≈ 86 min · practice ≈ 175 min · **≈ 69% hands-on**.

## Learning outcomes

By the end of Section 1, a learner can:

- design heading and landmark architecture for complex documents and audit broken ones;
- compute and assign accessible names correctly (content → alt → aria-label → aria-labelledby) and choose native semantics over ARIA;
- build disclosure patterns with `<details name>` and accessible dialogs with `<dialog>`, `::backdrop`, and autofocus placement;
- decide between dialog, popover, and invoker-command patterns for modern interactive UI (2026 platform: Popover GA 2025, Invoker Commands Baseline 2026);
- implement responsive images (`srcset`/`sizes`, `<picture>` art direction and format fallbacks, `fetchpriority`/`loading`/`decoding`) and accessible video with captions;
- embed third-party content safely (`sandbox` tokens, `allow=` delegation, `title`, `loading="lazy"`);
- write machine-readable metadata: viewport, canonical, robots, Open Graph, hreflang, `lang`/`dir`, `<time>`;
- apply progressive enhancement so interactions work before JavaScript arrives.

## Projects

**Project: Documentation Hub** (Section 1): a knowledge-base article page for an open-source-style tool integrating all six lessons. Graded by decision-verification challenges over the HTML artifact (structure, names, media attributes, sandbox tokens, metadata, enhancement layers).

Later sections will add their own projects (accessibility engineering, performance, backend architecture) as they are authored.

## Practice structure

Level ladder per set: guided → independent → debugging/real-world → project mini-build. Practice sets are anchored `afterLesson` so the flow interleaves Learn → Practice throughout the module — no theory wall, per the Beginner lesson learned.

## Estimated time

Section 1: ≈ 4.5 h (86 min reading + 175 min hands-on). Full-course estimate to be revised as sections are added.

## Verification gates (Section 1)

- `validate-content.ts` extended to three courses × both locales
- new `verify-challenges-c3.mjs` harness: every challenge reference-passes and wrong-solution-fails
- full platform gates: typecheck, lint, unit/integration, E2E, production build
