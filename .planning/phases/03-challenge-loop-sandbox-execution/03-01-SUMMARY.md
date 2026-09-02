---
phase: 03-challenge-loop-sandbox-execution
plan: 01
---

# Plan 03-01 Report: Execution Job Queue Backbone

**Completed:** 2026-09-02

## What Was Built

Postgres-backed execution queue keeping student-code execution off the web tier (PLAT-08):

1. **Typed verdict model** — `src/lib/execution/types.ts`: `ExecutionStatus`, `PerTestResult` (with educational `message`, CHAL-05), `VerdictPayload`, `JobPayload` (code + tests + limits ONLY — no env/secrets), `truncateOutput()` with `OUTPUT_LIMIT_CHARS = 10_000`.
2. **Schema additions** — `src/lib/db/schema.ts`: `submissions` (immutable snapshot: userId nullable for anonymous runs, challengeId, code, verdict fields written once, NO updatedAt) and `execution_jobs` (status enum queued→claimed→running→completed/failed, jsonb payload, verdictPayload, claimedBy/At, attempts, hasVerdict, ms-precision created_at, index on (status, created_at)). Migrations 0001 + 0002 generated, committed, applied — 8 tables live.
3. **Queue library** — `src/lib/execution/queue.ts`: `enqueueExecution`, `claimJob` (**FOR UPDATE SKIP LOCKED** inside a transaction, oldest-first, atomic attempts increment), `markRunning`, `completeJob` (mirrors verdict onto the linked submission), `failJob`, `requeueStale` (crash recovery after 2 min, MAX_ATTEMPTS = 3 then failed), `getLatestJobForSubmission`.
4. **Runner worker** — `src/workers/runner.ts` via `pnpm worker`: polls every `POLL_INTERVAL_MS` (default 1000), drains continuously, claims as `runner-<pid>`, never logs payload code/secrets, graceful SIGINT/SIGTERM shutdown with `closeDb()`. Execute hook is injectable (`setExecuteFn`); stub returns "runner not implemented (03-02 pending)".
5. **Worker preload** — `scripts/worker-imports.mjs` + `scripts/worker-resolve-hook.mjs`: loads `.env.local`, stubs `server-only` for both ESM (module.register hook) and CJS (tsx-compiled require) module paths. Next builds keep the real guard.

## Decisions Made

- Raw SQL for claimJob: drizzle's query builder has no FOR UPDATE SKIP LOCKED combinator.
- `server-only` added as a real dependency (0.0.1): vitest and the worker alias it to a stub; the RSC guard still applies in Next builds.
- `execution_jobs.created_at` uses millisecond precision — claim ordering relies on it.
- postgres-js `tx.execute` returns a RowList directly (no `.rows` wrapper) — types handled via `Record<string, unknown>` + cast.

## Verification

- `pnpm typecheck` — 0 errors
- `pnpm lint` — clean
- `pnpm test` — **49/49 passing**, including 7 new queue integration tests (claim ordering, SKIP LOCKED double-claim safety, running transition + verdict write, submission verdict mirror, failJob error record, stale recovery → requeue, attempts cap → failed). Suite skips when Postgres is down (same probe pattern as db.test.ts).
- `pnpm worker` live smoke test: polls ("worker runner-<pid> polling every 1000ms"), exits cleanly on SIGINT.

## Files

- `src/lib/execution/types.ts` (new)
- `src/lib/db/schema.ts` (extended)
- `src/lib/db/migrations/0001_bored_wildside.sql`, `0002_lovely_catseye.sql` (new)
- `src/lib/execution/queue.ts` (new)
- `src/workers/runner.ts` (new)
- `scripts/worker-imports.mjs`, `scripts/worker-resolve-hook.mjs` (new)
- `package.json` (+`worker` script, +`server-only`)
- `src/lib/db/index.ts` (+`closeDb`)
- `vitest.config.ts` (+server-only stub alias)
- `tests/stubs/server-only.ts` (new)
- `tests/unit/db-schema.test.ts` (updated: submissions now phase-3 table; immutability + sequencing guardrails)
- `tests/integration/execution-jobs.test.ts` (new)
- `src/app/(learn)/.../[lessonId]/page.tsx`, `src/server/actions/logout.ts` (pre-existing lint errors fixed: createElement for MDX component, unused redirect import)

## Requirements Covered

CHAL-02 (queue), CHAL-03 (submissions recorded server-side, anonymous runs allowed), PLAT-08 (web tier never executes code).
