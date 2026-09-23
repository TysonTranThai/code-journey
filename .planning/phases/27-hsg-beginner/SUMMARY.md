# Phase 27 — Course: Tuyển Học Sinh Giỏi Tin học — Beginner — SUMMARY

Date: 2026-09-18
Status: **COMPLETE**

## Course

Track `hsg`, course `hsg-beginner` ("Tuyển Học Sinh Giỏi Tin học — Cơ
bản") — a NEW course type: Vietnamese high-school **competitive
programming** preparation (Học sinh giỏi Tin học), distinct from the
normal `cpp` curriculum. **20 modules, 65 lessons** (60 teaching + 5
contest-strategy + 25 checkpoint lessons... structure: 3 lessons/module
× 19 + 8 in the contest module), **20 practice sets, 127 challenges**
(102 practice + 25 checkpoint, including 3 graded mock contests / 6
contest problems), ~33.4 h estimated (932 lesson minutes + 1070
practice minutes). Full EN + VI parity: 130 lesson MDX (65 × 2
locales), VI sidecar JSON on every module/practice/challenge —
validator: `SYNC: EN/VI structures match`, 253 nodes load clean per
locale. Id namespace `hsg-` on every id kind.

Arc (spec in docs/COURSE-HSG-BEGINNER.md): contest-statement reading +
verdict taxonomy → loops as simulation → arrays → mảng đánh dấu / đếm
phân phối → greedy with proof sketches → sorting/comparators/ranking →
binary search on answer → prefix sums (1D/2D) → difference arrays →
strings → basic number theory → STL-for-contests → recursion →
backtracking → DP basics (state/transition/base/order) → graphs (BFS/
DFS/components/grid) → two pointers & sliding window → contest
technique (complexity budgeting, subtasks, partial scoring) →
debugging broken submissions → Beginner Contest Series (3 mock
contests). Problem statements mirror the real format (Tên bài / Mô tả /
Dữ liệu vào / Dữ liệu ra / Giới hạn / Ví dụ / Subtask); all problems
original.

## Toolchain (probed in the sandbox, not assumed)

g++ 14.2.0 (Alpine), `-std=c++20`, `-Wall -Wextra -Wpedantic`, **no
-O2** at test compile, `bits/stdc++.h` compiles (~1.3 s/TU), 20 s
per-submission job budget (30 s ceiling), 512 MB, network off. Every
constraint ceiling is sized for the intended complexity at -O0 —
constraints are honest teaching data. Details in
docs/CURRICULUM-RESEARCH-HSG-BEGINNER.md.

## Verification (two-sided, real compiles in the Docker sandbox)

Reference (R) and intentionally-wrong (W) solutions for all 127
challenges in `hsg-beginner-solutions.mjs`, deduped keep-last. Final
parallel sweep (20 practice + 10 checkpoint filters, all exit 0):

```
challenges: 127
R tests: 560 pass / 0 fail
W tests: 285 fail / 275 pass  → every W fails ≥1 test, none hang
```

Every W fails for a behavioral, discriminating reason (greedy trap,
stale-visited DFS query, ascending knapsack loop reusing an item,
directed-graph BFS misread, truncate-vs-floor modulo…) — never
compile-only, never timeout-only, never a no-op near-miss. Notable
defects caught and fixed during authoring: wrong self-authored
expectations (palindrome counts, rank outputs, waiting-time sample),
doubled-`\n` escape class in early test I/O (root-caused; later
modules use the T()/cpp() discipline that eliminated it), 2-tuple
solution entries missing W bodies (M7 rebuild), near-misses provably
equivalent to R (flood right/down-only, treecheck self-loop,
presents greedy) replaced with real discriminators.

## Gates

- Curriculum validation (`validate-content.ts` + one-line
  `hsg-beginner` track entry): PASS — SYNC match; 253 nodes × 2
  locales; linear path 65 lessons.
- `pnpm content:map`: regenerated; 130 HSG entries in mdx-map.ts.
- Typecheck (`tsc --noEmit`): PASS. Lint: 0 errors (pre-existing
  warnings only). Unit tests: **184/184 PASS** (28 files).
- Build (`pnpm build`): PASS.
- E2E: NOT re-run this session — the Next 16 dev-server lock held by a
  concurrent agent's `next dev` (:3000) makes any second `next dev`
  exit 1 before Playwright's 60 s window. Last full E2E on this tree:
  36/36 (Phase 25). All content gates are E2E-independent.

## Parallel-work preservation

- Only HSG-owned files created/edited: `src/content/tracks/hsg/**`,
  `scripts/content-authoring/hsg*`, `docs/COURSE-HSG-BEGINNER.md`,
  `.planning/`.
- Shared-infrastructure change: exactly one line — the validator track
  entry. mdx-map generator auto-discovers tracks (no registry edit).
- Sibling-agent interactions: the C# Intermediate (Phase 26) agent
  repaired a minutes→difficulty arg-shift in 6 of my early lesson JSONs
  (verified theirs; preserved, not reverted) and removed my orphaned
  pre-rename `hsg-cp18-scoreline` checkpoint JSON in commit 25d9de3;
  course-agent commits landed mid-run while my work was uncommitted —
  re-verified from clean-tree HEAD that all 598 hsg content files, 20
  authoring scripts, the ledger, the validator row, and mdx-map entries
  are present. No destructive git commands; no other agent's work
  staged or committed by me.

## Files

- `src/content/tracks/hsg/**` — track, course, 20 modules, 65 lessons
  × 2 locales, 20 practices, 127 challenges, 25 checkpoints.
- `scripts/content-authoring/` — `hsg.py`, `hsg_m1.py`…`hsg_m20.py`
  (per-module generators), `verify-challenges-hsg.mjs`,
  `hsg-beginner-solutions.mjs` (generated R/W ledger),
  `_hsg_local_verify.py`, `_sync_hsg_manifest.py`.
- `scripts/content-authoring/validate-content.ts` — +hsg track row.
- `src/lib/curriculum/mdx-map.ts` — regenerated (130 new entries).
- `docs/COURSE-HSG-BEGINNER.md`,
  `docs/CURRICULUM-RESEARCH-HSG-BEGINNER.md`.

## Known limitations

- Offline single-job sandbox: batch-format problems only (as real
  judges), ≤4 tests/challenge (per-test compile cost), no sanitizer
  runs in graded tests (UB taught via prose + honest near-misses).
- Beginner boundary honored: no segment/Fenwick trees, Dijkstra, DSU,
  advanced strings/DP — reserved for HSG Intermediate/Advanced.
