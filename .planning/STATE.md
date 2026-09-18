---
gsd_state_version: '1.0'
status: milestone_complete

milestone_audit:
  date: 2026-09-03
  v1_requirements: 34
  requirements_complete: 34
  notes:
    - AUTH-03 (GitHub OAuth) code-complete and env-gated; activates with real OAuth app credentials
    - AI-01 provider seam complete; real mentor provider activates with MENTOR_API_KEY
    - Unit/integration 94/94; E2E 13/13 (incl. critical path + keyboard-only journey); pnpm audit clean; build clean
    - Known v1.x gaps documented in docs/SECURITY.md (rate limiting on challenge/auth endpoints, outbound allow-list) and .planning/STATE.md blockers
curriculum_milestone_audit:
  date: 2026-09-12
  milestone: Curriculum growth — Web Development learning path (Courses 1 + 2)
  scope:
    - Course 1 web-development-beginner (Phase 8 + Phase 10 revision): 7 modules, 56 lessons, 91 challenges, 52 practice sets
    - Course 2 web-development-intermediate (Phase 11): 13 modules, 80 lessons, 181 challenges, 63 practice sets; prerequisite on Course 1 enforced
  audit_results_2026-09-12:
    - validate-content.ts: both courses × both locales (259 + 401 nodes each) load clean; structures synchronized
    - Challenge harnesses: intermediate 181/181, beginner 91/91 (reference passes + wrong fails, per challenge)
    - Unit/integration 160/160 (27 files); E2E 36/36; typecheck/lint clean; production build 538 pages
    - Live QA: VI course page 404 (course.vi.json audience > 400-char schema limit) found, fixed, and gated by the both-locale loader sweep (fault-injection proven)
  leftovers:
    - ~396 files uncommitted on main (user decision on commit strategy)
    - repo-wide prettier drift (~304 pre-existing files) — separate repo-wide decision
  verdict: COMPLETE — all gates green, Beginner intact, both locales synchronized
progress:
  total_phases: 8
  completed_phases: 8
  total_plans: 30
  completed_plans: 30
  percent: 100

phase_8:
  date: 2026-09-04
  status: complete
  course: web-development-beginner (Course 1)
  modules: 7
  lessons: 56
  challenges: 51
  delivered:
    - Research: docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-BEGINNER.md (freeCodeCamp, MDN, Odin, W3C/WAI, web.dev patterns analyzed; original content only)
    - Spec: docs/COURSE-1-WEB-DEVELOPMENT-BEGINNER.md reconciled to shipped reality
    - Content-as-data: 7 modules (web intro, HTML, CSS, JavaScript, Git/GitHub, web architecture, capstone) with projects, checkpoints, mixed challenge types (guided/independent/debug/prediction/real-world)
    - Infra: scripts/generate-mdx-map.mjs wired into prebuild/predev; course dir renamed web-development-foundations → web-development-beginner
    - QA: scripts/content-authoring/verify-challenges.mjs executes every challenge test against reference (must pass) and wrong solutions (must fail) — 51/51 verified; fixed 7 grading defects it found
    - Landing: course.json landing fields (outcomes/audience/time), landing page renders stats + outcomes; achievements data-driven from curriculum loaders
    - Tests: tests/unit/curriculum-course.test.ts (34 integrity checks); updated 3 stale unit tests + breadcrumb E2E
  gate: typecheck ✓ lint ✓ prettier ✓ 124/124 unit+integration ✓ 33/33 E2E (a11y + mobile included) ✓ build 121 pages ✓
