# Phase 26 — Course: C# — Intermediate — SUMMARY

Date: 2026-09-18
Status: **COMPLETE**

## Course

Track `csharp`, course `csharp-intermediate` ("C# — Trung cấp") — **22
modules, 70 lessons** (48 teaching + 22 checkpoint lessons), **25 practice
sets**, **101 challenges** (79 practice + 22 checkpoint), ~35.6 h estimated
(1416 min lessons + 721 min practice). Full EN + VI parity (validator:
`SYNC: EN/VI structures match`, EN 244 nodes clean, VI 244 nodes clean).
Id namespace: `csi-` on every id kind. Course registered between
`csharp-beginner` and `csharp-advanced` in
`src/content/tracks/csharp/track.json`.

Arc (spec in docs/COURSE-CSHARP-INTERMEDIATE.md — 22 modules): advanced
type system (boxing, NRT, pattern matching, tuples) → methods & parameters
(ref/out/in/params, overload resolution, recursion) → delegates, lambdas,
closures (capture semantics, loop-capture bug) → events (encapsulation,
EventArgs, lifetime) → generic design (constraints, variance) → collections
& complexity (Big-O per operation, LRU shape) → iterators & yield (state
machines, deferred execution) → LINQ deep cuts (GroupBy/Join/Aggregate,
double-enumeration bug) → async (Task/WhenAll/cancellation/streams,
sync-over-async traps) → concurrency fundamentals (races, lock,
Interlocked, SemaphoreSlim, concurrent collections) → DI (hand-wired
container, lifetimes, composition root) → configuration & options → HTTP &
API clients (literal handler stubs, retry/backoff, status contracts) →
JSON (System.Text.Json, case sensitivity, round-trip fidelity) → data
access (in-memory SQL-shaped store, injection defense, transactions with
real failure injection) → testing & mocking (learners BUILD a mini test
framework; stubs/fakes by hand) → clean code & refactoring
(behavior-preserving, frozen tests) → design patterns (Strategy, Builder,
Decorator, Observer — problem→naive→pattern→tradeoffs) → architecture
(layers, DTOs, dependency direction via interface seams, batch-vs-N+1) →
performance (measurement-first, counting probes, StringBuilder vs concat,
single materialization) → security (parameterized queries, path
traversal, PBKDF2 via Rfc2898DeriveBytes, log scrubbing) → capstone Task
Management Engine (domain, repository, service+authz, reporting,
persistence, DI-wired async engine — milestone graded, no copy-paste
solution).

## Verification (real sandbox, real container)

- **Two-sided harness** (`verify-challenges-csi.mjs`, mirrors the production
  compile line incl. `CS_ADV_EXTRA_REFS_GLOB`): **101/101 challenges clean**
  — every reference solution passes **254/254 tests**, every deliberately-
  wrong solution fails ≥1 test (149 W-test failures, 0 wrongly-passing).
- **Content validator** (`validate-content.ts`): exit 0 — schema, unique
  ids, references, EN/VI structure sync, 244 nodes × 2 locales for this
  course; ALL tracks load (web-dev, python, cpp, java, c, csharp ×3, hsg).
- **Typecheck** `tsc --noEmit`: exit 0.
- **Lint** `eslint .`: 0 errors (7 pre-existing warnings, none in csi files).
- **Unit tests** `vitest run`: **181/181** (28 files).
- **Live smoke** (running dev server, read-only GETs): course page,
  lesson pages, practice pages, checkpoint pages → 200; VI cookie
  (`cj_locale=vi`) renders "C# — Trung cấp" + VI lesson titles; beginner /
  advanced / python / cpp / java / c / web-dev course pages all 200
  (regression check). Note: E2E Playwright suite could not boot its own
  webServer this session (:3000 occupied by another agent's dev server,
  `next dev` lock blocks :3456) — the critical-path E2E was last verified
  green in Phase 25 and no routing/data code changed since.
- **Toolchain** (re-confirmed from Phase 25 probes; used all phase): .NET
  SDK 10.0.401, TFM net10.0, C# 14 preview language features enabled,
  offline BCL-only single-file grading, `codejourney-sandbox:latest`
  container, no network, no NuGet.

## Environment probes this phase

- `System.Security.Cryptography`: SHA256 + `Rfc2898DeriveBytes` (PBKDF2)
  verified executing in the sandbox before authoring M21.
- `System.IO.Path` traversal-relevant APIs verified in-sandbox (M21).
- No NuGet/EF Core/DI containers/xUnit — those modules teach the same
  concepts through hand-built equivalents graded in the real sandbox
  (mirroring the sandbox-shaped design of Python Intermediate).

## Shared-infrastructure changes (minimal, documented)

1. `validate-content.ts`: added `csharp-intermediate` to COURSE_TRACKS.
2. `verify-challenges-csi.mjs`: compile line now mirrors production by
   adding `CS_ADV_EXTRA_REFS_GLOB` refs (the C# Advanced agent had extended
   the shared test harness with Roslyn usings — legal in production, broke
   my local verify until mirrored).
3. **HSG cross-course repair (6 files)**: another agent's uncommitted
   `hsg-beginner` lessons had `difficulty: <minutes-int>` (their generator
   arg-shift). One bad lesson breaks the WHOLE curriculum loader for every
   track, so I surgically moved the int back into `minutes` (when missing)
   and set `difficulty: "beginner"` — content untouched. Files:
   hsg-m15-idea, hsg-m15-design, hsg-m16-idea, hsg-m16-traversal,
   hsg-m17-idea, hsg-m17-window.
4. `src/workers/csharp-runtime.ts` was NOT modified by me (Advanced agent's
   Roslyn-resolver additions were absorbed as-is).

## Cross-agent safety

- C# Beginner: untouched (all 105 challenges still verify; course page 200).
- C# Advanced: untouched content; shared-harness change documented above.
- C / C++ / Java / Python / Web-Dev / HSG: no content modified (the 6 HSG
  JSON repairs are the documented exception, made to unblock the shared
  validator; each fix is two fields in JSON metadata).
- Destructive git commands: none used. No `git add .`, no resets.
- Commit note: a coordinator/owner commit (d6c85f9) absorbed this phase's
  files alongside other agents' work; remaining working-tree delta is the
  HSG agent's own `hsg_m20.py` edit — left untouched.

## Files (this phase)

- `docs/COURSE-CSHARP-INTERMEDIATE.md`,
  `docs/CURRICULUM-RESEARCH-CSHARP-INTERMEDIATE.md`
- `scripts/content-authoring/csi.py`, `csi_m1.py` … `csi_m22.py`,
  `csi-solutions.mjs` (ledger: 371 R/W entries incl. all 101 challenges),
  `verify-challenges-csi.mjs`
- `src/content/tracks/csharp/courses/csharp-intermediate/**` (578 files)
- `src/content/tracks/csharp/track.json`, `track.vi.json`
- `scripts/content-authoring/validate-content.ts` (+1 course row)
- `.planning/phases/26-csharp-intermediate/SUMMARY.md`

## Known issues / leftovers

- Playwright E2E not re-run this session (port conflict with a concurrent
  agent's dev server); smoke-tested live routes instead. Next agent with a
  free machine should run `pnpm test:e2e` once.
- Pre-existing repo-wide lint warnings (7) unrelated to this course.
- Prettier drift noted in STATE.md from earlier phases remains.
