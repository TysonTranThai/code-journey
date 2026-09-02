---
gsd_state_version: '1.0'
status: executing
progress:
  total_phases: 6
  completed_phases: 0
  total_plans: 19
  completed_plans: 0
  percent: 0
---

# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-09-02)

**Core value:** A student can learn to code for free through structured lessons, auto-graded sandboxed challenges, and verified progress — with an AI mentor that teaches instead of solving.
**Current focus:** Phase 4 — Progress & Achievements

**Standing product constraint (2026-09-02):** Code Journey is WEB-ONLY — the website is the product; the browser is the platform. No native/shell/mobile targets (Tauri/Electron/Swift/React Native/Flutter barred); responsive web UI required (intentionally designed mobile, not shrunken desktop); student-code execution and AI are server-side web APIs only; SEO for public content, no-index for private data; deployment is normal web infra, provider unselected (avoid vendor lock-in). Recorded in PROJECT.md, REQUIREMENTS.md (PLAT-06/07/08), ROADMAP.md.

## Current Position

Phase: 3 of 6 (Challenge Loop & Sandbox Execution) — EXECUTION COMPLETE
Plan: 4 of 4 in current phase (03-01…03-04 all executed + verified)
Status: Phase complete — all 7 phase requirements implemented; 5 success criteria verified incl. the malicious-sample hard gate
Last activity: 2026-09-02 — Phase 3 executed end-to-end: Postgres queue (SKIP LOCKED), hardened sandbox (fork bomb/egress/fs-escape/infinite-loop/memory-bomb all contained), challenge content + run/verdict APIs, responsive challenge workspace. Live E2E: correct solution → passed (583ms), failing solution → educational per-test hints. 59/59 tests.

Progress: [████░░░░░░] 57% (12 of 23 plans across Phases 1–3)

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Auth.js v5 pinned (next-auth@5.0.0-beta.32 + @auth/drizzle-adapter@1.11.3), JWT sessions, bcrypt 12, env-gated GitHub — live-verified (login/session/signout via curl)
- DB stores identity only; curriculum is content-as-data (JSON+MDX under src/content, zod build-time validation, invalid content fails build — proven by fixture tests)
- MDX via @next/mdx with serializable config (Turbopack constraint); lesson bodies resolved through a static import map
- Execution isolation locked: hardened Docker (node:22-alpine pinned, no-network, read-only rootfs, cap-drop ALL, non-root, wall-clock timeout); Judge0/Firecracker remain production-evolution paths; malicious-sample suite is the phase gate
- Execution queue locked: Postgres-backed execution_jobs, FOR UPDATE SKIP LOCKED claims, separate runner worker process (`pnpm worker`) — web tier never spawns interpreters
- Challenge content extends content-as-data: challengeSchema with per-test educational failure hints; submissions are immutable snapshots
- Draft persistence = localStorage keyed by challenge id (client-only)
- Monaco editor via @monaco-editor/react@4.7.0 + monaco-editor@0.54.0 (CDN loader, React 19 peers verified)
- Anonymous users can RUN challenges (submissions with null userId); attributed submits arrive with Phase 4 progress
- AUTH_SECRET required in prod mode (live 500 caught) — dev secret generated into .env.local

### Pending Todos

None yet.

### Blockers/Concerns

- GitHub OAuth (AUTH-03) needs a real OAuth app from the user — provider is env-gated; platform works without it
- remark-gfm/rehype-slug installed but not wired (Turbopack serializable-options constraint) — GFM tables in MDX render as plain tables; programmatic compile is the documented fallback
- Pages render dynamically due to session read in root layout — SSG/PPR split deferred to Phase 6 performance work
- Sandbox isolation verified against the phase's attack classes on Docker Desktop; production-grade claim still requires external review (docs/SECURITY.md)
- Monaco loads via CDN loader — local bundling deferred to Phase 6 (offline/privacy hardening)

## Session Continuity

Last session: 2026-09-02
Stopped at: Phase 3 execution complete — all 4 plans committed (03-01…03-04); isolation hard gate green; live E2E loop verified. Next: Phase 4 discuss→plan (progress & achievements, progress_events representation already locked).
Resume file: None