phase_9:
  date: 2026-09-05 (code work 2026-09-04)
  status: complete — PRIVATE BETA LIVE (GO)
  beta_deployment:
    host: user-approved dev machine (single-host fallback; two-host split remains production target)
    entry: http://localhost:3000 LOOPBACK-ONLY (user stood down the ngrok tunnel after full tunnel verification; AUTH_URL/NEXT_PUBLIC_SITE_URL restored to localhost)
    access: invite-code gate live (phrase stored in deploy/.beta-invite-code.txt, hash-only in env); wrong code creates 0 accounts (live-verified)
    fixes_during_deploy: fresh-DB migration double-PK defect (achievements/progress_events schema+migration+snapshots); compose env_file≠substitution trap (deploy/.env symlink)
  verification_2026-09-05:
    - E2E 30/30 THROUGH the public HTTPS tunnel (incl. invite-gated register → run → verdict → persist; mobile 375px; keyboard-only; axe) — then tunnel stood down by user decision; loopback serving re-verified (health, landing, /learn)
    - beta stack containers healthy (db/web/worker + healthchecks); verdict passed through container loop
    - security headers + HSTS verified over tunnel HTTPS; 20/20 live regression earlier on prod build
  delivered:
    - Verified baseline: 124/124 unit+integration (sandbox isolation suite green), 33 E2E, build 121 pages
    - FIX sandbox container leak (production blocker): wall-clock timeout now kills the CONTAINER not just the docker client (0 leaks across 3 verification runs)
    - FIX SSG build required live DB (lesson thread counts) — build-time fallback added
    - SMTP EmailSender adapter (nodemailer 8, env-gated EMAIL_PROVIDER=smtp + SMTP_URL + EMAIL_FROM), console fallback keeps loud warning
    - Security headers middleware: CSP, nosniff, frame-deny, referrer-policy, permissions-policy, prod-only HSTS — verified live on every response
    - Beta access gate: BETA_INVITE_CODE_SHA256 invite code on registration (constant-time, fail-closed, unit + live tested); register page made dynamic
    - Deploy assets: Dockerfile.web, deploy/beta.yml (db/web/worker/migrate/backup + singlehost fallback), deploy/sandbox-host.yml, .dockerignore
    - Backup/restore VERIFIED (pg_dump → fresh Postgres restore: 266 users/86 submissions/71 events)
    - Container rehearsal VERIFIED: web+worker containers → queue → hardened sandbox → verdict passed
    - Live security regression 20/20 on prod build (headers, 401 anon run, gated register, login, verdict passed, ownership 401, 429 burst, dashboard)
    - E2E 30/30 post-changes; 128/128 unit+integration; typecheck/lint/format clean
  gate: GO — PRIVATE BETA LIVE at http://localhost:3000 (loopback-only per user decision; tunnel re-enable procedure documented in docs/DEPLOYMENT.md); zero RED items; accepted YELLOWs: no remote access until tunnel/domain re-enabled, single-host sandbox fallback, SMTP delivery unverified, no mentor provider, no external monitoring. PUBLIC PRODUCTION: NOT READY (Judge0, dedicated sandbox host, real domain, email delivery, monitoring, final security review remain)
phase_10:
  date: 2026-09-05
  status: complete
  title: Course 1 Revision — expand practice, separate Learn/Practice (learner-feedback phase)
  delivered:
    - Practice architecture: PracticeSet content type (schema + loaders + zod), `afterLesson` anchoring with interleaved course flow (Learn → Practice → Learn), new routes /practice/<set> (hub) and /practice/<set>/<challenge>
    - Content: 52 practice sets / 88 practice challenges — every non-checkpoint lesson-attached challenge (48) MIGRATED into its lesson's practice set (lessons are pure theory; only 3 checkpoint challenges stay lesson-attached) + authored sets; 16 near-duplicates culled; every lesson followed by coding practice; levels: 52 guided, 10 imitation, 10 debugging, 7 independent, 6 mini-build, 2 real-world, 1 combination
    - UX: practice hub (concept, difficulty, level badges, per-challenge progress), PracticeProgress component + /api/progress/challenges endpoint, lesson-page anchored-practice callout, Learn/Practice/Project visual distinction on course page
    - Progress semantics: lesson completion requires passes from anchored practice sets; practice passes recorded as challenge events (no migration)
    - QA: harness extended to practices + practice-solutions.mjs (91/91 ref+wrong verified incl. 19 restored solutions + 3 interactive stubs), validate-content.ts integrity, unit tests updated to practice-first semantics (136/136 incl. PROG-02 gated on anchored-practice passes), E2E updated to practice URLs + practice callout flow (36/36)
    - Docs: COURSE-1 spec + CURRICULUM-RESEARCH revised (§9 practice-density/deliberate-practice evidence, IA decision, metrics)
  before_after: 56 lessons / 51→91 challenges (88 practice + 3 checkpoint) / 52 practice sets / ~13h→~21h
  gate: typecheck ✓ lint ✓ prettier ✓ 134/134 unit+integration ✓ 36/36 E2E ✓ harness 107/107 ✓ integrity OK ✓ build 199 pages ✓
  note: practice challenge URLs are 7-segment (no `challenge/` static segment) — 8-segment dynamic routes inside (learn) overflow in Next 16.3.4 Turbopack dev (isolated repro verified)
