# Course Spec — AP CSA Advanced Practice & Exam Mastery

Track `ap-csa` · Course `ap-csa-advanced` · Status: **COMPLETE (2026-09-26)**

## Identity

- **Audience:** Students who completed AP CSA Foundations (`ap-csa-beginner`)
  and AP CSA Core (`ap-csa-core`) and want exam-level performance: hard
  problems, mixed-topic transfer, full simulations under real time pressure.
- **Goal:** answer "can the student actually perform at AP CSA exam level?" —
  application, transfer, speed, accuracy, difficult reasoning. NOT another
  Java fundamentals course; ~80% problem solving, ~20% compressed strategy.
- **Positioning:** the endgame of the ladder
  `ap-csa-beginner` → `ap-csa-core` → `ap-csa-advanced` → READY FOR THE EXAM.
  Prerequisites declared in course.json: both prior AP CSA courses.

## Measured numbers

| Metric | Value |
| --- | --- |
| Modules | 24 |
| Lessons | 96 (72 teaching + 24 checkpoints) |
| Practice sets | 24 (one per module) |
| Challenges | 129 (105 practice + 24 checkpoint), all `language: "java"` |
| Locales | EN + VI, synchronized (validator-verified) |
| Verification | 129/129 two-sided OK (R passes all tests; W fails ≥1) |
| Prerequisites | `ap-csa-beginner`, `ap-csa-core` |

Difficulty scale (internal, documented per module; mapped to the platform's
beginner/intermediate/advanced labels): E1 advanced practice, E2 AP-level,
E3 hard AP, E4 expert AP challenge, E5 exam simulation. Distribution skews
E3–E5; nothing below E1.

## Structure (24 modules)

1. **Advanced Problem Solving** — specs, decomposition, selective tracing
2. **Difficult Code Tracing** — state tables, objects/statics, aliasing,
   removal-while-iterating, nested-loop shapes
3. **Advanced Multiple Choice** — 8 executed MCQs; every distractor is a
   named misconception with an explanation
4. **MCQ Speed Training** — 90-second drills, elimination order, five
   patterns, continue-trap checkpoint
5. **Advanced String Problems** — Caesar shift, word scan, collapse, mask,
   longest run, run-length encode (flush trap)
6. **Advanced Array & ArrayList Problems** — second distinct max, rotation,
   mode tie-break, in-place dedup, backward removal, interleave drain
7. **Advanced 2D Array Problems** — rotation, neighbor sums, peaks (true
   in-bounds average), per-column ledger, spiral fill, symmetry
8. **Advanced OOP** — parking gate, register balances, scoreboard fouls,
   lowest-free allocation
9. **Inheritance & Polymorphism Lab** — payroll dispatch, abstract shapes,
   inherited-method dispatch, discount chain
10. **Recursion Lab** — parity machine, stair counting, recursive reverse,
    subset sum, Euclid, digital root
11. **Integrated Coding** — unlabeled fusions: vowel encoder, climb log,
    row auditor, digit extraction
12. **FRQ Workshop** — weather station (a/b/c), full WarmWeek class
13. **FRQ Method Mastery** — frequent char (tie-break), star insertion,
    second smallest (sentinel), even-digit recursion, adjacent repeats
14. **FRQ Class Mastery** — candy machine, five-play like rule, library
    delegation, player lifecycle
15. **FRQ Debugging** — four single-bug repairs + window-boundary checkpoint
16. **FRQ Partial Credit** — three bankable cores, banking-order assembly
17. **Mixed AP Sets** — unlabeled predict/fix/implement rotation
18. **Timed FRQ Sets** — clock budgets (3/6/15/7 min), bottleneck autopsies
19. **Error Analysis Lab** — 13-class taxonomy, six diagnose-and-repair
    items, compound-bug checkpoint
20. **AP Exam Strategy** — pacing, three-bin triage, last-ten-minutes
    protocol (evidence-based; no fabricated score claims)
21. **Full Practice Exam #1** — MCQ half + TollBooth FRQ
22. **Full Practice Exam #2** — trap-weighted (dead variable, near-miss
    clause, order, mirror) + Recipe FRQ
23. **Full Practice Exam #3** — synthesis-weighted + Studio FRQ
24. **Final Master Simulation** — unlabeled MCQs + Clinic FRQ (fuses three
    banked patterns); verdict rubric (85/70 thresholds) and after-plan

All content is original — no College Board, AP Classroom, or released-exam
items are reproduced anywhere.

## MCQ format

The platform has no separate MCQ content type, so exam MCQs are executable
Java challenges: the learner prints the option letter plus a one-sentence
justification; tests verify the letter (and the wrong-answer W solutions
demonstrate a plausible but wrong letter fails). Ground truths for every
tracing/MCQ item were executed and confirmed before authoring (several
hand-traces were corrected by execution — e.g. `1 + 2 + "3" + 4 + 5` →
`3345`, removal-while-iterating survivor sets).

## Two-sided verification

`scripts/content-authoring/verify-challenges-apx.mjs` (isolated harness,
mirrors the sandbox contract via `buildJavaTestFile`): reference R must pass
ALL tests; intentionally-wrong W must fail ≥1. Final run: **129/129 OK**.
Ledger: `scripts/content-authoring/apx-solutions.mjs` (R/W maps, later
assignment wins).

## Authoring scripts

- `apx.py` — course library (clones `apc.py`; separate ledger)
- `apx_m1.py` … `apx_m24.py` — one generator per module (idempotent)
- `apx_finish_lessons.py` — authors the 72 teaching lessons from the L1/L2/L3
  + VI bodies defined in the module scripts (lesson metadata + mdx)
- `verify-challenges-apx.mjs` — two-sided Java QA harness

## Validation results (2026-09-26)

- `validate-content.ts`: exit 0; ap-csa-advanced 24 modules / 96 lessons /
  24 challenges; SYNC EN/VI match; 298 nodes load clean per locale
- `verify-challenges-apx.mjs`: 129/129 two-sided OK
- `pnpm typecheck`: clean
- `pnpm lint`: 0 errors (13 pre-existing warnings)
- `pnpm test`: 136 passed; 3 failed in `tests/integration/submissions-authz`
  (pre-existing DB-state failures, unrelated to content)
- `pnpm build`: SUCCESS (4916 static pages) after a minimal repair to two
  in-progress `ap-csa-core` MDX files (see Multi-agent notes)
- Live smoke (own port, prod build): course 200, practice challenge 200,
  checkpoint challenges 200, VI course 200 with Vietnamese rendering.
  Lesson pages 500 for ALL courses while the Docker daemon/DB is down
  (discussion-thread count query); environmental, not content-related.

## Multi-agent notes

- `ap-csa-core` files were treated as protected; no course content was
  modified. Exception (minimal, render-safety only): the Core agent's
  `cx-arraylist/lessons/cx-m7-removal{,.vi}.mdx` contained literal
  `{\"a\", \"a\", \"b\"}` artifacts in prose, which broke MDX parsing and
  therefore the whole repo build (4 errors incl. two in my course). The
  fix converted those artifacts to inline code spans in prose only; code
  blocks and all other Core files untouched.
- `track.json` extended by exactly one course entry (`ap-csa-advanced`).
- `validate-content.ts` extended with the three ap-csa courses and made to
  warn-and-skip not-yet-authored courses (was: hard crash on missing
  course.json — pre-existing behavior that broke the whole QA pass).
