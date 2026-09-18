# Phase 25 — Course: C# — Beginner — SUMMARY

Date: 2026-09-17
Status: **COMPLETE**

## Course

Track `csharp`, course `csharp-beginner` ("C# — Cơ bản") — **21 modules,
85 lessons** (64 teaching + 21 checkpoint lessons), 21 practice sets,
**105 challenges** (84 practice + 21 checkpoint), ~34 h estimated
(1234 min lessons + 806 min practice + checkpoint minutes). Full EN + VI
parity (85/85 lesson MDX × 2 locales = 170 mdx-map entries; VI overlays
on every module, practice set, and challenge — validator:
`SYNC: EN/VI structures match`, EN 254 nodes clean, VI 254 nodes clean).
Id namespace: `csb-` on every id kind. Course registered in
`src/content/tracks/csharp/track.json` (first course in the new csharp
track; validator walks it: `Linear path (csharp): 85 lessons`).

Arc (spec in docs/COURSE-CSHARP-BEGINNER.md — 21 modules): C# vs .NET
and first programs → variables/types → console I/O with `TryParse`
validation → control flow → methods → strings/`StringBuilder` → arrays
→ collections → classes/encapsulation → OOP (virtual/override,
interfaces, composition) → records/enums/value-vs-reference → generics
intro → exceptions (when *not* to throw) → files/persistence → LINQ
(demystified) → delegates/lambdas/events → debugging & testing → .NET
CLI/csproj/solutions → git workflow → algorithms (Big-O basics, search,
frequency counting, recursion intro) → capstone Personal Finance
Manager (records + collections + LINQ + file persistence, milestone
broken).

## Toolchain (verified in the sandbox, not assumed)

- .NET SDK **10.0.401**, target `net10.0`, Roslyn compiles, NuGet
  restore disabled (offline) — challenges are single-file, BCL-only.
- Test protocol: `Cj.True/Eq/False` prelude compiled with the learner
  file; verdicts parsed from `RESULT` lines (`src/workers/csharp-runtime.ts`).
- Runner must use `npx tsx …`: Node 22.22.2's `--import tsx/esm` path
  has a `require(esm)` cycle regression even for import-free modules
  (diagnosed 2026-09-16).

## Verification (two-sided, real compiles in the Docker sandbox)

Reference (R) and intentionally-wrong (W) solutions for all 105
challenges, ledger `csharp-beginner-solutions.mjs` (105 R + 105 W,
unique). Final clean-ledger sweep, nothing else running:

```
challenges: 105
R tests: 207 pass / 0 fail   W tests: 138 fail / 73 pass
challenge verdicts: 105 clean, 0 ref-fail, 0 wrongly-pass
```

Every R passes all its tests; every W fails ≥1 test (behavioral
near-misses, not compile-only). Deterministic defects found and fixed
during verification (notable): m11 money test calling `Solution.Money.Add`
on a static defined outside the record; m12 pairstore W behaviorally
identical on modern runtimes (replaced with an honest defect); m14–m17
checkpoint test/contract drift (`int[]` vs `List<int>`, missing
`Directory.CreateDirectory`, case-insensitive region merge contract,
averager contract vs prompt); m18 checkpoint R/test contradiction
("transitively depend" spec) and W diamond-graph discriminator; m21
checkpoint year-ignoring W plus missing capstone boilerplate
(`Transaction`/`Direction`/`AddResult`) on the checkpoint prelude.

## Gates

- Curriculum validation (`validate-content.ts`): PASS — SYNC match; EN
  254 nodes; VI 254 nodes; unique ids; all challenges resolve.
- Typecheck (`tsc --noEmit`): PASS (exit 0).
- Lint: 0 errors (pre-existing warnings only).
- Unit tests: **166/166 PASS** across 28 files.
- Build (`pnpm build`): PASS.
- E2E: **36/36 PASS** (axe-core WCAG 2.1 AA audits, mobile viewports,
  keyboard operability).
- Full two-sided challenge harness: **105/105 clean** (see above).

## Parallel-work preservation

- C Beginner / C Intermediate / C Advanced, C++ tracks, Java tracks:
  untouched. The mid-run VI-overlay validator blocker was an untracked
  file owned by the C Advanced agent (VI summary >200 chars); I did not
  touch it and verified my VI content with a scoped schema walk instead.
  That file was subsequently fixed by its owner; the global validator
  now loads all tracks clean.
- Shared files carrying concurrent work (`validate-content.ts` rewrite,
  `generate-mdx-map.mjs` VI sidecars, `verify-challenges.mjs`): my only
  addition is the one-line `csharp` entry in the validator's track list.
- No destructive git commands used; no other agent's changes staged or
  committed.

## Files

- `src/content/tracks/csharp/**` — track, course, 21 modules, 85
  lessons × 2 locales, 21 practices, 105 challenges, 21 checkpoints.
- `scripts/content-authoring/` — `csb.py`, `csb_m1.py`…`csb_m21.py`,
  `csb_course.py`, `verify-challenges-csharp.mjs`,
  `csharp-beginner-solutions.mjs` (generated ledger).
- `scripts/content-authoring/validate-content.ts` — +csharp in track list.
- `src/lib/curriculum/mdx-map.ts` — regenerated (170 new entries).
- `docs/COURSE-CSHARP-BEGINNER.md` — course doc.

## Known limitations

- BCL-only APIs (offline NuGet by design); console-input challenges
  graded as pure functions/prints; filesystem challenges stage under
  temp dirs the tests create.
- ~600 uncommitted parallel-agent files remain in the tree (preserved;
  commit strategy is the user's call).
