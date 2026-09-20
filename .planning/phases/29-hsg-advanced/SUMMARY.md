# Phase 29 — HSG Advanced (Tuyển Học Sinh Giỏi Tin học — Nâng cao) — SUMMARY

**Status: COMPLETE (2026-09-20)** · Track `hsg` · Course `hsg-advanced` · Prereq `hsg-intermediate`

## What was built

The third and highest course in the HSG competitive-programming track: 20 modules,
83 lessons (54 teaching + 17 module checkpoints + 12 contest checkpoints), 20 practice
sets, 92 challenges (63 practice + 29 checkpoint), fully bilingual (EN + VI), ~77 h
estimated. Registered on the `hsg` track after `hsg-intermediate` in
`src/content/tracks/hsg/track.json` (+ `track.vi.json`).

## Course shape

1. **Advanced attack patterns** — meet-in-the-middle, XOR invariants, construction
2. **Lazy segment trees** — range-assign/range-max lazy propagation
3. **Fenwick variants & offline power** — range-update point-query, offline sweeps
4. **Binary lifting & LCA** — 2^k tables, kth-ancestor, path sums
5. **Euler tour queries** — tin/tout, subtree aggregates
6. **Tree DP** — take/skip, rerooting, matching
7. **Heavy-light decomposition** — chain path queries
8. **SCC** — Tarjan, condensation, 2-SAT
9. **Max flow & matching** — Dinic, König
10. **Digit DP** — tight/free states, divisibility counting
11. **Interval DP** — merges, balloons, expected values
12. **String structures** — rolling hash, Z, suffix arrays
13. **Number theory II** — extended Euclid, CRT, Möbius, phi, Miller–Rabin
14. **Combinatorics** — inverses, stars & bars, Catalan, inclusion–exclusion
15. **Computational geometry** — hull (Andrew), shoelace, orientation
16. **Technique synthesis** — multi-technique composites
17. **Debugging under contest load** — RE/WA/TLE triage, stress-testing
18–20. **Contest Series I–III** — 2 strategy lessons + 4-checkpoint 120-minute mock
   contests each, following the `hsgi-contests` shape

## Verification

- **92/92 two-sided clean** in the real container (per-module foreground batches of
  `scripts/content-authoring/verify-challenges-hsga.mjs`); every solution passes its
  full reference suite, every wrong solution fails ≥ 1 test.
- Ledger ↔ emitted content mirror: 92/92 R/W bodies match
  `hsg-advanced-solutions.mjs` (after dedupe fix).
- Research doc: `docs/CURRICULUM-RESEARCH-HSG-ADVANCED.md`; course spec:
  `docs/COURSE-HSG-ADVANCED.md`.
- QA gates: curriculum unit tests 48/48, full unit suite 184/184, typecheck 0,
  lint 0 errors (8 pre-existing warnings elsewhere), production build PASS,
  E2E 36/36 (Postgres + Docker started locally for the run; earlier failures were
  infra-only).

## Defects found & fixed during the build

- **8 orphaned checkpoint lessons** (`hsga-cp-m10` … `hsga-cp-m17`): files existed on
  disk but were not referenced in their `module.json`; the loader loads refs only, so
  they were unreachable. Refs added; curriculum suite re-verified green.
- **Local verifier binding bug**: `_hsg_local_verify.py` bound only the last
  checkpoint's solution/wrong to every bodyless challenge in multi-checkpoint modules
  (false negatives in contest modules). Fixed to bind per challenge id, including
  variable-held `challenge()` results.
- **MDX compile gates**: prose `{…}` and bare `<` outside code fences across the
  course escaped (23 + 6 lines, 19 files); course descriptions shortened under the
  loader's 400-char schema cap.
- Numerous ground-truth corrections caught by double-checked models before emit
  (e.g. `C(50,25) mod p`, digit-DP suffix sign, hull closing edge, KMP border counts).

## Notes

- Detached background runs die with session restarts on this machine; the full-course
  sweep was therefore run as per-module foreground batches (40 id-family filters,
  each reported 0 not-clean).
- Pre-existing uncommitted work by other agents (C# verifier tweak, landing a11y pair
  `LandingLoader.tsx` + `dictionaries.ts`) left untouched.
