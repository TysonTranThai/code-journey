# Course Spec — Python — Intermediate (`python-intermediate`)

**Track:** python · **Course:** 2 of 3 · **Prerequisite:** `python-beginner`
**Status:** authored 2026-09-13 · EN complete · VI complete (synchronized)
**Research basis:** docs/CURRICULUM-RESEARCH-PYTHON-INTERMEDIATE.md

## Identity

- **Who this is for:** learners who finished Python — Beginner and can already write functions, loops, collections, and simple try/except, and want to write larger, cleaner, tested, data-backed Python.
- **Outcome promise:** build and test multi-module Python applications that persist data in SQLite, consume JSON over HTTP, run concurrent async collectors, ship as installable packages — with typed APIs and professional error handling.

## Learning outcomes

1. Write and read Pythonic data pipelines (comprehensions, unpacking, sorting with keys, generators).
2. Design class-based and dataclass models using composition over inheritance, with basic protocols.
3. Build custom iterators, generators, and context managers on the Python data model.
4. Annotate public APIs with modern typing (containers, unions, Literal, Protocol) and structure a `src/` package.
5. Design exception hierarchies, chain causes, log professionally, and validate at boundaries.
6. Work with files, pathlib, csv/json round-trips, and streaming pipelines.
7. Test with unittest: fixtures, subTest parametrization, mock patching at boundaries; repair broken code test-first.
8. Store and query data in SQLite with parameterized queries, transactions, and schema constraints.
9. Consume JSON HTTP APIs with http.client and the transport-injection pattern; handle pagination, timeouts, and errors.
10. Write asyncio programs that gather concurrent work with `return_exceptions=True` and timeouts.
11. Package an application with pyproject.toml, console entry point, and lockfile discipline.
12. Apply secure-by-default habits: parameterized SQL, safe deserialization, no shell injection, env-based secrets.

## Curriculum

| # | Module | Lessons | Practice sets | Challenges | est. min |
|---|--------|---------|--------------|-----------|----------|
| 1 | pythonic-toolkit | comprehensions-and-unpacking, functions-as-values, sorting-with-key, checkpoint-pipelines | 3 | 10 | 205 |
| 2 | objects-and-modeling | classes-basics, properties-validation, dataclasses, composition-over-inheritance, checkpoint-modeling | 4 | 13 | 265 |
| 3 | data-model-iteration | iterators, generators, context-managers, checkpoint-streams | 3 | 9 | 200 |
| 4 | structure-and-typing | modules-packages, package-layout, typing-essentials, typing-protocols, checkpoint-typed-app | 4 | 12 | 240 |
| 5 | robust-errors | exception-design, exception-chaining-boundaries, logging, checkpoint-resilience | 3 | 10 | 215 |
| 6 | files-and-data | pathlib, csv-json, streaming-pipelines, checkpoint-data-pipeline | 3 | 10 | 225 |
| 7 | testing-discipline | unittest-first, subtest-parametrize, mocking-boundaries, checkpoint-repair | 4 | 12 | 255 |
| 8 | databases | sql-fundamentals, parameterized-queries, transactions-schema, repository-pattern, checkpoint-database-app | 4 | 13 | 285 |
| 9 | http-json | http-client, json-api-client, transport-injection, checkpoint-api-client | 4 | 12 | 255 |
| 10 | concurrent-async | sync-vs-async, coroutines-tasks, gather-timeouts, checkpoint-async-collector | 4 | 12 | 245 |
| 11 | packaging | pyproject-layout, console-entry-points, venv-lockfiles, security-audit, checkpoint-ship | 4 | 12 | 250 |
| **capstone** | capstone-cli-app | capstone-brief (+ 3 checkpoint challenges) | 1 | 3 | 120 |

**Totals:** 11 modules + capstone · **43 lessons** · **35 practice sets** · **~128 challenges** · **3 checkpoints inside capstone** · **≈ 2,760 min ≈ 46 h** (challenge minutes ≈ 58% — practice-heavy by design; Beginner measured ≈43%.)

## Progression shape

- Every module: lessons interleave with practice sets (`afterLesson`), difficulty climbs imitation → independent → combination; every module closes with a `mini-build` or `checkpoint` set.
- Debugging challenges ship broken starter code; learners must diagnose via traceback/tests.
- Security is woven into modules 8 (SQL injection), 6 (deserialization), 11 (shell injection, secrets) — plus an explicit audit set in module 11.
- AI-mentor guidance is included in lesson "Working with AI" blocks: asking for hypotheses, generating test cases, reviewing generated code — never accepting unreviewed architecture.

## Projects

Guided → independent arc across module checkpoints, culminating in the **Capstone: `TaskNoter`** — a typed, tested, SQLite-backed CLI task manager packaged with a console entry point, consuming a JSON export endpoint with the transport-injection pattern, with an async bulk-export command. The capstone has requirements, acceptance criteria, milestones, and 3 decision-verification checkpoint challenges — **no reference solution is published** (independent work by design).

## Prerequisite boundary (measured against Beginner on disk, not assumed)

| Concept | Beginner | Intermediate |
|---|---|---|
| syntax, variables, collections, loops, functions, f-strings | ✓ | review only in practice |
| try/except basics, reading tracebacks, methodical debugging | ✓ | advanced application (hierarchies, chaining, logging) |
| comprehensions, unpacking, `sorted(key=)` | — | ✓ module 1 |
| files, pathlib, csv/json basics (Beginner M9) | ✓ read/write basics | deepen: round-trips, streaming, path safety (module 6) |
| creating & importing modules (Beginner M10) | ✓ single modules | deepen: packages, `src/` layout, circular-import avoidance (module 4) |
| venv + pip + requirements (Beginner M11) | ✓ | deepen: pyproject.toml, console entry points, lockfiles (module 11) |
| assertions + basic automated tests (Beginner M12) | ✓ | deepen: unittest discipline, subTest, mock, test-first repair (module 7) |
| argparse-lite CLI (Beginner M14) | ✓ | advanced application (capstone) |
| OOP, dataclasses, protocols | — | ✓ modules 2–4 |
| typing | — | ✓ module 4 |
| context managers, generators | — | ✓ module 3 |
| sqlite3, transactions, repository pattern | — | ✓ module 8 |
| HTTP/JSON clients | — | ✓ module 9 |
| asyncio | — | ✓ module 10 |
| security habits | — | woven through 6/8/11 |

## Localization

Vietnamese (`python-intermediate` course + every module/lesson/practice/challenge overlay) authored simultaneously with EN. Technical terms follow the corpus rule: Python, SQLite, JSON, HTTP, asyncio, mock, boilerplate stay in English; surrounding prose is natural Vietnamese. Shared grading: VI overlays translate `title`/`prompt`/`hints` only — test `code` is shared, so EN and VI learners are graded by identical logic.

## QA gates

- Scoped validator (`validate-pi.ts`): schema-validates every node, EN/VI structural parity, minutes budget.
- Harness (`verify-challenges-pi.mjs` + `pi-solutions.mjs`): two-sided through the real sandbox worker — reference solutions pass every test; wrong solutions fail ≥1.
- Regression: Beginner, Web Dev courses, unit suite, typecheck, lint, E2E, production build.
