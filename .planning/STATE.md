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
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02)

**Core value:** A student can learn to code for free through structured lessons, auto-graded sandboxed challenges, and verified progress — with an AI mentor that teaches instead of solving.
**Current focus:** v1.1-beta — Phase 7 (beta readiness & hardening) complete

**Standing product constraint (2026-09-02):** Code Journey is WEB-ONLY — the website is the product; the browser is the platform. No native/shell/mobile targets (Tauri/Electron/Swift/React Native/Flutter barred); responsive web UI required (intentionally designed mobile, not shrunken desktop); student-code execution and AI are server-side web APIs only; SEO for public content, no-index for private data; deployment is normal web infra, provider unselected (avoid vendor lock-in). Recorded in PROJECT.md, REQUIREMENTS.md (PLAT-06/07/08), ROADMAP.md.

## Current Position

Phase: 7 of 7 — ALL PHASES COMPLETE (Phase 7 executed 2026-09-03)
Plan: 30 of 30 plans executed across Phases 1–7
Status: v1.1-beta ready — all audit P0/P1 fixes implemented and regression-covered; private-beta appropriate (production Judge0 migration + curriculum growth remain)
Last activity: 2026-09-04 — Phase 8 executed: Course 1 "Web Development Beginner" shipped end-to-end (research → curriculum → 56 lessons / 51 challenges in 7 modules → challenge QA harness with 51/51 ref-verified → landing/outcomes/achievements → 34-check integrity suite → full gate green).

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

Last session: 2026-09-04
Stopped at: **Phase 8 (Course 1 — Web Development Beginner) COMPLETE** — 8 commits: 68beae3 research + Modules 1–2; a1127d5 Module 3; 4f7ce40 Module 4; fefd6bf Modules 5–7; 0ba1873 challenge QA harness + 5 grading-defect fixes; 9ad8fa5 landing metadata + data-driven achievement + integrity suite; c6d8386 repo-wide Prettier; 8eae08a breadcrumb E2E rename. Final gate: typecheck ✓ lint ✓ format ✓ 124/124 unit/integration ✓ 33/33 E2E (a11y + mobile included) ✓ build (121 pages) ✓.
Resume file: None
