# Phase 14 — Python Intermediate — SUMMARY

Date: 2026-09-13
Status: **CONTENT COMPLETE — all gates green**
Authoring agent: independent session; ran alongside the Python Beginner agent (Phase 13) under multi-agent safety rules.

## What was built

**Course `python-intermediate`** (track: python) — "larger, cleaner, testable Python", built on top of the *actual* Python Beginner curriculum (not the prompt's hypothetical boundary: Beginner already teaches files/pathlib/CSV/JSON, modules, venv/pip, assertions, argparse-lite — Intermediate deepens rather than reteaches).

| Metric | Actual |
|---|---|
| Modules | 12 (incl. capstone) |
| Lessons | 49 (11 of them checkpoint lessons) |
| Practice sets | 36 |
| Challenges | 93 — two-sided verified **93/93** |
| Checkpoints | 11 per-module checkpoints + capstone with decision-verification |
| Time | 1837 min ≈ 31 h — **59% practice / 41% theory** |
| Locales | EN complete, VI complete (227 nodes load clean per locale; EN/VI structures match) |

Module arc: pythonic-toolkit → objects-and-modeling → data-model-iteration → structure-and-typing → robust-errors → files-and-data → testing-discipline → databases → http-json → concurrent-async → packaging (+security-audit) → capstone-cli-app.

## Sandbox-driven design decisions

The sandbox image (probed directly) ships stdlib only: sqlite3, asyncio, http.client, tomllib, unittest.mock — **no pytest, no requests**. Therefore:
- Testing module teaches unittest + subTest + unittest.mock (pytest framed as a local-machine extension).
- HTTP module teaches transport injection (opener/transport callables) — no network needed to grade.
- Async grading uses real concurrency timing (sequential-await wrong solution fails the elapsed-time probe).

## QA — challenge verification (93/93, two-sided)

First harness run exposed **24 failures**, all root-caused and repaired (scripts `_pi_fix_bugs.py`, `_pi_fix_round2.py`, `_pi_restore_vi.py`):

1. **`inspect.getsource` can never work on the platform** — solutions are graded via `exec(SOLUTION_SOURCE)`; 8 tests rewritten to use the harness `code` variable (raw source, present in both dev harness and `python-runtime.ts`).
2. **Boilerplate is part of the graded unit** — the editor seeds it (`useDraft`) and the learner's full editor content is submitted; harness now prepends it, mirroring production (fixed `pi5-exc-order` without touching tests).
3. **sqlite tests** needed `row_factory = sqlite3.Row` (3 challenges) and the transfer test needed `conn.commit()` after seeding (correct `rollback()` had wiped the uncommitted seed).
4. **7 wrong solutions were accidentally correct** (classic traps cut both ways: class-attr vs instance, stable-sort no-op, sequential-await matching output, missing row_factory masking injection). Tests strengthened with discriminating probes; W solutions replaced where genuinely wrong patterns were available (e.g. mock-clock W now tests only one band).
5. **VI hint regression** introduced and fixed by my own sync script (6 hints restored from the authoring source).

Honest note: production can never support `inspect`-style source tests for Python; the platform contract is `code` (raw source) + executed names — future Python challenge authors should use `code`.

## Gates (final)

| Gate | Result |
|---|---|
| Scoped validator (`validate-pi.ts`) | PASS — schema-valid EN + VI, parity |
| Full validator (`validate-content.ts`) | PASS — all tracks, both locales; linear paths: web 143, python 106 |
| PI harness (two-sided) | **93/93** |
| Unit + integration | **160/160** (one flaky Postgres queue test passed on rerun) |
| MDX compile | fixed 2 unescaped-brace lines in capstone brief (EN+VI) — real production-page bug |
| Typecheck / lint | clean / 0 errors (3 warnings in the other agent's WIP `verify-challenges-py.mjs`, untouched) |
| E2E | **36/36** |
| Production build | **986 static pages** (was 694) |

## Multi-agent safety record

- Python Beginner agent's work fully preserved; `python-beginner/` never touched. Their Phase 13 landed mid-flight (15 modules, manifests) — full validator passes with **both** courses coexisting.
- Track registration was additive (two lines in `track.json`, format preserved).
- Shared-file edits: none beyond the additive track registration; my earlier Phase 12 manifest completion for their course was superseded by their own final structure (left intact, no revert).
- Zero destructive git commands; nothing committed.

## Prerequisites wired

`python-intermediate.course.json` declares `prerequisites: ["python-beginner"]` (schema `z.array(slugSchema)`; the course page renders a prerequisite callout when set).

## Remaining work

- None for this phase's scope. Python Advanced is intentionally out of scope.
- The other agent's `verify-challenges-py.mjs` still has a syntax error (their file; not mine to fix).