phase_11:
  date: 2026-09-12
  status: complete
  course: web-development-intermediate (Course 2)
  modules: 13
  lessons: 80 (EN .mdx + VI .vi.mdx sidecars)
  challenges: 181 (169 practice + 12 lesson-attached checkpoint incl. capstone verification)
  practice_sets: 63
  delivered:
    - Research: docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-INTERMEDIATE.md (MDN, web.dev, OWASP Top-10, Node/TypeScript/PostgreSQL docs, Odin, freeCodeCamp, Full Stack Open; original content only)
    - Spec: docs/COURSE-2-WEB-DEVELOPMENT-INTERMEDIATE.md reconciled to shipped reality
    - Content-as-data: 13 modules (modern JS, advanced DOM, async/APIs, advanced CSS/UI, TypeScript, git workflow, testing/debugging, performance, security, backend, databases/full-stack, production, capstone); prerequisite web-development-beginner enforced in course.json + prerequisite UI
    - Practice-first: Learn/Practice separation reused from Course 1 architecture; levels guided→independent with debugging/prediction/mini-build mixes; capstone (ServiceDesk) graded via decision-verification challenges that cannot be gamed
    - QA: verify-challenges-i2.mjs — 181/181 ref-verified pass + wrong-solution-fail; Beginner regression harness 91/91; validate-content.ts extended to walk BOTH courses through schema-validating loaders in BOTH locales (259 beginner + 401 intermediate nodes per locale)
    - Bug class closed: live QA caught VI course-page 404 — course.vi.json `audience` exceeded the 400-char zod limit so the loader threw on every VI request (no earlier gate loaded VI through the loaders); copy tightened to 389 chars and the both-locale loader sweep added to validate-content.ts, proven by fault injection
    - Wiring fixes: course.json module refs aligned to disk IDs; cross-course ID collisions renamed (workflow-checkpoint → git-workflow-checkpoint, components-practice); 7 checkpoints moved from invalid level to valid levels
    - Tests: unit/integration updated for two-course reality (160/160 across 27 files); dashboard/seo/curriculum tests tightened or extended; E2E 36/36 (mobile 375px, keyboard-only, a11y, SEO static render)
  gate: typecheck ✓ lint ✓ build 538 pages ✓ validator both-locales ✓ harnesses 181/181 + 91/91 ✓ unit 160/160 ✓ E2E 36/36 ✓
  note: all gates re-verified from scratch on 2026-09-12 after environment restart; 3 transient unit failures were the stopped codejourney-db container (environmental, not code)
phase_12:
  date: 2026-09-12 (gates closed 2026-09-13)
  status: complete
  course: web-development-advanced (Course 3, section 1: Advanced HTML)
  modules: 1 (advanced-html)
  lessons: 7 (EN .mdx + VI .vi.mdx)
  challenges: 21 (guided/independent/debugging/real-world + 3 project decision-verification)
  practice_sets: 7 (all afterLesson-interleaved; ~67% hands-on)
  delivered:
    - Research: docs/CURRICULUM-RESEARCH-WEB-DEVELOPMENT-ADVANCED.md (WHATWG HTML LS, MDN, W3C WAI, web.dev; Baseline-verified popover/invoker teaching)
    - Spec: docs/COURSE-3-WEB-DEVELOPMENT-ADVANCED.md
    - Content: html-architecture, accessible-names, native-disclosure-dialogs, popovers-invokers, responsive-media, sandboxed-embeds-metadata, docs-hub project (graded via 3 decision-verification challenges that read the artifact)
    - Intermediate audited COMPLETE before starting (independent re-run of validator + 181/181 + 91/91 harnesses)
    - Tooling: verify-challenges-c3.mjs + c3-solutions.mjs + validate-c3.ts; validate-content.ts extended additively to Course 3
  gate: harness 21/21 ✓ validator 3 courses × 2 locales ✓ typecheck ✓ lint 0 errors ✓ unit 160/160 ✓ E2E 36/36 ✓ build 694 pages ✓ beginner 91/91 + intermediate 181/181 regression ✓
  note: mid-session global gates were blocked by the concurrently-authoring Python track (missing manifests); left untouched per multi-agent safety, then unblocked only after user authorization; Python Beginner agent's own final structure later superseded the unblock
