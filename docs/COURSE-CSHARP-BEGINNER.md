# Course: C# — Beginner (csharp-beginner)

Date: 2026-09-17 · Status: **COMPLETE**

Track `csharp`, course `csharp-beginner` ("C# — Cơ bản") — **21 modules,
85 lessons** (64 teaching + 21 checkpoint lessons), 21 practice sets,
**105 challenges** (84 practice + 21 checkpoint), ~34 h estimated
(1234 min lessons + 806 min practice + checkpoint minutes). Full EN + VI
parity: 85 lesson MDX × 2 locales (170 mdx-map entries), VI overlays on
every module/practice/challenge; validator reports
`SYNC: EN/VI structures match` and **254 nodes load clean in both
locales**. Id namespace: `csb-` on every id kind. Course registered in
`src/content/tracks/csharp/track.json`; `validate-content.ts` walks it
(`Linear path (csharp): 85 lessons`).

## Verified environment (probed, not assumed)

| Question | Verified answer | Evidence |
| --- | --- | --- |
| .NET SDK in sandbox | **10.0.401** | `dotnet --list-sdks` inside the hardened container |
| Target framework | net10.0 | sandbox project restore |
| Compiler | Roslyn via `dotnet build`/csc, deterministic no-restore compiles | harness staging runs |
| NuGet restore | disabled (offline) — challenges are single-file, BCL-only | runtime job script |
| Test protocol | `Cj.True/Eq/False` assertion prelude compiled with the learner file; verdicts parsed from `RESULT` lines | `src/workers/csharp-runtime.ts` |
| Execution | Docker sandbox, no network, fs-scoped, timeout + memory caps | unit tests cover cap enforcement |

## Module map (21)

1. `csb-welcome` — C# vs .NET, first programs, how grading works
2. `csb-variables` — types, `var`/`const`/null, strings & chars
3. `csb-io` — `Console.ReadLine`, parsing, `TryParse` validation
4. `csb-flow` — operators, conditions, loops, `switch`
5. `csb-methods` — parameters, overloading, decomposition
6. `csb-strings` — string API, immutability, `StringBuilder`
7. `csb-arrays` — indexing, iteration, search/sort basics
8. `csb-collections` — `List<T>`, `Dictionary`, `HashSet`, `Queue`/`Stack`
9. `csb-classes` — fields, properties, constructors, encapsulation
10. `csb-oop` — inheritance, virtual/override, interfaces, composition
11. `csb-records` — records, enums, value vs reference modeling
12. `csb-generics` — generic methods/classes, constraints intro
13. `csb-exceptions` — try/catch/finally, custom exceptions, when *not* to throw
14. `csb-files` — `File`/`Directory`/`Path`, persistence mini-projects
15. `csb-linq` — Where/Select/OrderBy/GroupBy/aggregates, LINQ demystified
16. `csb-delegates` — delegates, lambdas, `Action`/`Func`, events
17. `csb-testing` — debugging, stack traces, assertions, edge cases
18. `csb-cli` — csproj, `dotnet` CLI, solutions, project references
19. `csb-git` — repos, commits, branches, .gitignore, PR concepts
20. `csb-algorithms` — Big-O basics, search, frequency counting, recursion intro
21. `csb-capstone` — Personal Finance Manager milestones (CSV, totals, statements)

## Challenge verification (two-sided, real compiles)

Every challenge carries a reference solution (R) and an intentional
behavioral near-miss (W). `scripts/content-authoring/verify-challenges-csharp.mjs`
compiles and runs both inside the actual sandbox container:

```
challenges: 105
R tests: 207 pass / 0 fail   W tests: 138 fail / 73 pass
challenge verdicts: 105 clean, 0 ref-fail, 0 wrongly-pass
```

Every W fails at least one test (behavioral, not compile-only); every R
passes all of its tests. Note: the runner must be invoked via
`npx tsx …` — Node 22.22.2's `--import tsx/esm` path has a `require(esm)`
cycle regression even for import-free modules.

## QA gates (final tree)

- `tsc --noEmit` — **PASS** (exit 0)
- `pnpm lint` — **0 errors** (pre-existing warnings only)
- `pnpm test` (unit) — **166/166 PASS** across 28 files
- `pnpm build` (production) — **PASS**
- E2E (Playwright) — **36/36 PASS** incl. axe-core WCAG 2.1 AA audits, mobile viewports, keyboard operability
- `validate-content.ts` — SYNC PASS; EN 254 nodes clean; VI 254 nodes clean
- mdx-map — regenerated; 170 `csharp-beginner` entries (85 EN + 85 VI)

## Shared-infrastructure changes (smallest compatible)

- `scripts/content-authoring/validate-content.ts` — added `csharp` to the
  validator's `COURSE_TRACKS` (single-line list addition; also carries
  other agents' concurrent rewrite, untouched).
- No other shared files modified by this course's work.

## Known limitations

- NuGet/network offline by design → challenges use BCL-only APIs.
- Console-input challenges are graded as pure functions/prints (no
  interactive stdin in the grading harness).
- Filesystem challenges stage under temp dirs created by the tests.

## Authoring pipeline

Source-of-truth scripts in `scripts/content-authoring/`:
`csb.py` (shared prelude/helpers), `csb_m1.py`…`csb_m21.py` (per-module),
`csb_course.py` (course manifest), `verify-challenges-csharp.mjs`
(two-sided harness), `csharp-beginner-solutions.mjs` (generated R/W
ledger, 105+105 entries).
