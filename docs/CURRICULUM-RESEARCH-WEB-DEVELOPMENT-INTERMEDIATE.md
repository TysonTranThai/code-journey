# Curriculum Research — Web Development Intermediate

**Course 2 research basis** · 2026-09-08 · Original curriculum informed by (never copied from) the sources below.

## 1. Sources investigated

| Source                                                     | What was taken from it                                                                                                                                          |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MDN Web Docs (JavaScript, CSS, Accessibility, Performance) | Topic completeness check: closures, modules, event loop, container queries, cascade layers, IntersectionObserver, Core Web Vitals vocabulary                    |
| web.dev (Learn Performance, Learn CSS)                     | Rendering-path vocabulary (parse → layout → paint → composite), INP/LCP/CLS framing, measurement-first pedagogy                                                 |
| OWASP Top 10 + OWASP Cheat Sheets                          | Defensive security scope: XSS, injection, CSRF, CORS, secrets, security headers, least privilege                                                                |
| Node.js official docs                                      | Runtime model, `node:http`, no-framework server fundamentals                                                                                                    |
| TypeScript official handbook                               | Type inference, narrowing, generics, `unknown`/`never`, config                                                                                                  |
| PostgreSQL official docs                                   | Relational model, SQL basics, constraints, transactions, indexes                                                                                                |
| Git / GitHub official docs                                 | Branching, rebase vs merge, PR workflow, conventional commits, semver                                                                                           |
| W3C WAI (WCAG 2.1, WAI-ARIA patterns)                      | Keyboard patterns, focus management, reduced motion, accessible forms                                                                                           |
| The Odin Project                                           | Intermediate/advanced module ordering precedent: deep JS → DOM → async → testing; project-driven progression                                                    |
| freeCodeCamp                                               | Practice-density model: thousands of small graded steps between concepts                                                                                        |
| Full Stack Open (Univ. of Helsinki)                        | Full-stack sequencing precedent: async → typed frontend → backend → DB → testing → deploy                                                                       |
| Dev-roadmap surveys (roadmap.sh et al.)                    | Industry expectation list for "intermediate": async fluency, testing, debugging, Git collaboration, security basics, performance basics, backend + SQL exposure |

## 2. Key findings

### What separates an intermediate developer from a beginner (industry view)

1. **Decides, not follows** — beginners implement given steps; intermediates choose structure (functions vs modules vs classes, state location, data shape) and justify it.
2. **Asynchronous fluency** — comfortable reading and writing promise chains, `async/await`, parallel vs sequential composition, cancellation.
3. **Debugging as a method** — reproduces, isolates, hypothesizes, verifies; uses DevTools/network panel instead of `console.log`-only.
4. **Tests what they build** — writes assertions first or alongside; treats a bug fixed without a test as unfinished.
5. **Owns the whole request** — can trace a feature from UI event → HTTP request → server → database → response → render.
6. **Security posture** — assumes hostile input; knows XSS/injection/CSRF by mechanism, not buzzword.
7. **Performance as measurement** — profiles before optimizing; knows the render pipeline and the network waterfall.

### Educational-structure findings

- **Spacing + interleaving beats blocking**: practice distributed across many small sets (freeCodeCamp/Odin pattern) outperforms long theory blocks followed by one big exercise (spacing-effect literature; deliberate-practice research).
- **Progressive problem solving** (guided → independent) is the documented effective ladder for programming skill (van Merriënboer's worked-examples research; the basis of Code Journey's imitation→real-world levels).
- **Debugging is teachable and best taught with broken artifacts**: learners who repair deliberately-broken code transfer the skill better than those who only write greenfield code.
- **Backend should arrive after async mastery** — Node's event-loop model reuses the same mental model, so sequencing async (M3) before backend (M10) pays off twice.

### Practice research

- Effective practice for intermediate learners is **retrieval + variation**: recall the API, apply it to new data shapes, then combine with yesterday's concept.
- A reasonable research-supported density for a ~60–70 h course is **150–200 graded activities** at 5–15 min each, i.e. most learner hours in the editor.
- Every concept needs at least one **apply**, one **predict** (read code, forecast behavior), and one **debug** (fix broken code) activity.

