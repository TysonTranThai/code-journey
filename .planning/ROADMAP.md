# Roadmap: Code Journey

## Overview

Code Journey ships as a vertical MVP: each phase delivers a working, end-to-end user capability. Phase 1 establishes a verified development foundation. Phase 2 adds identity, data, and the content pipeline. Phase 3 delivers the platform's defining loop — browser-authored code graded inside an isolated sandbox. Phase 4 turns grading events into progress. Phase 5 adds community and the pedagogy-first AI mentor. Phase 6 hardens everything (accessibility, security, observability) to launch quality.

## Phases

**Standing Product Constraint (all phases):** Code Journey is a WEB-ONLY product — the website is the product. Every phase delivers responsive web UI (desktop/tablet/ intentionally-designed mobile); public content is SEO-indexable while private user pages are no-index; all student-code execution and AI calls go through server-side web APIs (the browser never executes student code with platform privileges). Native targets (Tauri/Electron/Swift/React Native/Flutter) are barred unless requirements explicitly change.

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Development Foundation & Verification** - Reproducible dev environment with all quality gates green
- [ ] **Phase 2: Data, Auth & Content Pipeline** - Working auth, database, and zod-validated content-as-data curriculum browsing
- [ ] **Phase 3: Challenge Loop & Sandbox Execution** - Students write code in the browser and get auto-graded in an isolated sandbox
- [ ] **Phase 4: Progress & Achievements** - Server-verified progress, streaks, and achievements
- [ ] **Phase 5: Community & AI Mentor** - Discussions anchored to content plus guarded AI hints
- [x] **Phase 6: Hardening, Accessibility & Launch Readiness** - WCAG 2.1 AA, security review, observability, E2E coverage
- [x] **Phase 8: Course 1 — Web Development Beginner** - First full production course: research → curriculum → 56 lessons / 51 challenges across 7 modules, all test-verified
- [x] **Phase 9: Private Beta Deployment** - Beta live loopback-only with invite gate, hardened sandbox timeout fix, backup/restore + container rehearsal verified
- [x] **Phase 10: Course 1 Revision** - Learn/Practice separation as first-class PracticeSet content type; 91 challenges; deliberate-practice level model
- [x] **Phase 11: Course 2 — Web Development Intermediate** - Genuine Beginner progression: research → curriculum → 13 modules / 80 lessons / 181 challenges (EN+VI), all test-verified in both locales
- [x] **Phase 12: Course 3 — Web Development Advanced (Section 1: Advanced HTML)** - Advanced HTML section: 1 module / 7 lessons / 7 practice sets / 21 challenges (EN+VI), Documentation Hub project with decision-verification checkpoints, prerequisite on Course 2 enforced
- [x] **Phase 13: Python Beginner** - First Python course: research → curriculum → 15 modules / 57 lessons / 40 practice sets / 134 challenges (EN+VI), Python added to the sandbox runtime, all test-verified
- [x] **Phase 14: Python Intermediate** - Genuine Python Beginner progression: 12 modules / 49 lessons / 36 practice sets / 93 challenges (EN+VI), sandbox-shaped design (stdlib-only grading), all test-verified
- [x] **Phase 15: C++ Beginner** - New cpp track: research → curriculum → 19 modules / 66 lessons / 27 practice sets / 46 challenges (EN+VI), C++20 added to the sandbox runtime (g++ 14.2, exec-able /tmp), modern ownership-first C++, all test-verified

## Phase Details

### Phase 1: Development Foundation & Verification
**Goal**: A clean, reproducible development foundation: scaffolded Next.js/TypeScript/Tailwind app, verified scripts, code quality tooling, git hygiene, and documentation
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: PLAT-01, PLAT-02, PLAT-04
**Success Criteria** (what must be TRUE):
  1. A developer can clone the repo and start the dev server using only README-documented commands (verified on a clean install)
  2. `pnpm dev`, `pnpm build`, `pnpm lint`, `pnpm typecheck`, `pnpm test` all run successfully
  3. `.env.example` documents every required environment variable; no real secrets are in git history
  4. `.gitignore` covers node_modules, build output, and env files; `.env*` (except example) cannot be committed
