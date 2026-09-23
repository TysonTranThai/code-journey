# HSG Intensive — Course Documentation

**Track:** `hsg` · **Course:** `hsg-intensive` · **Prerequisite:** `hsg-advanced`
**Status:** Complete (2026-09-22) · **Locales:** English + Vietnamese (full parity)

## Purpose

HSG Intensive is the fourth stage of the HSG THPT track. It is deliberately **not**
another algorithm course. Students finishing HSG Advanced already know the tools;
this course trains the *use* of those tools under contest conditions:

> "I don't know what algorithm this is." → analyze constraints → try brute force →
> discover the observation → derive the algorithm → implement → get WA → debug →
> optimize → pass.

Approximately 20% of the content is review (compressed, execution-focused); the
remaining 80% is problem solving: recognition drills, constraint analysis,
wrong-solution clinics, stress testing, subtask strategy, timed sets, mock
contests, editorial training, and a final challenge pack.

## Course structure

| # | Module | Focus | Lessons | Challenges |
|---|--------|-------|---------|-----------|
| 1 | hsgx-recognition | Problem recognition: constraints → tool, hidden-topic drills | 3 (incl. checkpoint) | 9 |
| 2 | hsgx-budget | The arithmetic of budgets: 10⁸/10⁹/10¹⁰, memory lines, small-n law | 3 (incl. checkpoint) | 7 |
| 3 | hsgx-observation | Find the key observation: brute → bottleneck → invariant → proof | 3 (incl. checkpoint) | 6 |
| 4 | hsgx-combinations | Fusing two tools: BS+greedy, compression+Fenwick, DSU-in-time, Dijkstra-on-states, SCC+DAG DP | 3 (incl. checkpoint) | 6 |
| 5 | hsgx-wrong | Wrong-solution clinic: WA/TLE/overflow/greedy/DP/DSU bugs, counterexamples | 3 (incl. checkpoint) | 11 |
| 6 | hsgx-stress | Differential stress testing: candidate + oracle + generator, seeds, 4000-trial harnesses | 3 (incl. checkpoint) | 4 |
| 7 | hsgx-subtask | Subtask mastery: partial scoring, brute-force partials, verified full-scale TLEs | 3 (incl. checkpoint) | 4 |
| 8 | hsgx-speed | Speed training: four self-timed sprints + recognition/implementation/debug/hard layout | 3 (incl. checkpoint) | 5 |
| 9 | hsgx-mixed | Mixed sets A–E, topics hidden; learner names the tool first | 2 (incl. checkpoint) | 10 |
| 10 | hsgx-contests | Two original 3-problem mock contests + final-simulation checkpoint | 2 (incl. checkpoint) | 7 |
| 11 | hsgx-editorials | Editorial protocol + re-solve/variation training | 2 (incl. checkpoint) | 3 |
| 12 | hsgx-final | Final challenge pack (6 problems) + capstone + reference pack (selection guides) | 2 (incl. checkpoint) | 7 |

**Totals:** 12 modules · 32 lessons (12 checkpoints) · 79 challenges ·
levels: 39 combination / 23 independent / 15 debugging / 2 real-world.

## Challenge model

Every practice and checkpoint challenge ships as a **two-sided pair**:

- a verified **reference solution** (`R`) that must pass every test, and
- a deliberately **wrong solution** (`W`) — the natural first idea (greedy trap,
  off-by-one, double-count, overflow, quadratic re-scan) — that must fail at
  least one test.

Both sides execute in the real hardened sandbox (`codejourney-sandbox`, g++ 14.2.0,
C++20, 20 s job budget, no network). Editorials inside lesson MDX walk the
observation → proof → complexity → common-wrong-approaches chain before any code.

## Reference solutions

Executable references live in
`scripts/content-authoring/hsg-intensive-solutions.mjs` (`R[W]` ledgers keyed by
challenge id). The verification harness
(`scripts/content-authoring/verify-challenges-hsgx.mjs`) compiles both sides into
the same test TU the production worker uses and reports per-challenge verdicts.

## Verification (2026-09-22)

- **Two-sided harness:** 79/79 clean — every reference passes every test;
  every wrong solution fails ≥ 1 test (WA or container TIMEOUT).
- **Ground truths:** all sample and full-scale expected values verified
  independently in Python (brute force or closed form), including the
  full-scale generators inside each module source (import-time asserts).
- **Brute-forced subtask partials:** executed against their own test files —
  small tests pass, full-scale tests TIMEOUT as designed (one documented
  exception: the s2 brute is fast because SIMD constants beat the O(n·k)
  complexity folklore; the lesson text states what was measured).
- **Scoped content validation:** `validate-content-hsgx.ts` loads the whole
  course through the public loaders in **both locales** — 150 nodes clean per
  locale; EN/VI structures match; isolated from other agents' in-flight courses
  via a temp curriculum root.
- **Typecheck:** 0 errors. **Lint:** 0 errors. **Unit/integration:** 184/184.
  **Production build:** PASS.

## Regression

`hsg-beginner`, `hsg-intermediate`, `hsg-advanced` verified unchanged: each
loads clean in EN and VI through a scoped root with identical counts to their
completion summaries. (Track-wide VI loading is currently blocked by one
schema violation in the *other* course `hsg-mastery`'s uncommitted
`hsgm-process/module.vi.json` — summary > 200 chars — reported, not touched.)

## Known limitations (honest)

- **No real-time contest timer / leaderboard / submission history:** the
  platform schema has no contest entity. Mock contests are modeled as
  practice sets with contest-format statements, contest-order difficulty and
  per-test scoring semantics; timed sprints are **labeled self-timed** in the
  lesson text rather than pretending a timer exists.
- **Partial scoring is procedural, not automatic:** subtask tests exist as
  named tests, but the grader awards all-or-nothing per challenge, so the
  lessons teach the *strategy* of banking subtasks.
- **No distributed/interactive problems:** the sandbox has no network and no
  interactor; "distributed-flavored" problems are deterministic simulations.
- Difficulty metadata uses the platform's single `difficulty: "advanced"` value;
  the A–E "HSG-challenge" gradation lives in titles/statements, not schema.

## Multi-agent note

This course was authored alongside other agents' work (`hsg-mastery`, C/C++,
Java, C#, Python tracks). All edits were additive: new course directory, new
authoring scripts, one appended row in `hsg/track.json` (after the other
agent's `hsg-mastery` entry, which was preserved verbatim), one new scoped
validator, one new course doc, one new phase directory. No existing course
content was modified.
