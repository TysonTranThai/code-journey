# Phase 32 — HSG Intensive (hsg-intensive) — SUMMARY

**Status: COMPLETE (2026-09-22)** — subject to one cross-agent caveat (below).

## What shipped

A new fourth stage for the HSG THPT track: `src/content/tracks/hsg/courses/hsg-intensive/`.

- **12 modules · 32 lessons (12 checkpoints) · 79 challenges (EN + VI)**, all
  executable C++20 (reference + deliberate-wrong pairs) verified in the real
  sandbox; levels: 39 combination / 23 independent / 15 debugging / 2 real-world.
- Practice-heavy philosophy: ~20% review / 80% problem solving — recognition
  drills, constraint→algorithm budget arithmetic, key-observation training,
  tool-combination problems, a wrong-solution clinic, differential stress
  testing, subtask strategy, self-timed sprints, hidden-topic mixed sets, two
  original 3-problem mock contests + final-simulation checkpoint, editorial
  protocol with re-solve/variation training, and a final challenge pack with
  capstone and reference-pack lesson (selection guides, complexity cheat sheet).
- Authoring: `scripts/content-authoring/hsgx.py` + `hsgx_m1.py … hsgx_m12.py`
  (emit with in-file ground-truth asserts); solutions ledger
  `hsg-intensive-solutions.mjs`; harness `verify-challenges-hsgx.mjs`;
  scoped validator `validate-content-hsgx.ts`.
- Registration: one additive row in `src/content/tracks/hsg/track.json`
  (placed after the other agent's `hsg-mastery` entry, preserved verbatim).
- Docs: `docs/COURSE-HSG-INTENSIVE.md`,
  `docs/CURRICULUM-RESEARCH-HSG-INTENSIVE.md` (written earlier this phase).

## Verification evidence

- **Two-sided harness:** 79/79 clean — every reference passes every test;
  every wrong solution fails ≥ 1 test (deterministic WA or container TIMEOUT).
  Filter coverage reconciled against the on-disk id set (79/79, 0 missed).
- **Ground truths:** expected values verified independently in Python
  (brute force / closed form); full-scale generators asserted at import time
  inside the module sources. During the build the harness caught and I fixed
  several real defects, including a control-flow bug in a module-6 reference,
  six wrong expected values in module 7, a serialization desync in module 8's
  generator, and a capstone truth fix in module 12.
- **Brute partials executed:** subtask brute solutions run against their own
  test files — pass small, TIMEOUT full-scale as designed (s2 documented as
  the honest constants-beat-complexity exception).
- **Scoped content validation:** 150 nodes load clean in EN and in VI;
  EN/VI structures match; validator isolated from other agents' courses via a
  temp curriculum root (deep-copied course, track.json stripped to one course).
- **QA gates:** typecheck 0 · lint 0 errors (13 pre-existing warnings) ·
  unit/integration 184/184 · production build PASS.
- **Regression:** hsg-beginner (20/65/127), hsg-intermediate (18/58/110),
  hsg-advanced (20/83/92) load clean in EN and VI through scoped roots —
  unchanged.

## Cross-agent findings

1. **`hsg-mastery` (phase 31, other agent) coexists additively** — different
   directory, id prefix (`hsgm-`), and track.json row. No conflicts.
2. **One live defect in that agent's uncommitted file:**
   `hsg-mastery/modules/hsgm-process/module.vi.json` has `summary` 207 chars
   (schema max 200). Because the loader validates the whole track, this
   single VI overlay currently breaks VI loading of **every** hsg course
   through the real (non-scoped) path. Not mine to edit — reported here and
   in the course doc. Re-run any track-wide VI validation after they fix it.
3. Shared-file edits by me: only the additive `track.json` row.

## Known limitations

- No real-time contest timer, leaderboard, or submission-history entity in
  the platform schema: contests are practice sets in contest format; timed
  sprints are labeled self-timed in lesson text.
- Partial scoring is taught procedurally (named subtask tests); the grader
  itself is all-or-nothing per challenge.
- Sandbox has no network/interactor: distributed-flavored problems are
  deterministic simulations; interactive problems omitted.
- Difficulty gradation (Advanced → HSG-challenge) lives in titles/statements;
  the schema carries a single `difficulty` value.

## Multi-agent safety

No destructive git commands; no resets; no staging of others' work; nothing
committed (working tree left for the user). Edits strictly additive: new
course dir, new authoring scripts, new validator/harness/ledger, new docs,
new phase dir, one appended track.json row.
