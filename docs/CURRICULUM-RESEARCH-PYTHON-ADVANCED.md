# Curriculum Research — Python — Advanced

Date: 2026-09-13 · Status: design input for `docs/COURSE-PYTHON-ADVANCED.md`
Rule honored: no curriculum text is copied from any source; sources inform an
original Code Journey progression. Only sources actually consulted during this
phase are listed.

## 1. Sources consulted

### Runtime / language specifications (primary truth for graded content)

- **Python documentation — Coroutines and Tasks** (docs.python.org/3/library/asyncio-task.html):
  confirms `asyncio.TaskGroup` and `asyncio.timeout()` as the structured-concurrency
  primitives (3.11+), built on cancellation. This anchors Module 5.
- **PEP 695 — Type Parameter Syntax** (peps.python.org/pep-0695): `class Box[T]`,
  `def first[T]`, inline `type` aliases (3.12+). Anchors the Advanced Typing module —
  taught as prose + version note, not graded, because the QA harness host runs 3.11.
- **PEP 742 — `typing.TypeIs`** (3.13) and **PEP 703 — free-threaded CPython**
  (3.13 optional build): covered as "where the language is heading" prose.
- **CPython Data Model, `__init_subclass__`, descriptors, MRO (C3 linearization),
  `contextlib`, `concurrent.futures`, `multiprocessing`** — standard-library
  documentation set consulted for accurate semantics of Module 1/2/4 topics.
- **Python packaging user guide — Writing your pyproject.toml**
  (packaging.python.org/guides/writing-pyproject-toml): Module 13 (packaging) follows
  the current standard (pyproject-only, no setup.py).
- **pytest — Writing plugins** (docs.pytest.org): entry-point-based plugin
  registration informs both the metaprogramming registry project and packaging.

### Engineering-practice sources (positioning and expectations)

- **Real Python — Advanced tutorials index** (realpython.com/tutorials/advanced):
  confirms the professional topic set this course targets: concurrency,
  metaprogramming, performance optimization, CPython internals.
- **Quansight Labs — Scaling asyncio on Free-Threaded Python** (labs.quansight.org,
  Sep 2025) and **Optiver — Choosing between free threading and async in Python**
  (Dec 2025): current industry view that the GIL story is becoming a real
  engineering decision; course teaches the decision framework, not folklore.
- **Community "advanced Python" discourse (Reddit r/learnpython threads,
  2024–2025 listicle articles)**: used only as a signal of what learners expect;
  deliberately *not* followed where it equates "advanced" with syntax trivia.

### Repo-internal evidence (used as design input, not external sources)

- **Python — Beginner (shipped, Phase 13)**: 15 modules ending at CLI apps,
  testing basics, and the Personal Finance CLI capstone. Establishes the floor.
- **Python — Intermediate (in progress, other agent)**: visible module set is
  `pythonic-toolkit, objects-and-modeling, data-model-iteration,
  structure-and-typing, robust-errors, files-and-data, testing-discipline,
  databases, http-json, concurrent-async, packaging, capstone-cli-app` — i.e.
  Intermediate already covers: iteration/data-model *introduction*, typing
  structure, pytest discipline, SQL/databases, HTTP clients, asyncio basics,
  packaging basics. **Advanced therefore must not re-teach these**; it deepens
  and engineers them (see §3).

## 2. What actually distinguishes an advanced Python developer

Synthesis of the sources above and professional practice:

1. **They reason about the object model instead of memorizing it** — attribute
   lookup, descriptors, MRO, protocols are tools they can implement, not trivia.
2. **They choose concurrency models deliberately** — threads vs processes vs
   asyncio vs (soon) free-threading, based on I/O- vs CPU-boundness, and can
   benchmark the choice.
3. **They measure before optimizing** — profile, attribute, verify; performance
   work is evidence-driven.
4. **They design boundaries** — dependency inversion, ports/adapters, plugin
   registries; architecture serves a stated problem.