### Project research

Intermediate-level projects should require **composition** (multiple subsystems) and **decision space** (learner chooses structure), not longer tutorials. Odin/Full Stack Open both gate progression on buildable artifacts. A capstone driven by requirements only (no steps) is the standard capstone design at this level.

## 3. Topics included (and why)

Modern JS depth (closures, modules, HOFs, Map/Set, error handling) — the language layer everything else stands on. Advanced DOM + browser APIs — components and delegation are prerequisite thinking for any framework later. Async + APIs as a major module — the single biggest beginner→intermediate differentiator. Advanced CSS — custom properties, container queries, theming. TypeScript after JS fluency — types as a design tool, not syntax trivia. Professional Git — conflicts, rebase, PRs. Testing + debugging as one module — two halves of one skill. Performance (measure-first), Security (defensive), Node backend, SQL, production concepts, requirements-driven capstone.

## 4. Topics excluded (and why)

- **React/Vue/Svelte/Tailwind/Next.js** — framework courses come after this course (spec §4: underlying technology first).
- **GraphQL, Redis, Docker internals, k8s, microservices** — beyond intermediate scope; production module covers deployment _concepts_ only.
- **Offensive security** (exploitation tooling) — spec §17: defensive recognition → prevention → safe verification only.
- **ORM deep-dives** — SQL fundamentals first; ORM is mentioned conceptually (M11) but not the teaching vehicle.
- **Generators beyond introduction, WebRTC, WebAssembly, service workers/PWA** — advanced-track material.

## 5. Ordering rationale

1. **Modern JS first** — every later module writes JS; closures/HOFs/modules are the vocabulary of M2–M9.
2. **DOM/browser APIs second** — applies M1 immediately in the browser; components before async keeps one new difficulty axis per module.
3. **Async + APIs third** — now both JS and DOM are solid; async is hard and deserves its own module before more UI work.
4. **Advanced CSS fourth** — a deliberate breather after async; UI engineering applies DOM + state skills.
5. **TypeScript fifth** — typing requires JS fluency and is best learned against real code the learner wrote in M1–M3.
6. **Git sixth** — professional workflows (rebase, PRs) make sense once the learner has real projects worth collaborating on.
7. **Testing/debugging seventh** — testing needs stable JS + module skills; debugging consolidates everything so far.
8. **Performance eighth** — measurement requires DevTools fluency from M7.
9. **Security ninth** — injection/XSS make sense once HTTP + forms + backend concepts exist.
10. **Backend tenth** — Node reuses the async model; HTTP knowledge from Beginner M6 + M3 feeds directly in.
11. **Databases eleventh** — SQL before full-stack wiring; then the full-stack CRUD project connects all three tiers.
12. **Production twelfth** — deployment concepts after the learner has something real to deploy.
13. **Capstone last** — requirements-only, integrates M1–M12.

## 6. Practice design decisions

- Loop per lesson: **Learn → micro-practice → guided → independent → debug/predict**, realized as Code Journey practice sets anchored `afterLesson` (existing architecture — no new content types).
- Target **~160 challenges** across 13 modules (within the 150–200 research band; every challenge must earn its place — no filler).
- Level mix per set follows the deliberate-practice ladder: imitation/guided → independent → combination → real-world/debugging/mini-build.
- Checkpoints are **coding checkpoints** (write code, not multiple choice) at M1, M3, M5, M7, M9, M11 + capstone.

## 7. Localization findings

- Keep industry terms in English (frontend, backend, API, request, closure, promise) — Vietnamese developers use these verbatim; translating them harms clarity.
- Educational prose is localized, not literally translated: shorter sentences, active voice, Vietnamese examples where natural.
- Grading semantics (test `code`) are shared between locales — only learner-facing text (title/prompt/hint/test names) is localized, enforced by the existing sidecar overlay architecture.
