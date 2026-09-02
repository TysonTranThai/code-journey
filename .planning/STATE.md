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

Phase: 4 of 6 (Progress & Achievements) — PLANNING COMPLETE
Plan: 0 of 2 in current phase (04-01…04-02 planned)
Status: Phase 4 planned (CONTEXT + 2 PLANs) — ready for execution
Last activity: 2026-09-02 — Phase 3 complete (queue, hardened sandbox with green isolation gate, challenge loop E2E-verified); Phase 4 planned: append-only progress_events, verdict-derived challenge completion, server-verified lesson completion, derived streaks, content-as-data achievement defs, no-index dashboard.

Progress: [████░░░░░░] 57% (12 of 23 plans across Phases 1–3)

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Auth.js v5 pinned (next-auth@5.0.0-beta.32 + @auth/drizzle-adapter@1.11.3), JWT sessions, bcrypt 12, env-gated GitHub — live-verified
- DB stores identity + execution/progress state; curriculum content-as-data (zod, build-time validation); submissions immutable snapshots
- Progress representation locked: append-only progress_events, unique (user, contentType, contentId); challenge completion derives from sandbox verdicts (D-05 Phase 4); lesson completion server-verifies challenge passes; streaks derived at read time; achievement defs as content-as-data with idempotent server awards
- Execution isolation locked: hardened Docker sandbox, malicious-sample suite green; Judge0/Firecracker remain production paths
- Monaco via @monaco-editor/react (CDN loader); drafts in localStorage
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

Last session: 2026-09-02
Stopped at: Phase 4 planning complete (04-CONTEXT + 2 PLANs). Next: execute 04-01 (progress backbone) then 04-02 (dashboard).
Resume file: None
