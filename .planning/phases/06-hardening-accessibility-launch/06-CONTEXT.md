# Phase 6: Hardening, Accessibility & Launch Readiness - Context

**Gathered:** 2026-09-02
**Status:** Ready for planning

<domain>
## Phase Boundary

Phase 6 raises the platform to public-quality bar: critical-path E2E coverage (Playwright), WCAG 2.1 AA accessibility pass on core flows, a security review checklist with dependency audit, and observability foundations (structured logs, error-tracking hook, health check) plus docs refresh. Features are frozen — this phase verifies and hardens what Phases 1–5 built. Standing constraints remain (WEB-ONLY, responsive, SEO public / no-index private).

</domain>

<decisions>
## Implementation Decisions

### E2E (PLAT-03)
- **D-01:** Playwright with @playwright/test, chromium-only locally (cross-browser later), webServer config reusing `pnpm dev -p 3100` (avoids colliding with dev servers on 3000) and DATABASE_URL from .env.local. Tests cover the critical path: register → browse lesson → run challenge (sandbox up) → verdict → dashboard progress. Anonymous browsing + no-index checks also E2E'd.
- **D-02:** E2E uses real infra (Docker DB + sandbox); suites skip-with-message when infra is down, mirroring unit/integration conventions. `pnpm test:e2e` script; kept OUT of the default `pnpm test` (unit+integration) so CI without Docker still passes.

### Accessibility (PLAT-05, WCAG 2.1 AA)
- **D-03:** Pass targets: skip link (exists — verify), semantic landmarks (header/nav/main/footer — verify), focus-visible rings on all interactive elements, contrast of the zinc/sky/indigo palette on dark backgrounds (audit + fix), form labels (already aria-label'd — audit), aria-live for verdict/mentor output (exists), reduced-motion (exists), keyboard-only path through lesson → challenge → run (E2E assertion via keyboard navigation).
- **D-04:** Manual-ish audits become automated where cheap: axe-core via @axe-core/playwright on core pages (home, learn, lesson, challenge, login, register, dashboard) with AA ruleset; violations fail the E2E run.

### Security & observability (PLAT-05 partial)
- **D-05:** Security review checklist in docs/SECURITY.md upgraded from PLANNED to VERIFIED items with evidence pointers (isolation suite, auth posture, authorization guards, zod boundaries, no raw HTML, secrets strategy). Dependency audit: `pnpm audit` run + triaged (documented, not silently ignored).
- **D-06:** Observability foundations: structured JSON log lines from the runner (already job-id-only — formalize a tiny logger), error-tracking hook (`src/lib/observability.ts` — captureError() that console-errors in dev and is the seam for Sentry etc. later; NO vendor added), health endpoint extended to report DB reachability.
- **D-07:** Docs refresh: README verified-commands table, CONTRIBUTING accuracy, PHASE report links. No invented instructions — every command re-verified.

</decisions>

<specifics>
## Specific Ideas

- E2E run/verdict test asserts the FULL user-visible loop (button states, verdict panel copy) — the strongest regression net the platform has.
- axe audit as a separate Playwright project so it can run without the sandbox when Docker is down.
- Health endpoint returns {status, db: up/down} — used by E2E to wait for readiness.

</specifics>

<canonical_refs>
## Canonical References
- `.planning/REQUIREMENTS.md` — PLAT-03, PLAT-05, PLAT-06
- `.planning/ROADMAP.md` — Phase 6 success criteria
- `docs/SECURITY.md` — honesty requirements (IMPLEMENTED vs PLANNED vs NOT YET VERIFIED)
- `docs/DATA-MODEL.md`, `README.md`, `CONTRIBUTING.md` — accuracy refresh targets
</canonical_refs>

<code_context>
## Existing Code Insights
- Skip-if-infra-down test conventions; vitest aliases; pnpm scripts
- Existing skip link + aria usage from Phases 2–5; dark zinc palette
- Health route exists at /health (basic) — extend
</code_context>

<deferred>
## Deferred Ideas
- Cross-browser E2E (webkit/firefox) — post-launch CI expansion
- Error-tracking vendor integration — seam only (no vendor lock-in)
- Performance budgets/PPR — noted in STATE as future work
</deferred>

---

*Phase: 06-hardening-accessibility-launch*
*Context gathered: 2026-09-02*
