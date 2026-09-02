---
phase: 06-hardening-accessibility-launch
plan: 01
---

# Plan 06-01 Report: E2E Critical Path

**Completed:** 2026-09-02

## What Was Built

Playwright E2E covering the anonymous surface and the authenticated student journey against real infra (PLAT-03):

1. **Playwright config** — `playwright.config.ts`: Chromium, single worker, dev server on :3456 (3100 is occupied by an unrelated machine sidecar), `.env.local` preloaded via dotenv, `reuseExistingServer` for local iteration, trace retained on failure.
2. **Web-server entry** — `scripts/dev-e2e.mjs`: spawns BOTH the challenge runner worker (`node --import tsx ... src/workers/runner.ts`) and `next dev`, so the full register → run → verdict loop works inside Playwright's webServer lifecycle; both children torn down on exit (SIGINT/SIGTERM/exit hooks).
3. **Health endpoint** — `src/app/health/route.ts`: `{ status, db }` JSON (DB up/down via `SELECT 1`); used by the webServer readiness probe and by tests to skip cleanly when infra is down.
4. **Anonymous spec** — `tests/e2e/anonymous.spec.ts`: visitors read curriculum/lessons/challenges without an account (COMM-03), anonymous discussion read access, dashboard redirect to /login, health endpoint contract (PLAT-07 privacy).
5. **Critical path spec** — `tests/e2e/critical-path.spec.ts`: register (unique credentials per run) → browse curriculum → open lesson → open challenge → edit code in Monaco → Run → "All tests passed" verdict with real sandbox execution → dashboard shows verified progress and the Code Runner achievement (PROG-01..05). Second test proves keyboard-only operation reaches the verdict panel (a11y-adjacent).

## Debugging Notes (worth keeping)

- Monaco's visible `.view-line` elements intercept pointer events while the labelled `native-edit-context` textbox does not — role-locator clicks stall; clicking a view line + `ControlOrMeta+a` is the reliable user-like flow.
- Monaco is NOT inside an iframe in this setup; earlier `frameLocator` assumptions were wrong.
- The success banner renders in both the aria-live status region and the output panel — assert via `getByRole("status")` to avoid strict-mode violations.
- First run in a fresh worker pays the sandbox container cold start; verdict timeout set to 75s (observed ~5s warm, well within budget).

## Verification

- `pnpm exec playwright test tests/e2e/` → **6 passed** (4 anonymous + 2 critical path), ~15.5s.
- `pnpm test` → 94/94; `pnpm typecheck` → 0 errors; `pnpm lint` → clean.

## Requirements Covered

PLAT-03 (E2E), COMM-03 (anonymous read access), PROG-05 (dashboard reflects verified progress).
