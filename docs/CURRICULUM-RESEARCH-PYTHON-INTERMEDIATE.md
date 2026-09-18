# Curriculum Research — Python Intermediate (Course 2 of the Python track)

**Status:** living research doc for Python — Intermediate
**Created:** 2026-09-13 (authored from the sources and repository findings below)
**Predecessor:** docs/COURSE-PYTHON-BEGINNER.md (Course 1, in progress by another agent at authoring time)
**Rule applied throughout:** sources inform scope and pedagogy; every explanation and challenge is original Code Journey content.

---

## 1. Repository findings that shaped the design (measured, not assumed)

Before designing anything, the actual repo and runtime were inspected. These findings constrain the curriculum more than any external source:

### 1.1 What Python Beginner actually teaches (its real boundary)

The Beginner course on disk (8 modules when last measured, still being finalized by its authoring agent) covers: first programs, running Python, variables/numbers/booleans/None, operators and precedence, strings (indexing, slicing, methods, f-strings), conditionals and validation patterns, lists/dicts/tuples/sets, loops and accumulators, functions (def, return, defaults, scope, decomposition), tracebacks and basic try/except, and practice sets including mini-builds.

Its 15-module plan additionally covers files/pathlib/CSV/JSON (M9), creating and importing modules (M10), venv + pip + requirements (M11), assertions and basic automated tests (M12), argparse-lite CLI work (M14), and a broken-code bug-hunt project (M8). It does **not** cover: comprehensions, unpacking, packages/src-layout, OOP, dataclasses, typing, context managers, generators, sqlite3, HTTP, asyncio, pyproject packaging, performance, or security. Design consequences:

- **Intermediate deepens Beginner's basics** (files → round-trips/streaming/path-safety; modules → packages; assertions → unittest discipline; venv → pyproject/entry points) instead of reteaching them.
- **Intermediate teaches fresh**: OOP/dataclasses, the data model, typing, sqlite3, HTTP/JSON, asyncio, security.
- **Robust errors builds custom exceptions and chaining** on Beginner's try/except, not from zero.

### 1.2 The sandbox defines what challenges can grade

Python challenges execute in `codejourney-sandbox:latest` (Alpine, python **3.12.14**), probed directly for this research:

| Capability | Available? | Design consequence |
|---|---|---|
| stdlib: sqlite3, asyncio, json, pathlib, csv, re, datetime, collections, itertools, functools, unittest (+ mock), tomllib, http.client | ✅ | Fully gradable modules |
| `requests` | ❌ | API client module is **stdlib-first** (http.client for a raw lesson, then transport-injection pattern where requests is shown as the industry tool) |
| `pytest` | ❌ | Testing module is **unittest-first** (subTest, mock, setUp/tearDown); pytest shown as the ecosystem standard with an honest "how it maps" |

This is a pedagogically sound constraint: unittest is in the standard library and transferable, and dependency-injection for I/O is the professional pattern regardless of the HTTP library. The research doc for each module records what is deferred to "on your own machine" (pytest plugins, requests/sessions, httpx).

### 1.3 Platform mechanics discovered

- Challenges carry `language: "python"` and grade through the real sandbox worker (`src/workers/sandbox.ts` + `python-runtime.ts` harness). Two-sided QA (reference passes / wrong fails) runs through the same path (pattern: `verify-challenges-py.mjs` + `py-solutions.mjs`).
- Challenge tests are `(name, code, hint)` triples; `boilerplate` is starter code; practice levels are `imitation → guided → independent → combination → real-world / debugging / mini-build`.
- Course ids in this track: Beginner's `course.json` already declares `nextCourse: "python-intermediate"` — the id is fixed by that reference.
- `validate-content.ts` sweeps every course directory on disk; a half-written course breaks global loads. Beginner's agent was observed writing files minutes before authoring began, so the Intermediate course directory was authored **in one scripted wave** to minimize any window where global validation could see a partial tree.

---

## 2. Sources

Authoritative, consulted for scope and correctness (no content copied):

