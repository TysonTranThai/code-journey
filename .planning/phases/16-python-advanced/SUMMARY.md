# Phase 16 — Course: Python — Advanced — SUMMARY

Date: 2026-09-13
Status: **COMPLETE**

## Course

Track `python`, course `python-advanced` — 15 modules, 63 lessons (including 15
checkpoints), 49 practice sets, **89 challenges** (74 practice-set + 15
checkpoint), full EN + VI parity (126 lesson MDX bodies compile clean, VI
overlays on every challenge and module). Course metadata:
`prerequisites: ["python-intermediate"]`, 14 outcomes, learner-facing audience
copy. Track path: python-beginner → python-intermediate → python-advanced.

## Modules

1. data-model-protocols — attribute lookup, descriptors, MRO, slots, protocols
2. metaprogramming — decorators, `__init_subclass__`, metaclasses, plugin registries
3. advanced-typing — generics, ParamSpec, Protocols, overloads, TypedDict
4. concurrency-parallelism — GIL, threads, locks, executors, benchmarked choices
5. structured-async — TaskGroup, timeouts, cancellation, bounded queues
6. performance-engineering — profile → optimize → verify (deterministic graded tests)
7. cpython-internals — bytecode, frames, refcounting/GC, import system
8. architecture-patterns — ports & adapters, DI, repositories, refactoring
9. production-apis — status-code contracts, pagination, idempotency, validation, readiness
10. distributed-systems — retries/backoff, idempotent consumers, circuit breakers, DLQs
11. databases-data-access — query plans, indexes, N+1, isolation, optimistic locking
12. security-engineering — threat modeling, injection, SSRF, path traversal, secrets
13. advanced-testing — fakes, property-based testing, flaky-test triage, test runner
14. production-tooling — packaging/semver, atomic writes, graceful shutdown, structured logs
15. capstone-production-platform — job platform from a requirements brief, acceptance-tested

## Graded-code constraint

Host harness runs `python3.11`; sandbox image runs Python 3.12.14. All graded
code is Python 3.11-compatible; 3.12/3.13 features (PEP 695, TypeIs,
free-threading) appear as lesson prose with version notes only.

## Level migration (discovered during wiring)

`challengeSchema.level` accepts only
imitation|guided|independent|combination|real-world|debugging|mini-build. The
authoring pipeline had emitted a legacy vocabulary (build/apply/predict/debug/
refactor). All 74 practice challenges were remapped deliberately (drills →
guided/independent, multi-concept → combination, find-and-fix → debugging,
project-sized → real-world, mini components → mini-build); authoring sources
were patched in lockstep so a re-emit cannot regress. Final distribution:
18 guided / 15 independent / 20 combination / 9 debugging / 10 real-world /
2 mini-build.

## Loader-schema fixes during wiring

- `production-apis` had no module manifest (m9 script skipped `write_module`) — created, EN+VI
- 5 module summaries + course description exceeded the 200-char loader cap — trimmed in place, sources synced where emitted by scripts
- Checkpoint sidecars carried an invalid `level:"build"` — checkpoint (lesson-attached) challenges may omit `level` per schema comment; removed
- Checkpoint lesson ids collided with their own challenge ids (single global id namespace); then generic ids collided with other agents' courses — all 15 lessons renamed `pa-checkpoint-X` → `advanced-checkpoint-X`; plus `capstone-brief` → `advanced-capstone-brief`, `observability` → `advanced-observability`, `threat-modeling` → `advanced-threat-modeling` (cross-course collisions with python-intermediate and web-development-intermediate); all `afterLesson` refs updated
- Wiring done by `scripts/content-authoring/pypa_wire.py` (idempotent): 15 modules into course.json, course appended to track.json

## QA — actual results

| Gate | Result |
|---|---|
| Two-sided challenge harness (`_harness_pa.py`, python3.11) | **89/89** (reference PASS + wrong-solution FAIL) |
| validate-content.ts (6 courses) | exit 0; python-advanced: 15 modules, 63 lessons, EN/VI synced, 266 nodes/locale |
| MDX compile (python-advanced, EN+VI) | **126/126** (`check-mdx-pa.mts`) |
| Typecheck | clean |
| Lint | **0 errors, 0 warnings** (removed dead imports from my `verify-challenges-py.mjs`) |
| Unit + integration tests | **160/160** (27 files) |
| Production build | PASS (full route table emitted) |
| E2E (Playwright) | **36/36** vs live :3000 server; first attempt without the temp config failed because Next 16 refuses a second dev server in the same dir — used the temp-config workaround from Phase 13, then deleted it |

## Practice distribution (why)

- 18 guided / 15 independent: mechanism drills right after deep dives
- 20 combination: multi-concept synthesis (protocol + slots, TaskGroup + timeouts + backpressure)
- 9 debugging: find-and-fix (diamond MRO bug, N+1, flaky tests, SSRF, path traversal)
- 10 real-world: module projects + capstone milestones, minimal scaffolding
- 2 mini-build: reusable components (custom deque, API router)
- 15 checkpoints: lesson-attached, acceptance-test graded
- Estimated learner time: 1595 min lessons / 1169 min practice+projects ≈ **42% hands-on** (advanced courses legitimately carry more reading; every module still follows learn → deep dive → practice → debug → build)

## Files created/modified

- `src/content/tracks/python/courses/python-advanced/**` — full course (EN+VI)
- `src/content/tracks/python/track.json` — course registered
- `scripts/content-authoring/validate-content.ts` — python-advanced added to COURSE_TRACKS (one line, established pattern)
- `scripts/content-authoring/pypa.py`, `pypa_course.py`, `pypa_m1..15.py`, `pypa_wire.py`, `_harness_pa.py`, `check-mdx-pa.mts`, `_fix_m7.py`, `_fix_m9.py`, `_fix_m10.py`
- `scripts/content-authoring/py-solutions.mjs` — pa-* ledger entries
- `docs/COURSE-PYTHON-ADVANCED.md`, `docs/CURRICULUM-RESEARCH-PYTHON-ADVANCED.md`
- `scripts/content-authoring/verify-challenges-py.mjs` — my file: dead imports removed

## Multi-agent safety

- No destructive git commands; no resets/checkouts/cleans; nothing committed
- Python Intermediate agent's files untouched (their `capstone-brief` lesson id was the collision; I renamed **my** copy)
- cpp agent's scaffold was mid-flight during validation windows — waited and re-ran rather than editing
- Shared-file touches limited to the established one-line validator pattern and my own harness files

## Remaining issues

- None known for this course. Pre-existing repo-level leftovers unchanged: prettier drift (~235 files), ~500 uncommitted files (user decision)
