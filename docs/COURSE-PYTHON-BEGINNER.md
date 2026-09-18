# Course Specification — Python Beginner

Track: `python` · Course: `python-beginner` · Level: Beginner · Prerequisites: none
Companion research: `docs/CURRICULUM-RESEARCH-PYTHON-BEGINNER.md`

## Audience & positioning

First Python course for absolute beginners (no programming experience assumed; Web Development
Beginner graduates may take it, but nothing from it is required). Establishes strong programming
fundamentals through Python and prepares for Python Intermediate (not yet built), automation,
backend, scripting, data work, and general software engineering. NOT a data-science or AI course.

## Learning outcomes

By completion the learner can: run Python (interpreter, REPL, `.py` files); use
variables/primitives (int, float, str, bool, None); manipulate strings (indexing, slicing, methods,
f-strings); make decisions (if/elif/else, truthiness, boolean logic); use lists, tuples, sets,
dicts; write loops (for/while, break/continue, accumulators); write functions (params, returns,
defaults, keywords, scope basics, docstrings); read tracebacks and debug systematically; handle
errors (try/except/else/finally, raise); read/write files with `with`, use `pathlib`, CSV, JSON;
import and create modules; use core stdlib (`math`, `random`, `datetime`, `pathlib`, `json`,
`statistics`, `collections.Counter`); create/activate venvs and pip-install into them; write
assertions and basic automated tests; decompose problems (inputs → processing → outputs); build and
organize CLI applications; and use AI assistants critically (hints, review, testing — never blind
copying).

## Module map (15 modules)

| #   | Module id                        | Lessons (core focus)                                                                                                                              | Practice emphasis                                                                                     |
| --- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | `python-and-your-first-programs` | what-python-is · running-python · first-programs (print, comments) · syntax-errors-reading-them                                                   | output, tiny calculations, fix-the-syntax-error, prediction                                           |
| 2   | `variables-and-data-types`       | variables-assignment · numbers · booleans-none · conversions-type-inspection · operators-precedence                                               | calculator, unit converter, bill splitter, grade calculator mini builds                               |
| 3   | `working-with-strings`           | string-basics-indexing · slicing · string-methods · f-strings-formatting                                                                          | text transformation, username generator, mini parser, format drills                                   |
| 4   | `making-decisions`               | if-elif-else · truthiness · boolean-logic · validation-patterns                                                                                   | age/category checker, password validator, ticket + shipping calculators                               |
| 5   | `lists-and-collections`          | lists · tuples-sets · dictionaries · nested-collections · iterating-collections                                                                   | shopping list, contact book, inventory, leaderboard mini builds                                       |
| 6   | `loops`                          | for-loops · range-counting · while-loops · break-continue · nested-loops-patterns · accumulator-patterns                                          | counters, aggregation, search, pattern generation, menu loops                                         |
| 7   | `functions`                      | defining-functions · parameters-returns · default-keyword-arguments · scope-basics · docstrings-decomposition                                     | refactor repetitive scripts into functions; validation toolkit                                        |
| 8   | `errors-and-debugging`           | syntax-vs-runtime-vs-logic · tracebacks · try-except · else-finally-raise · debugging-methodically · **bug-hunt project (broken apps to repair)** | diagnose-and-fix broken programs                                                                      |
| 9   | `files-paths-and-data`           | reading-files · writing-files-with · paths-pathlib · csv-basics · json-persistence                                                                | notes app, expense tracker, JSON contact manager                                                      |
| 10  | `modules-and-standard-library`   | imports-modules · creating-modules-name · stdlib-tour (math/random/datetime) · stdlib-tour-2 (pathlib/json/statistics/Counter)                    | utility toolkit project                                                                               |
| 11  | `environments-and-packages`      | why-dependencies · venv · pip-requirements                                                                                                        | install a package into a venv; requirements workflow (verified conceptually — sandbox has no network) |
| 12  | `testing-and-code-quality`       | why-testing · assertions · basic-automated-tests · readable-code                                                                                  | make-the-tests-pass exercises; write-your-own tests                                                   |
| 13  | `problem-solving-fundamentals`   | decompose-inputs-outputs · pseudocode · searching-counting · aggregation-transformation · complexity-intuition · ai-as-assistant                  | progressively harder puzzles; AI-critique exercises                                                   |
| 14  | `command-line-applications`      | cli-input-menus · argparse-lite · organizing-cli-apps · persistence-errors                                                                        | task manager CLI project                                                                              |
| 15  | `capstone-personal-finance-cli`  | capstone-brief (requirements + acceptance criteria + milestones)                                                                                  | independent build, decision-based grading                                                             |

Checkpoints (coding-first, not quizzes): `checkpoint-fundamentals` (M2), `checkpoint-collections-control` (M6),
`checkpoint-functions-errors` (M8), `checkpoint-files-modules` (M10), `checkpoint-problem-solving` (M13),
`final-readiness` (M15 capstone-verification challenges). Checkpoint challenges attach as
lesson-attached challenges on checkpoint lessons (existing architecture).

## Practice plan (target 120–180, quality-gated)

Per-lesson micro practice sets (guided → independent climb, existing `level` ladder:
imitation → guided → debugging → independent → mini-build → real-world → combination), plus module
mini builds and the project ladder. Challenge types: guided, independent, debugging, prediction,
code-reading, fill-in, fix-the-code, edge-case, real-world. **Final counts are measured after
authoring and reported; if quality says 120, we ship 120 — no filler.**

## Execution support (minimal changes, additive)

- `language` field on challenges (`"javascript"` default; `"python"` for this course).
- Sandbox image gains pinned `python3`; worker script branches by language; verdict parsing unchanged.
- Python test contract: exec-solution + assertions in scope; `input()` disabled with clear error.
- Python 3.9-compatible content (harness floor; sandbox ships newer 3.x).

## Assessment philosophy

Two-sided verification for every challenge (reference passes, wrong fails); checkpoints are
implementation tasks; the capstone grades decisions (schema, module layout, persistence choice,
validation strategy) via decision-verification challenges — not a copy-paste tutorial.

## AI-learning philosophy

Platform mentor remains hint-laddered (never full solutions). Course content trains AI literacy:
asking for hints vs answers, reviewing AI code by running it, spotting hallucinated APIs, and
progressively reducing assistance.

## Localization

English + Vietnamese (`python-beginner` → _Python — Cơ bản_), same ids, natural Vietnamese using
the platform terminology table; EN/VI structural sync enforced by `validate-content.ts`.

## Estimated time (declared; reconciled at ship)

~57 lessons ≈ 14–15 h theory · ~130 challenges + 8 projects ≈ 20–24 h practice · total ≈ 35–39 h.
