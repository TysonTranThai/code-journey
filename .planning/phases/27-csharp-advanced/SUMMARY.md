# Phase 27 — Course: C# — Advanced — SUMMARY

Date: 2026-09-18
Status: **COMPLETE**

## Course

Track `csharp`, course `csharp-advanced` ("C# — Advanced" / "C# — Nâng cao") —
**23 modules, 110 lessons** (87 teaching + 23 checkpoint lessons), **23
practice sets**, **78 challenges** (55 practice + 23 checkpoint tasks),
full EN + VI parity (scoped validator: both locales load clean through the
public loaders, 258 nodes each, structures match). Id namespace: `csa-` on
every id kind. Course registered third in
`src/content/tracks/csharp/track.json` after `csharp-intermediate`.

Arc (spec in docs/COURSE-CSHARP-ADVANCED.md): advanced language semantics →
memory & object model → advanced generics → delegates/closures → reflection
→ attributes → Roslyn → source generators → expression trees → advanced
async → concurrency → parallel → channels → GC → performance engineering →
runtime internals → diagnostics → unsafe/interop → NativeAOT & deployment →
networking → data access → distributed systems → security → production
architecture + capstone. No projects directory exists in the loader schema
(an inspected limitation); project briefs are delivered as lessons/practice
challenges instead (documented in docs/COURSE-CSHARP-ADVANCED.md).

## Environment (probed, not assumed)

- Sandbox: `codejourney-sandbox` image (docker/Dockerfile.sandbox), no
  network, hardened flags. .NET SDK inside image; `dotnet-script` not used.
- Execution path: production `buildCSharpJobScript` compiles with
  `csc.dll` + ref packs + SDK Roslyn assemblies as `-r:` references and
  `-unsafe`. Loopback TCP/UDP, in-process Roslyn, unsafe pointers, PBKDF2,
  Channels, and ArrayPool all verified by probe before use.
- NativeAOT and external infrastructure are NOT available in the sandbox;
  those topics are taught conceptually / simulated deterministically.

## Shared runtime change (cross-course impact, verified safe)

`src/workers/csharp-runtime.ts` (shared C# test harness):

1. Async test support: tests containing `await` are wrapped in an `async
   Task<int> Main`; sync tests keep byte-identical output (Beginner/Inter/
   mediate unaffected).
2. Roslyn assembly resolver via `[ModuleInitializer]` so tests using
   Roslyn types bind at load (production compiles without dlls beside exe).
3. Roslyn `using`s are emitted only when test code references Roslyn
   types — prevents CS0234 in jobs compiled without `-r:` Roslyn refs.

**Beginner regression: 105/105 clean (207 ref tests pass, 138 wrong-side
fails)** with the upgraded harness — restored after the intermediate
"unconditional usings" break was found and fixed. Intermediate unaffected
(no Roslyn/async usage changes output).

## Verification evidence

- Two-sided sandbox verification (`verify-challenges-csharp-advanced.mjs`,
  unique staging dir `csharp-verify-advanced`): **78/78 clean** — every
  reference solution passes all **128** tests; every wrong solution fails
  at least one test (**94 wrong-side test failures** recorded). Zero
  ref-fails, zero vacuous passes.
- Notable content bugs caught by the harness and fixed: Amdahl break-even
  (5× @ S=0.1 ⇒ 9 cores, not 13), constant-folding test that the C#
  compiler constant-folds at compile time (now builds trees via explicit
  `Expression.*` calls), invented `ArrayPoolExtensions` API, `SpinWait.
  SpinBetween` (real API: `Thread.SpinWait`), attribute-suffix resolution
  (`[Gen2]` → `Gen2Attribute`), `Lazy<int>` factory typing, echo-server
  deadlock, LE byte order, and 14 non-discriminating wrong solutions
  replaced with deterministic semantic contracts (no timing flakiness).
- Scoped content validation (`validate-content-csa.ts`, isolated course
  copy so other agents' in-flight state never blocks this QA): EN + VI
  clean, all loaders, both locales.
- Typecheck: `tsc --noEmit` exit 0. Lint: 0 errors, 0 warnings.
- Unit/integration: **184/184 tests, 28 files** (`pnpm test`).
- E2E: not run in this session (shared dev-port constraints, consistent
  with Phases 25/26 practice); unit + scoped validator + live harness
  cover course integrity.

## Cross-agent safety

Work committed in phases by the user/operator. Final tree: only
`scripts/content-authoring/verify-challenges-csharp-advanced.mjs` carried a
one-line lint fix uncommitted (unused destructured variable →
`selected.keys()`); all other files committed. C# Beginner preserved: YES.
C# Intermediate preserved: YES. C/C++/Java/Python/Web tracks untouched:
YES. Deployment/infra untouched: YES. No destructive git commands used.

## Files (owned)

- `src/content/tracks/csharp/courses/csharp-advanced/**` (691 files: course
  + 23 modules, 110 lessons ×2 locales, 23 practice sets, 78 challenges ×2)
- `src/workers/csharp-runtime.ts` (shared harness — see above)
- `scripts/content-authoring/csa*.py` (emitter, 23 content modules, VI
  overlays, scratch patch scripts)
- `scripts/content-authoring/verify-challenges-csharp-advanced.mjs`
- `scripts/content-authoring/validate-content-csa.ts`
- `docs/COURSE-CSHARP-ADVANCED.md`, `docs/CURRICULUM-RESEARCH-CSHARP-ADVANCED.md`
