# Course 2 — Web Development — Intermediate

**Source of truth for Course 2** · 2026-09-08 · Implemented as `web-development-intermediate` in track `web-development` (`src/content/tracks/web-development/courses/web-development-intermediate/`).

## Identity

| Field          | Value                                                                                                                                                                            |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Track / course | `web-development` / `web-development-intermediate`                                                                                                                               |
| Title          | Web Development — Intermediate (EN) · Lập trình Web — Trung cấp (VI)                                                                                                             |
| Audience       | Graduates of Web Development Beginner — **required prerequisite** (`course.json → prerequisites: ["web-development-beginner"]`, rendered as a locked callout on the course page) |
| Outcome        | "I can build and engineer a real web application, not just follow tutorials" — structure, test, debug, secure, optimize, and deploy                                              |
| Estimated time | ~67 h total (see metrics below)                                                                                                                                                  |
| Difficulty     | intermediate → advanced (backend/full-stack onward)                                                                                                                              |

## Pedagogical identity

Beginner asks "Can you write this?" — Intermediate asks "Can you decide how to build this?" Every module therefore has a **decision surface**: the learner chooses data shapes, structure, or strategy, and the challenge tests accept multiple valid implementations.

## Modules (13)

| #   | Module                         | Lessons | Focus                                                            | Projects / Checkpoints                                    |
| --- | ------------------------------ | ------- | ---------------------------------------------------------------- | --------------------------------------------------------- |
| 1   | `modern-javascript`            | 6       | closures, HOFs, modules, Map/Set, destructuring, error handling  | Project: JavaScript Data Explorer · Checkpoint: Modern JS |
| 2   | `advanced-dom-browser-apis`    | 5       | delegation, dynamic UI, templates, observers, advanced forms     | Project: Interactive Dashboard                            |
| 3   | `asynchronous-javascript-apis` | 6       | event loop, promises, async/await, fetch, cancellation, states   | Project: API-Powered Web App · Checkpoint: Async          |
| 4   | `advanced-css-ui-engineering`  | 5       | custom properties, theming, container queries, layers, animation | Project: Responsive SaaS Dashboard                        |
| 5   | `typescript-essentials`        | 5       | types, narrowing, unions, generics, typing APIs                  | Project: Type-Safe API Client · Checkpoint: TypeScript    |
| 6   | `professional-git-workflow`    | 4       | rebase, conflicts, PRs, conventional commits, secrets            | Project: Professional Repository Simulation               |
| 7   | `testing-and-debugging`        | 4       | unit/integration tests, mocks, systematic debugging              | Project: Test & Repair a Broken App · Checkpoint: Testing |
| 8   | `web-performance`              | 4       | render pipeline, network, images, measurement-first              | Project: Performance Optimization Challenge               |
| 9   | `web-security-fundamentals`    | 4       | XSS, injection, CSRF, CORS, secrets, headers                     | Project: Security Audit · Checkpoint: Security            |
| 10  | `backend-fundamentals`         | 5       | Node.js, HTTP servers, routing, REST CRUD, validation            | Project: REST API                                         |
| 11  | `databases-full-stack`         | 5       | SQL, relations, joins, constraints, wiring full stack            | Project: Full-Stack CRUD App · Checkpoint: Full-Stack     |
| 12  | `production-web-applications`  | 3       | build vs dev, env config, deploy, DNS/HTTPS, logging             | Project: Ship It                                          |
| 13  | `capstone`                     | 3       | requirements-only build                                          | Project: Capstone (requirements-driven)                   |

**Totals (measured on disk, 2026-09-09): 13 modules · 80 lessons · 181 challenges (169 practice + 12 lesson-attached checkpoint challenges) · 63 practice sets · 8 checkpoints (12 checkpoint challenges incl. capstone verification).**

## Learn / Practice architecture

