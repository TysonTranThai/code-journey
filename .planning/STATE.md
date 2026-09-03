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
  total_phases: 6
  completed_phases: 6
  total_plans: 19
  completed_plans: 19
  percent: 100
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02)

**Core value:** A student can learn to code for free through structured lessons, auto-graded sandboxed challenges, and verified progress — with an AI mentor that teaches instead of solving.
**Current focus:** Milestone complete — launch-ready MVP

**Standing product constraint (2026-09-02):** Code Journey is WEB-ONLY — the website is the product; the browser is the platform. No native/shell/mobile targets (Tauri/Electron/Swift/React Native/Flutter barred); responsive web UI required (intentionally designed mobile, not shrunken desktop); student-code execution and AI are server-side web APIs only; SEO for public content, no-index for private data; deployment is normal web infra, provider unselected (avoid vendor lock-in). Recorded in PROJECT.md, REQUIREMENTS.md (PLAT-06/07/08), ROADMAP.md.

## Current Position

Phase: 6 of 6 — ALL PHASES COMPLETE
Plan: 19 of 19 plans executed across Phases 1–6
Status: Milestone v1 complete — launch-ready MVP with E2E critical path, WCAG 2.1 AA audits, clean dependency audit, observability seam
Last activity: 2026-09-03 — Phase 6 executed: Playwright E2E (6/6 green incl. register→lesson→challenge→verdict→dashboard against real infra), axe-core AA audits + contrast fix (docs/A11Y.md), evidence-based docs/SECURITY.md (pnpm audit clean via overrides), vendor-neutral observability seam (src/lib/observability.ts), README/CONTRIBUTING verified-commands refresh.

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
- Pages render dynamically due to session read in root layout — SSG/PPR split deferred to Phase 6
- Sandbox isolation verified against phase attack classes on Docker Desktop; production-grade claim requires external review (docs/SECURITY.md)
- Monaco CDN loader — local bundling deferred to Phase 6

## Session Continuity

Last session: 2026-09-03
Stopped at: Milestone v1 complete — all 6 phases executed and committed. Next: milestone audit, then v1.x backlog (auth hardening: email verification/reset + GitHub OAuth; rate limiting on challenge/auth endpoints; production sandbox evaluation: Judge0/Firecracker; deployment provider selection).
Resume file: None