phase_13:
  date: 2026-09-13
  status: complete
  course: python-beginner (first Python course; track python)
  modules: 15
  lessons: 57
  challenges: 134 (two-sided verified)
  practice_sets: 40
  delivered:
    - Platform: Python execution in sandbox worker (src/workers/python-runtime.ts, same heredoc-data job protocol as JS; __builtins__ preserved for graded code); python3 in Dockerfile.sandbox
    - Content: fundamentals → strings → decisions → collections → loops → functions → errors/debugging → files/paths/data → stdlib/modules → venv/pip → testing/quality → problem-solving → CLI (Task Manager) → finance capstone
    - Localization: full EN+VI parity (134 VI sidecars + practice/lesson overlays)
    - QA: harness 134/134 (ledger deduped); validate-content.ts all-courses green; MDX compile sweep 114/114 (fixed unescaped `<` in capstone-finance-ship)
  gate: harness 134/134 ✓ validator 5 courses × 2 locales ✓ typecheck ✓ lint 0 errors ✓ unit 124/124 ✓ E2E 36/36 ✓ build PASS (re-verified after the intermediate MDX fix) ✓
  note: executed by a second agent concurrently with Phases 12/14; this record reflects their SUMMARY at .planning/phases/13-python-beginner/SUMMARY.md
phase_14:
  date: 2026-09-13
  status: complete
  course: python-intermediate (prerequisite python-beginner wired)
  modules: 12 (incl. capstone)
  lessons: 49 (11 checkpoint lessons)
  challenges: 93 (two-sided verified)
  practice_sets: 36
  delivered:
    - Research: docs/CURRICULUM-RESEARCH-PYTHON-INTERMEDIATE.md + docs/COURSE-PYTHON-INTERMEDIATE.md (boundary aligned to the ACTUAL Beginner scope — deepen, not reteach)
    - Content arc: pythonic-toolkit → objects-and-modeling → data-model-iteration → structure-and-typing → robust-errors → files-and-data → testing-discipline → databases (SQLite, parameterized queries as security centerpiece) → http-json (transport injection, no network needed) → concurrent-async (graded by real concurrency timing) → packaging + security-audit → capstone-cli-app
    - Sandbox-shaped design: image ships stdlib only (sqlite3/asyncio/http.client/tomllib/unittest.mock; no pytest/requests) → unittest+mock taught, pytest framed as local extension
    - QA: 24 first-run harness failures all root-caused and fixed (exec contract: no inspect.getsource ever — use `code`; boilerplate is part of the graded unit; sqlite row_factory/commit in tests; 7 accidentally-correct wrong solutions replaced); VI hint regression self-introduced and restored
  gate: harness 93/93 ✓ validator full tree × 2 locales (227 nodes/locale) ✓ unit 160/160 ✓ E2E 36/36 ✓ typecheck ✓ lint 0 errors ✓ build 986 pages ✓
phase_15:
  date: 2026-09-13
  status: complete
  course: cpp-beginner (new cpp track; prerequisites: none — first C++ course)
  modules: 19 (incl. capstone)
  lessons: 66 (17 checkpoint lessons)
  challenges: 46 (two-sided verified)
  practice_sets: 27
  delivered:
    - Platform: C++ execution added to the sandbox (cpp-runtime.ts with #include "solution.cpp" + #define main cj_learner_main test contract; g++ 14.2 in Dockerfile.sandbox; /tmp tmpfs noexec→exec, documented; language enum widened additively; 120s timeout; 4/4 hard-path probes before any content)
    - Research: docs/CURRICULUM-RESEARCH-CPP-BEGINNER.md + docs/COURSE-CPP-BEGINNER.md — C++20 baseline (GCC 14.2 Alpine), modern-practices ordering, memory-safety spine (RAII/ownership core; raw new/delete never normalized)
    - Content arc: first-programs → variables-and-types → conditions → cpp-loops → cpp-functions → strings → collections → stl-algorithms → structs-enums → classes-oop → pointers-references → memory-raii → files-persistence → errors-debugging-tests → multi-file-cmake → architecture-refactoring → git-professional-workflow → problem-solving → capstone-finance-cli
    - QA: 11 first-run harness failures root-caused (macro args split at top-level commas → variadic CHECK_LINES/CHECK_THROWS; CHECK_THROWS(fn) called the RESULT; 3 accidentally-correct wrong solutions replaced; 2 broken authored snippets; missing }; in cpp19 solutions); systemic over-escape repair across 48 challenge JSONs + ledger rebuilt (46 R/W pairs); MDX JSX traps (pair<iterator,bool>, bare {sets}) fixed; 7 global-ID collisions renamed on my side only
  gate: harness 46/46 (byte-identical test files via buildCppTestFile) ✓ validator full tree × 2 locales (184 nodes/locale cpp; 3 tracks / 6 courses) ✓ unit 160/160 ✓ E2E 36/36 ✓ typecheck ✓ lint 0 errors ✓ build 1125 pages ✓ live routes 200 incl. VI cookie