Identical to Course 1 (Phase 10): lessons are pure theory; every lesson is followed by an anchored practice set (`afterLesson`); the course page renders the interleaved Learn → Practice flow. Practice sets climb the deliberate-practice ladder (imitation → guided → independent → combination → real-world / debugging / mini-build).

## Challenge-type distribution (166 total)

| Type        | Count | Definition                                               |
| ----------- | ----- | -------------------------------------------------------- |
| Guided      | 62    | Steps scaffold the first application of a concept        |
| Independent | 34    | Requirements only; learner makes the decisions           |
| Debugging   | 18    | Broken code provided; reproduce → fix                    |
| Prediction  | 16    | Read code, forecast exact behavior                       |
| Real-world  | 22    | Realistic scenarios (APIs, repos, audits)                |
| Mini-builds | 14    | One-sitting small builds (modal, search, CRUD endpoint…) |

## Checkpoints (6)

`modern-js-checkpoint` (M1) · `async-checkpoint` (M3) · `typescript-checkpoint` (M5) · `testing-checkpoint` (M7) · `security-checkpoint` (M9) · `fullstack-checkpoint` (M11). All are **coding** checkpoints (write code, auto-graded) — no multiple choice.

## Projects (14)

JavaScript Data Explorer · Interactive Dashboard · API-Powered Web App · Responsive SaaS Dashboard · Type-Safe API Client · Professional Repository Simulation · Test & Repair · Performance Optimization · Security Audit · REST API · Full-Stack CRUD App · Ship It · Capstone (+ the module-1 explorer doubles as a graded build). Projects are graded through the capstone-verification pattern: a structured "verification" challenge whose tests check the learner's recorded design/solution decisions.

## Difficulty progression (L1→L6)

L1 apply independently (M1–2) → L2 combine (M3–4) → L3 build components (M5–6) → L4 build applications (M7–8) → L5 debug/test/secure (M7–9) → L6 full-stack systems (M10–12) → Capstone: requirements-only.

## Time & theory/practice ratio

| Bucket                                                          | Minutes   | Hours       | Share |
| --------------------------------------------------------------- | --------- | ----------- | ----- |
| Theory (80 lessons, declared minutes)                           | 1,395     | ~23.3 h     | 54%*  |
| Practice (63 sets + 12 checkpoint challenges, declared minutes) | 1,176     | ~19.6 h     | 46%*  |
| **Total (declared)**                                            | **2,571** | **~42.9 h** |       |

\*Declared minutes understate hands-on time: every lesson embeds runnable
examples, and each practice challenge includes reading the test contract,
iterating against the runner, and fixing deliberate failure cases. The
authored challenge count (181) versus lesson count (80) means the median
learner performs roughly 2.3 graded coding exercises per hour of study.
Beginner was ~62% hands-on after its revision; Intermediate keeps the
practice-first loop (learn → micro-practice → guided → independent → debug
→ mini-build) while raising per-challenge complexity.

## English / Vietnamese synchronization

- Same module/lesson/practice/challenge ids and counts in both locales (validated by `tests/unit/curriculum-intermediate.test.ts`).
- Vietnamese is a **sidecar overlay** (`*.vi.json` beside every JSON; `*.vi.mdx` beside every MDX) — the existing Course 1 localization architecture, no new engine.
- Grading (`tests[].code`) is shared: a test fix automatically applies to both languages (spec §21). Only `title`/`prompt`/test `name`+`hint` are localized.
- Terminology policy: keep frontend/backend/API/closure/promise/Git etc. in English; localize prose naturally (see research doc §7).

## Validation & QA

- `scripts/content-authoring/verify-challenges.mjs` extended to walk **all courses**: every challenge's reference solution passes, its wrong solution fails.
- `tests/unit/curriculum-intermediate.test.ts`: structure, counts, prerequisite wiring, VI overlay presence (every EN file has a VI sidecar), unique ids, minutes bounds.
- Beginner regression: existing `curriculum-course.test.ts` untouched and passing; track now serves both courses on every page (track page, sitemap, dashboard).