**Plans**: 3 plans

Plans:
- [x] 01-01: Scaffold Next.js 16 + TypeScript + Tailwind 4 app with pnpm
- [x] 01-02: Quality gates (ESLint flat config, Prettier, Vitest with a first real test) and verified package scripts
- [x] 01-03: Git hygiene (.gitignore, .env.example), README/CONTRIBUTING/docs skeleton, environment audit doc

### Phase 2: Data, Auth & Content Pipeline
**Goal**: Working identity and data layer plus the curriculum content pipeline; visitors can browse real structured lessons
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: AUTH-01, AUTH-02, AUTH-03, AUTH-04, AUTH-05, CURR-01, CURR-02, CURR-03, CURR-04, PLAT-07
**Success Criteria** (what must be TRUE):
  1. A visitor can browse tracks → courses → lessons and read a rendered lesson without an account
  2. A user can sign up with email/password, log in via GitHub, and stay logged in across refreshes; logout works everywhere
  3. Password reset flow issues an emailed (dev: logged) link that lets the user set a new password
  4. Database runs via Docker Compose; `pnpm db:migrate` and `pnpm db:seed` work from a clean state
  5. Invalid curriculum content fails the build with a schema validation error
**Plans**: 4 plans

Plans:
- [x] 02-01: PostgreSQL via Docker Compose + Drizzle schema (users, sessions, curriculum core) + db scripts
- [x] 02-02: Auth.js integration (email/password + GitHub OAuth, dev-mode email transport)
- [x] 02-03: Content-as-data pipeline (MDX/JSON + zod schema + loaders with build-time validation)
- [x] 02-04: Curriculum browsing UI (track/course/lesson pages, linear navigation; responsive layouts, SEO metadata on public pages, no-index on authed pages)

### Phase 3: Challenge Loop & Sandbox Execution
**Goal**: The core product loop — a student writes code in the browser, submits, and gets test-by-test verdicts from an isolated sandbox
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: CHAL-01, CHAL-02, CHAL-03, CHAL-04, CHAL-05, CHAL-06, PLAT-08
**Success Criteria** (what must be TRUE):
  1. A user can write code in the browser editor, run it against challenge tests, and see pass/fail per test
  2. Passing submissions are recorded server-side and linked to the user and challenge
  3. Submitted code executes in a sandbox with: no network access, memory/CPU limits, execution timeout, non-root user, ephemeral filesystem
  4. Malicious-sample test suite (fork bombs, network calls, file access, infinite loops) passes — all attempts are contained or timeout
  5. In-progress code survives a page refresh
**Plans**: 4 plans

Plans:
- [x] 03-01: Execution job queue (Postgres-backed) + runner worker architecture
- [x] 03-02: Containerized Node sandbox (no-network, resource limits, timeouts) + isolation test suite
- [x] 03-03: Submissions API + verdict flow (queue → run → verdict persistence)
- [x] 03-04: Challenge page UI (Monaco editor, run/submit actions, educational failure output, draft persistence; responsive workspace — desktop panels reflow to tabs/drawers/stacked sections on tablet/mobile)

### Phase 4: Progress & Achievements
**Goal**: Real, server-verified progress a learner can see and trust
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: PROG-01, PROG-02, PROG-03, PROG-04
**Success Criteria** (what must be TRUE):
  1. Completed lessons and challenges show completion state for the logged-in user
  2. A user dashboard shows overall progress and a consecutive-day streak
  3. Defined milestones award achievements; award logic runs server-side only
  4. Forged client requests cannot mark progress without a server-verified completion event
**Plans**: 2 plans

Plans:
- [x] 04-01: Progress events model + server-verified completion recording
- [x] 04-02: Dashboard UI (progress, streak, achievements)