curriculum_milestone_audit_2:
  date: 2026-09-13
  milestone: Curriculum growth — Course 3 start (Advanced HTML) + Python learning path (Beginner + Intermediate)
  scope:
    - Course 3 web-development-advanced (Phase 12): section 1 of 5 planned sections — 1 module, 7 lessons, 21 challenges, Documentation Hub project
    - Course python-beginner (Phase 13): 15 modules, 57 lessons, 134 challenges, 40 practice sets
    - Course python-intermediate (Phase 14): 12 modules, 49 lessons, 93 challenges, 36 practice sets; prerequisite on python-beginner enforced
  audit_results_2026-09-13:
    - validate-content.ts: full tree (web beg/int/adv + python beg/int) × both locales load clean, structures synchronized
    - Challenge harnesses all two-sided: 91/91 + 181/181 + 21/21 (web) and 134/134 + 93/93 (python)
    - Unit/integration 160/160; E2E 36/36 (mobile + keyboard + a11y); typecheck/lint clean; production build 986 pages (was 538)
    - Live QA: deep routes served correctly after dev-server restart with new content; VI locale (cookie-based) renders Course 3 + Python Intermediate
  leftovers:
    - ~500 files uncommitted on main (user decision on commit strategy)
    - repo-wide prettier drift (pre-existing) — separate repo-wide decision
    - other agent's scripts/content-authoring/verify-challenges-py.mjs still has a syntax error (their WIP file, left untouched)
  verdict: COMPLETE — all gates green, all prior courses intact, EN/VI synchronized across five courses