5. **They engineer for failure** — retries with backoff, idempotency, timeouts,
   graceful shutdown, observability.
6. **They can make code type-safe as a design activity**, and treat tests
   (property-based, contract, concurrency tests) as design tools.
7. **They can audit security** of real code (injection, unsafe deserialization,
   SSRF, secrets handling) and repair it safely.

## 3. Sequencing decisions (and what is intentionally excluded)

Dependency matrix against the actual existing courses (✓ = taught there):

| Topic | Beginner | Intermediate | Advanced |
|---|---|---|---|
| Syntax, collections, functions, files, testing basics | ✓ | — | — |
| OOP modeling, iteration protocol intro | — | ✓ | deepens |
| Typing structure, annotations | — | ✓ | deepens |
| pytest discipline | — | ✓ | deepens |
| Databases/SQL, HTTP clients, async basics, packaging basics | — | ✓ | deepens |
| Descriptors, `__getattribute__` family, MRO mastery, custom protocols | — | — | **✓** |
| Metaclasses / registries / plugin patterns | — | — | **✓** |
| Generics depth (variance, ParamSpec, overloads), static-analysis architecture | — | — | **✓** |
| Concurrency as engineering (pools, races, GIL, benchmarking) | — | — | **✓** |
| Structured async (TaskGroup, timeouts, async CMs/iterators, backpressure) | — | — | **✓** |
| Profiling-driven performance (cProfile, timeit, memory) | — | — | **✓** |
| CPython internals for practitioners (bytecode, GC, import system) | — | — | **✓** |
| Ports/adapters, DI, modular architecture, refactoring strategy | — | — | **✓** |
| Production API engineering (validation, rate limits, idempotency, pooling) | — | — | **✓** |
| Distributed fundamentals (queues, retries/backoff, circuit breakers) | — | — | **✓** |
| Security engineering (threat modeling, injection, deserialization, SSRF) | — | — | **✓** |
| Observability (structured logs, metrics, correlation IDs, SLOs) | — | — | **✓** |

**Intentionally excluded** (wrong level or wrong course): CPython C-API extension
authoring, building alternative interpreters, Kubernetes/infra operations,
offensive security, framework-specific deep dives (FastAPI/Django/Celery are
referenced conceptually; the course stays stdlib-first), PySpark/data-science.

## 4. Practice philosophy

Same loop as Beginner/Intermediate, deepened: Learn → Deep Dive → Practice →
Debug → Benchmark/Test → Build → Project. Target investigated range 150–220
challenges; every challenge is engineering-flavored (diagnose, repair, prove,
benchmark) rather than syntax recall. Every graded challenge is two-sided
verified (reference passes, plausible wrong solution fails) on the same harness
contract as Beginner (host `python3.11` ≙ sandbox `python3.12`).

## 5. Runtime constraint discovered (affects authoring)

- QA harness host default `python3` is **3.9.6**, but `python3.11` (3.11.15) is
  available; sandbox image pins **python 3.12.14** (`docker/Dockerfile.sandbox`).
- Decision: **graded code targets Python 3.11** (runs on both); 3.12/3.13
  features (PEP 695, TypeIs, free-threading) appear in lessons as prose with
  version notes. `typing` features used in graded code are 3.11-safe
  (`ParamSpec`, `Self` via 3.11, `Literal`, `Protocol`, `TypedDict`,
  `overloads`).

## 6. Project progression (scaffolding decreases to zero)

1. Custom collection that obeys Python protocols (guided)
2. Plugin registration framework (guided → independent)
3. Concurrent job processing system (independent, benchmark required)
4. Performance rescue (measure → profile → optimize → prove)
5. Architecture refactor of a tangled application (independent)
6. Production-style API (independent)
7. Distributed job system with retries/idempotency (independent)
8. Security hardening lab (audit + repair)
9. Instrumented service (observability)
10. Legacy system rescue (minimal scaffolding)
11. **Capstone: production-grade job-processing platform** (requirements +
    acceptance criteria only; learner makes the architecture decisions)