### Phase 5: Community & AI Mentor
**Goal**: Social learning and guarded AI help layered onto the core loop
**Mode:** mvp
**Depends on**: Phase 4
**Requirements**: COMM-01, COMM-02, COMM-03, AI-01, AI-02, AI-03, AI-04
**Success Criteria** (what must be TRUE):
  1. Logged-in users can post and reply on lessons; visitors can read threads
  2. The mentor returns graduated hints on request and never a complete working solution (verified by a refusal test suite)
  3. The mentor can explain errors from a failed run in educational terms
  4. Mentor usage is rate-limited per user; with no AI key configured, the platform works fully and mentor UI degrades gracefully
**Plans**: 3 plans

Plans:
- [x] 05-01: Discussions (threads anchored to lessons, reply, read access for visitors)
- [x] 05-02: MentorAdapter interface + guardrails (hint ladders, refusal tests, rate limiting)
- [x] 05-03: Mentor UI (hint/error-explain actions on challenge pages, graceful no-key degradation) — executed within 05-02 (UI + degradation delivered together)

### Phase 6: Hardening, Accessibility & Launch Readiness
**Goal**: Public-quality bar: accessibility, security review, observability, and E2E coverage
**Mode:** mvp
**Depends on**: Phase 5
**Requirements**: PLAT-03, PLAT-05, PLAT-06
**Success Criteria** (what must be TRUE):
  1. Critical-path E2E suite (signup → lesson → challenge → pass → progress) passes in CI-equivalent runs
  2. Keyboard navigation and WCAG 2.1 AA contrast verified on core flows (lessons, challenges, dashboard, auth)
  3. Security review checklist completed: auth/session posture, sandbox isolation audit, dependency audit clean or triaged
  4. Structured logs, error tracking hook, and basic health endpoint exist; README documents all verified commands accurately
**Plans**: 3 plans

Plans:
- [x] 06-01: E2E suite (Playwright) for the critical path
- [x] 06-02: Accessibility pass (keyboard, contrast, focus states, reduced motion) + a11y tests
- [x] 06-03: Security review + observability (logging, error tracking hook, health endpoint) + docs refresh

### Phase 11: Course 2 — Web Development Intermediate
**Goal**: Genuine progression from Beginner: build, debug, test, secure, optimize, and deploy more complex web applications (EN+VI)
**Mode:** mvp
**Depends on**: Phase 8 (Course 1) + Phase 10 (practice architecture)
**Success Criteria** (what must be TRUE):
  1. Every challenge verified two-sided by harness: reference solution passes, wrong solution fails (181/181 intermediate; beginner regression 91/91)
  2. EN and VI content structurally synchronized and loadable through schema-validating loaders in both locales
  3. Beginner course intact: full beginner regression gates green
  4. Full gate: typecheck, lint, unit/integration, E2E (mobile + a11y + keyboard), production build, content validation
**Waves**: research → curriculum spec → content authoring (13 modules) → practice → projects → localization → validation → QA

Waves:
- [x] 11-01: Research + curriculum spec (docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-INTERMEDIATE.md, docs/COURSE-2-...md)
- [x] 11-02: Content authoring 13 modules via Python authoring pipeline (lessons, practices, checkpoints, capstone)
- [x] 11-03: Localization (VI sidecars + practice overlays, EN/VI structural sync validation)
- [x] 11-04: QA + hardening (challenge harness, both-locale loader sweep in validate-content.ts, unit/E2E updates, VI 404 fix)

### Phase 12: Course 3 — Web Development Advanced (Section 1: Advanced HTML)
**Goal**: Begin Course 3 with genuine advanced HTML: document architecture, ARIA-first accessibility, native interactive elements, responsive media, secure embeds, metadata, progressive enhancement (EN+VI)
**Mode:** mvp
**Depends on**: Phase 11 (Course 2 verified complete before starting — independently audited)
**Success Criteria** (what must be TRUE):
  1. Every challenge verified two-sided by harness (21/21; beginner 91/91 + intermediate 181/181 regression)
  2. EN and VI structurally synchronized, schema-valid in both locales
  3. Advanced course enforces prerequisite on Course 2; project graded via decision-verification (not gameable)
  4. Full gate: typecheck, lint, unit/integration, E2E, production build, content validation