curriculum_milestone_audit_3:
  date: 2026-09-14
  milestone: Curriculum growth — C++ Advanced course completes the C++ learning path (Phase 20, parallel build)
  scope:
    - Course cpp-advanced (Phase 20): 20 modules, 74 lessons (20 checkpoints), 40 practice sets, 88 challenges (68 practice + 20 checkpoint); EN+VI parity; prerequisite on cpp-intermediate (resolved — Phase 17 shipped in parallel)
  audit_results_2026-09-14:
    - Challenge harness verify-challenges-cppa.mjs: 88/88 two-sided green (byte-identical sandbox files)
    - validate-content.ts: 3 tracks / 9 courses × both locales clean; cpp linear path 204 lessons; deliberate-practice levels stamped on all 68 practice challenges (6 imitation / 14 guided / 11 independent / 20 combination / 12 real-world / 4 debugging / 1 mini-build)
    - Unit/integration 160/160; E2E critical path 2/2; typecheck/lint clean; repo-wide pnpm build PASS 1949 pages (clears the Phase 19 note's external blocker from my then-untracked MDX)
    - Live QA: preview on :3000 renders the full course; VI chrome via cookie
  leftovers:
    - course-header "challenges" stat reads 0 on ALL courses (getLessonPractices called with empty lessonId in course page) — pre-existing shared-router quirk, untouched
    - repo-wide prettier drift; ~600 uncommitted files (user decisions)
  verdict: COMPLETE — all gates green, all sibling courses intact, C++ path Beginner→Intermediate→Advanced finished
curriculum_milestone_audit_4:
  date: 2026-09-15
  milestone: Curriculum growth — C Intermediate course bridges Beginner→Advanced on the C track (Phase 23, parallel build)
  scope:
    - Course c-intermediate (Phase 23): 16 modules, 64 lessons (48 teaching + 16 checkpoints), 32 practice sets, 84 challenges (68 practice + 16 checkpoint); EN+VI parity; ~33.6 h; capstone = persistent MiniKV key-value store
  audit_results_2026-09-15:
    - Challenge harness verify-challenges-cint.mjs: 84/84 two-sided clean (102/102 reference tests pass; every wrong solution fails ≥1 test)
    - validate-content.ts: schema-valid, ids unique across kinds/courses, c-intermediate 229 nodes × both locales clean; c linear path 148 lessons; exit 0
    - Unit/integration 160/160; E2E 36/36 (mobile 390px + keyboard); typecheck/lint clean; production build PASS
    - Regression: C Beginner harness 158/158 OK; all five track linear paths healthy (no sibling damage)
  leftovers:
    - repo-wide prettier drift; ~600 uncommitted files (user decisions)
    - E2E webServer holds the :3000 dev lock (long-lived process from an earlier session) — E2E run against production next start on :3456
  verdict: COMPLETE — all gates green, C Beginner intact, EN/VI synchronized
curriculum_milestone_audit_5:
  date: 2026-09-17
  milestone: Curriculum growth — C Advanced course completes the C learning path (Phase 24, parallel build)
  scope:
    - Course c-advanced (Phase 24): 24 modules, 77 lessons (53 teaching + 24 checkpoints), 24 practice sets, 112 challenges (88 practice + 24 checkpoint); EN+VI parity; ~20.9 h; final checkpoint = integrated systems capstone
  audit_results_2026-09-17:
    - Two-sided harness (via _ca_smoke.mjs against the staged course dir): 112/112 — every reference solution passes, every wrong solution fails ≥1 test (0 false passes)
    - validate-content.ts: c-advanced clean both locales; global id uniqueness (no cross-kind ca- collisions); schema limits enforced (400/200-char, level enum)
    - Unit/integration 166/166 (28 files); E2E 15/15 (critical path 2/2, axe WCAG 2.1 AA 7/7, practice-flow 6/6 incl. mobile 390px); typecheck clean; lint 0 errors; production build PASS
    - content:map indexes c-advanced MDX (2012 lessons repo-wide)
    - Regression: c-beginner (22 modules), c-intermediate (16), cpp (20/19/12), java (14/15/15) untouched per git diff — zero modifications to sibling tracks
  leftovers:
    - repo-wide prettier drift; ~1500 uncommitted files incl. this course's authoring scripts (user decisions)
    - sanitizers/Valgrind/GDB/multi-file linking taught conceptually (sandbox-verified absence) with deterministic behavioral discriminators
  verdict: COMPLETE — all gates green, all sibling courses intact, C path Beginner→Intermediate→Advanced finished
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02)

**Core value:** A student can learn to code for free through structured lessons, auto-graded sandboxed challenges, and verified progress — with an AI mentor that teaches instead of solving.
**Current focus:** v1.1-beta — PRIVATE BETA LIVE (Phase 9 deployed 2026-09-05); curriculum growth shipped — Course 1 Revision (Phase 10), Course 2 — Web Development Intermediate (Phase 11), Course 3 — Web Development Advanced started with the Advanced HTML section (Phase 12), and the Python track Beginner + Intermediate (Phases 13–14); public production gated (Judge0, domain, email, monitoring)

**Standing product constraint (2026-09-02):** Code Journey is WEB-ONLY — the website is the product; the browser is the platform. No native/shell/mobile targets (Tauri/Electron/Swift/React Native/Flutter barred); responsive web UI required (intentionally designed mobile, not shrunken desktop); student-code execution and AI are server-side web APIs only; SEO for public content, no-index for private data; deployment is normal web infra, provider unselected (avoid vendor lock-in). Recorded in PROJECT.md, REQUIREMENTS.md (PLAT-06/07/08), ROADMAP.md.

## Current Position

Phase: 7 of 7 — ALL PHASES COMPLETE (Phase 7 executed 2026-09-03)
Plan: 30 of 30 plans executed across Phases 1–7
Status: v1.1-beta ready — all audit P0/P1 fixes implemented and regression-covered; private-beta appropriate (production Judge0 migration + curriculum growth remain)
Last activity: 2026-09-13 — Phases 12–14 executed and verified end-to-end: Course 3 Advanced HTML (Phase 12), Python Beginner (Phase 13, second agent), Python Intermediate (Phase 14). Curriculum now: web-development Beginner→Intermediate→Advanced(HTML section) and python Beginner→Intermediate, all EN+VI synchronized; milestone audit 2 recorded in frontmatter (build 986 pages, harnesses 91+181+21+134+93 all two-sided green).