- **Python 3 docs (docs.python.org/3)**: Tutorial ch. 9 (classes), `sqlite3` DB-API guide (placeholder discipline), `pathlib`, `contextlib`, `typing` (generics, Protocol), `unittest` (+ mock), `asyncio` (coroutines, tasks, gather), `logging` (basic config, logger hierarchy), `functools` (cached_property? — no: cached_property lives on functools; lru_cache), `dataclasses`, `csv`/`json` (round-tripping), `pyproject.toml` (Packaging User Guide: setuptools layout, entry points).
- **PEP 8** — naming, module layout conventions used in the architecture module.
- **PEP 484 / 604** — typing syntax (`X | None`), when annotations are evaluated, typing for containers.
- **OWASP SQL Injection Prevention Cheat Sheet** — parameterized-query pedagogy for the database module.
- **sqlite.org** — pragma forensics (`pragma table_info`), transaction semantics used in challenges.
- **Fluent Python (Ramalho), 2nd ed.** — pedagogical framing for the data model, protocols, and "composition over inheritance" sequencing (concepts only; no text reused).
- **Real Python / roadmap.sh** — consulted for common intermediate-skill inventories and ordering comparisons; confirmed the industry expectation that intermediates own: OOP, typing, files/serialization, testing discipline, and packaging basics.

## 3. Skill-gap analysis: what separates Beginner from Intermediate

Measured against the Beginner course on disk and the sources above, an intermediate Python developer is expected to:

1. **Model data with classes and dataclasses**, choosing composition over inheritance, and implement basic protocols (`__repr__`, `__eq__`, iteration).
2. **Write Pythonic data pipelines**: comprehensions, unpacking, `sorted(key=)`, generator-based streaming for large inputs.
3. **Manage resources safely**: `with` on files and connections, custom context managers via class-based and `@contextmanager` forms.
4. **Structure code**: modules, packages, `__init__.py`, relative vs absolute imports, avoiding circular imports.
5. **Handle failure deliberately**: exception hierarchies, `raise ... from`, validation at boundaries, `logging` instead of prints.
6. **Test as engineering**: unittest with fixtures, parametrization (`subTest`), mocking at boundaries, test-first repair of broken code.
7. **Persist data**: sqlite3 with parameterized queries (never string-built SQL), transactions, schema constraints.
8. **Consume and build HTTP/JSON services**: http.client fundamentals; the transport-injection pattern that keeps business logic testable.
9. **Reason about async**: event loop, coroutines, `asyncio.gather` concurrency with `return_exceptions=True`, timeouts.
10. **Package and ship**: pyproject.toml, console entry points, virtualenv workflow, reproducibility via lockfiles.
11. **Type-annotate** public APIs (containers, Optional/`|`, Literal, Protocol) and check with mypy on their own machines.
12. **Apply secure habits**: parameterized SQL, safe deserialization (`json` not `pickle` for untrusted data), `shlex.join`/no shell=True, secrets from environment.

## 4. Scope decisions

**Included (11 modules + capstone):** see docs/COURSE-PYTHON-INTERMEDIATE.md for the final module list and minute budget.

**Excluded from Intermediate (reserved for Python Advanced):** descriptors, metaclasses, ABCs beyond one Protocol lesson, `__init_subclass__`, concurrency beyond asyncio (threads/multiprocessing internals, GIL theory), C extensions, Cython, plugin/entry-point discovery systems, web frameworks (FastAPI/Django), ORMs/alembic, async generators, asyncio internals (loop policies, uvloop), packaging internals (wheel building internals, publishing automation), distributed systems, advanced mypy configuration (plugins, strict mode).

**Deferred to "on your own machine" boxes** (sandbox lacks the dependency): pytest fixtures/parametrize as the ecosystem standard, requests/httpx, mypy runs. Each gets an honest note plus a stdlib transferable equivalent that IS graded (unittest.mock, http.client, annotation-writing skills verified by structure/behavior tests rather than a checker run).

## 5. Pedagogy and practice architecture

The deliberate-practice ladder (platform levels) is used per module:

`imitation` (mirror a worked pattern) → `guided` (fill the hard part) → `independent` (spec only) → `combination` (two+ concepts together) → `real-world` / `debugging` / `mini-build` (authentic task shapes; debugging challenges ship genuinely broken starter code).

Ratio target set before authoring: ≥55% of learner minutes in hands-on challenge work (Beginner measured ≈43% practice; Web Intermediate measured ≈45%). Every module ends at a mini-build; the course ends in an independent capstone (no reference solution published).

## 6. Sequencing rationale (dependencies before dependents)

functions/protocols → OOP (needs functions) → data model/iteration (needs classes) → typing (needs OOP + protocols) → errors/logging (needs OOP for custom exceptions) → files/serialization (needs errors) → testing (needs everything above to test) → databases (needs files/typing/errors) → HTTP/JSON (needs errors + testing's mock) → asyncio (needs HTTP mental model) → packaging/capstone (needs all). Security is not an isolated module: parameterized SQL, safe deserialization, subprocess discipline, and secret handling are **woven into the modules where the hazard lives** (matches how adults retain security practice and how OWASP frames prevention-by-default), with a dedicated audit challenge set at the end.