**Waves**: audit Intermediate → research (WHATWG/MDN/WAI/web.dev) → authoring → localization → QA

Waves:
- [x] 12-01: Research (docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-ADVANCED.md) + Course 3 docs (docs/COURSE-3-WEB-DEVELOPMENT-ADVANCED.md)
- [x] 12-02: Advanced HTML authoring — 7 lessons + 7 practice sets + 21 challenges + Documentation Hub project (EN)
- [x] 12-03: VI localization, synchronized structures, shared grading code
- [x] 12-04: QA — harness 21/21, both-locale validation, regression harnesses, full gates (blocked mid-session by Python track co-authoring; unblocked and closed 2026-09-13)

### Phase 13: Python Beginner
**Goal**: First full Python course on the platform: fundamentals through files, modules, environments, testing, CLIs, and a finance capstone (EN+VI)
**Mode:** mvp
**Depends on**: Phase 3 (sandbox execution) — extends the worker contract with a Python runtime
**Success Criteria** (what must be TRUE):
  1. Python execution in the sandboxed worker (same heredoc-data job protocol, isolation preserved)
  2. Every challenge verified two-sided (134/134; web regression 91+181+21 green)
  3. EN and VI synchronized and schema-valid in both locales
  4. Full gate green including production build with the new course
**Waves**: research → sandbox runtime → authoring (15 modules) → practice → localization → validation → QA

Waves:
- [x] 13-01: Research + curriculum design (docs/COURSE-PYTHON-BEGINNER.md)
- [x] 13-02: Python runtime in sandbox worker (`src/workers/python-runtime.ts`, Dockerfile.sandbox python3)
- [x] 13-03: Content authoring — 15 modules, 57 lessons, 40 practice sets, 134 challenges + capstone (EN)
- [x] 13-04: VI localization (134 VI sidecars + overlays); QA — harness 134/134, validator all-courses green, E2E 36/36

### Phase 14: Python Intermediate
**Goal**: Genuine Python Beginner progression: larger, cleaner, testable Python — OOP/data model, typing, robust errors, files/streaming, testing (unittest+mock), SQLite with parameterized security, HTTP via transport injection, asyncio, packaging + security audit, CLI capstone (EN+VI)
**Mode:** mvp
**Depends on**: Phase 13 (Python Beginner; ran concurrently under multi-agent safety, prerequisite wired after Beginner landed)
**Success Criteria** (what must be TRUE):
  1. Every challenge verified two-sided (93/93)
  2. Grading honest to the platform contract: exec + `code` source variable + boilerplate-as-submission (no `inspect.getsource` tests)
  3. EN and VI synchronized (227 nodes per locale), schema-valid
  4. Prerequisite on python-beginner enforced; Beginner course untouched throughout
  5. Full gate: validator, unit/integration, E2E, typecheck, lint, production build
**Waves**: audit Beginner state → research → authoring (12 modules) → localization → challenge verification → QA

Waves:
- [x] 14-01: Research + spec (docs/CURRICULUM-RESEARCH-PYTHON-INTERMEDIATE.md, docs/COURSE-PYTHON-INTERMEDIATE.md) — boundary aligned to actual Beginner scope
- [x] 14-02: Authoring — 12 modules, 49 lessons, 36 practice sets, 93 challenges (EN) via pi.py pipeline
- [x] 14-03: VI localization, synchronized, shared grading code
- [x] 14-04: QA — 93/93 two-sided after root-causing 24 harness failures (exec-contract rewrites, sqlite row_factory/commit fixes, 7 accidentally-correct wrong solutions replaced); unit 160/160; E2E 36/36; build 986 pages