Progress: [██████████] 100% (19 of 19 plans across Phases 1–6)

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Auth.js v5 pinned (next-auth@5.0.0-beta.32 + @auth/drizzle-adapter@1.11.3), JWT sessions, bcrypt 12, env-gated GitHub — live-verified
- DB stores identity + execution/progress state; curriculum content-as-data (zod, build-time validation); submissions immutable snapshots
- Progress representation locked: append-only progress_events, unique (user, contentType, contentId); challenge completion derives from sandbox verdicts (D-05 Phase 4); lesson completion server-verifies challenge passes; streaks derived at read time; achievement defs as content-as-data with idempotent server awards
- Execution isolation locked: hardened Docker sandbox, malicious-sample suite green; Judge0/Firecracker remain production paths
- Monaco via @monaco-editor/react (CDN loader); drafts in localStorage
- Mentor: provider-agnostic MentorAdapter seam; NullMentor degrades to content-hint hints (AI-04); refusal filter + hint ladder server-side (refusal suite green); mentor_requests per-user daily quotas (10 hints / 20 explains); real provider arrives only with MENTOR_API_KEY + a chosen provider
- Discussions: threads anchored to content lesson ids; public read, session-derived authorship; plain-text comments (React-escaped)
- AUTH_SECRET required in prod mode; dev secret in .env.local

### Pending Todos

None yet.

### Blockers/Concerns

- GitHub OAuth (AUTH-03) needs a real OAuth app from the user — provider is env-gated; platform works without it
- remark-gfm/rehype-slug installed but not wired (Turbopack serializable-options constraint) — GFM tables render plain; programmatic compile is the fallback
- ~~Pages render dynamically due to session read in root layout~~ RESOLVED 07-08: root layout static; public routes pre-render (SSG); challenge page derives session client-side
- Sandbox isolation verified against phase attack classes on Docker Desktop; production-grade claim requires external review (docs/SECURITY.md); beta = dedicated sandbox host (SANDBOX_DOCKER_HOST), public = self-hosted Judge0 (docs/PRODUCTION.md)
- ~~Monaco CDN loader — local bundling deferred~~ RESOLVED Wave 2: Monaco self-hosted in public/monaco-vs via `pnpm monaco:sync`
- E2E determinism: pause `pnpm worker` while running unit/integration suites — the live worker steals queue jobs from tests sharing the dev DB (observed 2026-09-03)

## Session Continuity

Last session: 2026-09-17
Stopped at: **Phase 26 COMPLETE — C# Intermediate shipped: 22 modules / 70 lessons (22 checkpoints) / 25 practice sets / 101 challenges (two-sided harness 101/101 in the real sandbox: 254 reference tests pass, every wrong solution fails ≥1 test, 0 wrongly-passing), full EN+VI parity (validator SYNC match, 244 nodes × 2 locales; see `.planning/phases/26-csharp-intermediate/SUMMARY.md` and `docs/COURSE-CSHARP-INTERMEDIATE.md`).** Gates green: validate-content exit 0 (all tracks incl. hsg load EN+VI), typecheck exit 0, lint 0 errors, unit tests 181/181, live route smoke PASS (course/lesson/practice/checkpoint 200; VI cookie renders C# — Trung cấp). E2E Playwright NOT re-run this session (dev-server port conflict with a concurrent agent; smoke-tested live routes instead). Toolchain: .NET SDK 10.0.401, net10.0, C# 14, offline BCL-only grading; PBKDF2/Rfc2898DeriveBytes + path APIs probed in-sandbox before M21. Shared-infra changes documented: validator +1 course row, verify script mirrors production CS_ADV_EXTRA_REFS_GLOB, 6 HSG lessons repaired (another agent's minutes→difficulty arg-shift broke the whole-curriculum loader). The csharp track now runs Beginner → Intermediate → Advanced. Prior session: 2026-09-17 Phase 25 COMPLETE — C# Beginner (21 modules / 105 challenges, harness 105/105; details in STATE history and `.planning/phases/25-csharp-beginner/SUMMARY.md`). Known repo-level leftovers: prettier drift, HSG agent's uncommitted hsg_m20.py (theirs, untouched).
