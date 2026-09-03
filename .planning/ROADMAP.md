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

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Development Foundation & Verification | 3/3 | Complete (executed during Phase 0 init) | 2026-09-02 |
| 2. Data, Auth & Content Pipeline | 4/4 | Complete (executed + live-verified) | 2026-09-02 |
| 3. Challenge Loop & Sandbox Execution | 4/4 | Complete (executed + E2E verified; isolation hard gate green) | 2026-09-02 |
| 4. Progress & Achievements | 2/2 | Complete (executed + live-verified: verdict→event→award→dashboard) | 2026-09-02 |
| 5. Community & AI Mentor | 3/3 | Complete (refusal suite green; no-key degradation verified; rate-limited) | 2026-09-02 |
| 6. Hardening, Accessibility & Launch Readiness | 3/3 | Complete (6/6 E2E green incl. critical path; axe AA audits green; pnpm audit clean; observability seam) | 2026-09-03 |
| 7. Beta Readiness & Hardening | 11/11 | **Complete (2026-09-03)** — grade integrity, auth-to-run + submission authz, atomic rate limits, reset email seam, mobile editor + run flow fixed (E2E at 7 viewports), static public curriculum (SSG), breadcrumb/prompt polish, sandbox host scoping + Judge0 production doc | 2026-09-03 |