### Phase 15: C++ Beginner
**Goal**: First C++ course on a brand-new cpp track: modern C++ (C++20, GCC 14.2) taught ownership-first for true beginners and Python/Web converts — fundamentals, STL, OOP, pointers/references, RAII & memory safety, files, debugging/testing, multi-file+CMake, architecture, git workflow, problem solving, finance-CLI capstone (EN+VI)
**Mode:** mvp
**Depends on**: none (independent track; ran alongside the active Python Advanced agent under multi-agent safety)
**Success Criteria** (what must be TRUE):
  1. C++ execution proven end-to-end through the real sandbox path before any content
  2. Every challenge verified two-sided (46/46) with byte-identical test files (harness imports buildCppTestFile)
  3. Modern C++ throughout: RAII/ownership core, raw new/delete never normalized, warnings always on
  4. EN and VI synchronized (184 nodes per locale), schema-valid, globally unique IDs
  5. Full gate: validator, unit/integration, E2E, typecheck, lint, production build; no regression in any existing course
**Waves**: capability probe → research → authoring (19 modules) → localization → challenge verification → QA

Waves:
- [x] 15-01: Multi-agent inspection + capability probe (sandbox had no C++ — added cpp-runtime.ts, g++ to Dockerfile.sandbox, exec-able /tmp tmpfs; 4/4 hard-path probes)
- [x] 15-02: Research + spec (docs/CURRICULUM-RESEARCH-CPP-BEGINNER.md, docs/COURSE-CPP-BEGINNER.md) — C++20 baseline, modern-practices ordering
- [x] 15-03: Authoring — 19 modules, 66 lessons (17 checkpoints), 27 practice sets, 46 challenges (EN) via cppb.py pipeline
- [x] 15-04: VI localization synchronized; global-ID collision renames (7, my side only)
- [x] 15-05: QA — 46/46 two-sided after root-causing 11 first-run failures (variadic CHECK_LINES/CHECK_THROWS after preprocessor comma discovery, 3 accidentally-correct wrong solutions replaced, broken authored snippets fixed, missing }; in capstone solutions); systemic over-escape repair (48 challenge JSONs + ledger); MDX JSX traps fixed; unit 160/160; E2E 36/36; typecheck ✓; lint 0 errors; build 1125 pages

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Development Foundation & Verification | 3/3 | Complete (executed during Phase 0 init) | 2026-09-02 |
| 2. Data, Auth & Content Pipeline | 4/4 | Complete (executed + live-verified) | 2026-09-02 |
| 3. Challenge Loop & Sandbox Execution | 4/4 | Complete (executed + E2E verified; isolation hard gate green) | 2026-09-02 |
| 4. Progress & Achievements | 2/2 | Complete (executed + live-verified: verdict→event→award→dashboard) | 2026-09-02 |
| 5. Community & AI Mentor | 3/3 | Complete (refusal suite green; no-key degradation verified; rate-limited) | 2026-09-02 |
| 6. Hardening, Accessibility & Launch Readiness | 3/3 | Complete (6/6 E2E green incl. critical path; axe AA audits green; pnpm audit clean; observability seam) | 2026-09-03 |
| 7. Beta Readiness & Hardening | 11/11 | **Complete (2026-09-03)** — grade integrity, auth-to-run + submission authz, atomic rate limits, reset email seam, mobile editor + run flow fixed (E2E at 7 viewports), static public curriculum (SSG), breadcrumb/prompt polish, sandbox host scoping + Judge0 production doc | 2026-09-03 |
| 8. Course 1 — Web Development Beginner | 8 waves | **Complete (2026-09-04)** — research + spec docs; 7 modules, 56 lessons, 51 challenges (every challenge ref-verified pass/fail by harness); course landing metadata + outcomes; data-driven module achievement; curriculum integrity suite (34 checks); QA found and fixed 7 grading defects; full gate green (124 unit/integration, 33 E2E, lint/typecheck/format/build) | 2026-09-04 |
| 9. Private Beta Deployment | deploy waves | **Complete (2026-09-05)** — PRIVATE BETA LIVE loopback-only (user decision); invite-code gate; sandbox container-timeout leak fix; backup/restore verified; tunnel E2E 30/30 then stood down | 2026-09-05 |
| 10. Course 1 Revision | 1 phase | **Complete (2026-09-05)** — Learn/Practice separation (PracticeSet content type, afterLesson interleaving); 52 sets / 88 practice challenges / 91 total; deliberate-practice level model surfaced in UX; harness 107/107; unit 136/136; E2E 36/36 | 2026-09-05 |
| 11. Course 2 — Web Development Intermediate | 4 waves | **Complete (2026-09-12)** — 13 modules, 80 lessons (EN+VI), 63 practice sets, 181 challenges (169 practice + 12 checkpoint); prerequisite enforced; harness 181/181 + beginner 91/91; validate-content.ts extended to both courses × both locales; VI loader 404 fixed + gated; unit 160/160; E2E 36/36; build 538 pages | 2026-09-12 |
| 12. Course 3 — Web Development Advanced (Advanced HTML) | 4 waves | **Complete (2026-09-13)** — Advanced HTML section: 1 module, 7 lessons, 7 practice sets, 21 challenges (EN+VI); Documentation Hub project via 3 decision-verification checkpoints; prerequisite on Course 2 enforced; harness 21/21; validator 3 courses × 2 locales; unit 160/160; E2E 36/36; build 694 pages | 2026-09-13 |
| 13. Python Beginner | 4 waves | **Complete (2026-09-13)** — 15 modules, 57 lessons, 40 practice sets, 134 challenges (EN+VI); Python sandbox runtime added to worker contract; harness 134/134; validator all-courses green; unit 124/124 (later re-runs green); E2E 36/36 | 2026-09-13 |
| 14. Python Intermediate | 4 waves | **Complete (2026-09-13)** — 12 modules, 49 lessons, 36 practice sets, 93 challenges (EN+VI); prerequisite on python-beginner; harness 93/93 after root-causing 24 failures (platform exec-contract, sqlite, accidentally-correct wrong solutions); unit 160/160; E2E 36/36; build 986 pages | 2026-09-13 |
| 15. C++ Beginner | 5 waves | **Complete (2026-09-13)** — new cpp track: 19 modules, 66 lessons (17 checkpoints), 27 practice sets, 46 challenges (EN+VI); C++20 sandbox runtime added (cpp-runtime.ts, g++ 14.2, exec-able /tmp tmpfs); modern ownership-first C++; harness 46/46 after root-causing 11 failures (variadic CHECK_LINES/CHECK_THROWS, 3 accidentally-correct wrong solutions, broken authored snippets); systemic over-escape repair; unit 160/160; E2E 36/36; build 1125 pages | 2026-09-13 |
| 16. Python Advanced | 4 waves | **Complete (2026-09-14)** — see .planning/phases/16-python-advanced/SUMMARY.md | 2026-09-14 |
| 17. C++ Intermediate | 4 waves | **Complete (2026-09-14)** — see .planning/phases/17-cpp-intermediate/SUMMARY.md | 2026-09-14 |
| 18. Java Beginner | 4 waves | **Complete (2026-09-14)** — see .planning/phases/18-java-beginner/SUMMARY.md | 2026-09-14 |
| 19. Java Intermediate | 4 waves | **Complete (2026-09-15)** — see .planning/phases/19-java-intermediate/SUMMARY.md | 2026-09-15 |
| 20. C++ Advanced | 4 waves | **Complete (2026-09-15)** — see .planning/phases/20-cpp-advanced/SUMMARY.md | 2026-09-15 |
| 21. Java Advanced | 4 waves | **Complete (2026-09-15)** — see .planning/phases/21-java-advanced/SUMMARY.md | 2026-09-15 |
| 22. C Beginner | 4 waves | **Complete (2026-09-15)** — see .planning/phases/22-c-beginner/SUMMARY.md | 2026-09-15 |
| 23. C Intermediate | 4 waves | **Complete (2026-09-15)** — see .planning/phases/23-c-intermediate/SUMMARY.md | 2026-09-15 |
| 24. C Advanced | 4 waves | **Complete (2026-09-16)** — see .planning/phases/24-c-advanced/SUMMARY.md | 2026-09-16 |
| 25. C# Beginner | 4 waves | **Complete (2026-09-17)** — new csharp track: 21 modules, 85 lessons, 105 challenges; .NET 10 sandbox runtime; harness 105/105; see .planning/phases/25-csharp-beginner/SUMMARY.md | 2026-09-17 |
| 26. C# Intermediate | 4 waves | **Complete (2026-09-18)** — 22 modules, 70 lessons (22 checkpoints), 25 practice sets, 101 challenges (EN+VI, 244 nodes × 2 locales); harness 101/101 (254 ref tests, every wrong solution fails ≥1); validator all-tracks green; typecheck 0, lint 0 errors, unit 181/181; live smoke PASS; E2E deferred (port conflict, documented); see .planning/phases/26-csharp-intermediate/SUMMARY.md | 2026-09-18 |
| 27. C# Advanced | 4 waves | **Complete (2026-09-18)** — 23 modules, 110 lessons (23 checkpoints), 23 practice sets, 78 challenges (EN+VI, 258 nodes × 2 locales); two-sided harness 78/78 (128 ref tests pass, all wrong solutions fail ≥1, 94 wrong-side fails); scoped validator both locales green; typecheck 0, lint 0, unit 184/184; shared C# harness upgraded (async tests, Roslyn resolver, conditional usings) with Beginner regression re-verified 105/105; E2E deferred (documented); see .planning/phases/27-csharp-advanced/SUMMARY.md | 2026-09-18 |
| 28. HSG Intermediate | 4 waves | **Complete (2026-09-19)** — new hsg-intermediate course: 18 modules, 58 lessons (18 checkpoints + 4 contest checkpoints), 18 practice sets, 110 challenges (EN+VI); two-sided harness 110/110 (460/460 ref tests, every wrong solution fails ≥1); g++ 14.2.0 C++20 sandbox verified, perf probe ≤1.5s on largest inputs; typecheck 0, lint 0 errors, unit 184/184, build PASS, E2E 36/36; see .planning/phases/28-hsg-intermediate/SUMMARY.md | 2026-09-19 |
| 29. HSG Advanced | 20 waves (module-per-wave) | **Complete (2026-09-20)** — new hsg-advanced course: 20 modules, 83 lessons (17 module checkpoints + 12 contest checkpoints), 20 practice sets, 92 challenges (EN+VI, ~77 h); two-sided container harness 92/92 (every wrong solution fails ≥1) + ledger mirror 92/92; fixed 8 orphaned checkpoint lesson refs found by loader audit; typecheck 0, lint 0 errors, unit 184/184, build PASS, E2E 36/36; see .planning/phases/29-hsg-advanced/SUMMARY.md | 2026-09-20 |
| 30. AP CSA Beginner | 20 waves (module-per-wave) | **Complete (2026-09-21)** — NEW ap-csa track + ap-csa-beginner course: 20 modules, 80 lessons (60 teaching + 20 checkpoints), 20 practice sets, 109 challenges (EN+VI, ~36.5 h), aligned to revised Fall-2025 AP CSA framework (4 units, inheritance light); two-sided harness 109/109 + ledger mirror 109/109 on javac --release 21; typecheck 0, lint 0 errors, unit 184/184, build PASS, E2E 36/36; see .planning/phases/30-ap-csa-beginner/SUMMARY.md | 2026-09-21 |
| 31. HSG Mastery | 14 waves (module-per-wave) | **Complete (2026-09-22)** — new hsg-mastery course (track hsg), process-first problem-solving capstone: 14 modules, 43 lessons (28 teaching + 15 checkpoints), 14 practice sets, 57 challenges (EN+VI, ~17.1 h); two-sided container harness 57/57 (101/101 ref tests, every wrong solution fails ≥1) + ledger mirror 57/57; typecheck 0, lint 0 errors, unit 172/172, build PASS, E2E 36/36; disclosed minimal MDX fix to untracked hsg-intensive files; see .planning/phases/31-hsg-mastery/SUMMARY.md | 2026-09-22 |
| 32. HSG Intensive | module-per-wave | **Complete (2026-09-22)** — new hsg-intensive course (track hsg), fourth stage: mastery & competition training, ~20% review / 80% problem solving: 12 modules, 32 lessons (12 checkpoints), 12 practice sets, 79 challenges (EN+VI; 39 combination / 23 independent / 15 debugging / 2 real-world); recognition/budget/observation/combination/wrong-clinic/stress/subtask/speed/mixed/contests/editorials/final-pack incl. 2 original mock contests + final simulation + capstone; two-sided container harness 79/79 (every ref passes all tests, every wrong fails ≥1, coverage reconciled 79/79) + Python ground truths; scoped validator 150 nodes/locale clean; typecheck 0, lint 0 errors, unit 184/184, build PASS; regression B/I/A clean EN+VI via scoped roots; note: hsgm-process VI summary >200 chars (other course) blocks track-wide VI load until fixed; no contest-timer schema — contests are contest-format practice sets, sprints self-timed (documented); see .planning/phases/32-hsg-intensive/SUMMARY.md | 2026-09-22 |
| 33. AP CSA Advanced | module-per-wave | **Complete (2026-09-26)** — new ap-csa-advanced course (track ap-csa, course 3, the endgame after Foundations and Core): 24 modules, 96 lessons (72 teaching + 24 checkpoints), 24 practice sets, 129 Java challenges (EN+VI, 298 nodes × 2 locales, ~42 h); ~80% problem solving with E1–E5 difficulty scale; hard tracing, misconception-coded MCQs (all ground truths machine-verified), FRQ workshop/method/class/debug/partial-credit, error-analysis lab (13 classes), timed sets, exam strategy, three full practice exams + final master simulation; two-sided harness 129/129 (every ref passes all tests, every wrong fails ≥1); validator all-tracks green (exit 0); typecheck 0, lint 0 errors, unit 136 passed / 3 pre-existing integration failures, build PASS (4916 pages); live smoke on own port (course/practice/checkpoints 200, VI 200); lesson URLs need re-check when Docker daemon returns (DB down = 500 for all courses); shared-infra: additive track.json row, validator warns-and-skips unauthored courses, minimal render-safety fix to other agent's in-progress ap-csa-core MDX (build-breaking brace artifacts), Core content otherwise untouched; see .planning/phases/33-ap-csa-advanced/SUMMARY.md | 2026-09-26 |
| 34. AP CSA Core | module-per-wave | **Complete (2026-09-26)** — new ap-csa-core course (track ap-csa, course 2, the bridge between Foundations and the mastery course): 20 modules, 42 lessons (20 teaching + 22 checkpoints), 26 practice sets, 121 Java challenges (EN+VI, ~31 h), ~30% instruction / ~70% problems in four arcs (problem-solving, topic mastery, integration, exam performance incl. per-type FRQ labs, debugging clinic, four timed mixed sets, four-part simulation + rubric self-scoring); MCQ-style practice delivered as executable trace/predict/repair challenges (platform has no native MCQ schema — documented); two-sided harness 121/121 via verify-challenges-apc-core.mjs (same buildJavaTestFile as sandbox, javac --release 21); typecheck 0, lint 0 errors, unit 172/172 passed 0 failed (12 conditional skips; local-DB integration fixed via superuser grant), build PASS, content map 3446 imports, curriculum audit 2864 ids / 0 problems; shared-infra: additive track.json row + course-order fix (core before advanced), mdx-map regenerated; cross-agent edits disclosed and preserved (advanced course + validator warn-and-skip); see .planning/phases/33-ap-csa-core/SUMMARY.md, docs/COURSE-AP-CSA-CORE.md | 2026-09-26 |
