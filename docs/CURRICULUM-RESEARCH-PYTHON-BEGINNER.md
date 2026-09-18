# Curriculum Research — Python Beginner

Date: 2026-09-12 · Course: **Python — Beginner** (first course of the future Python track)
Method: sources below were inspected before designing the curriculum. Inspection depth is labeled
honestly per source: **[READ]** = page fetched and read this session; **[SURVEY]** = reviewed via
search results/snippets only. No curriculum text was copied; findings informed original content.

## 1. Sources

| Source                                                             | Depth                             | What was taken from it                                                                                                                                                                                                                                                                 |
| ------------------------------------------------------------------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Python official Tutorial (docs.python.org/3/tutorial)              | [READ] — full TOC + intro         | Topic coverage map (interpreter → calculator-style intro → control flow → data structures → modules → I/O → errors → stdlib → venv/pip); its explicit note that it targets _programmers new to Python_, not new-to-programming learners — our course must be gentler than its ordering |
| CS50P — Harvard (cs50.harvard.edu/python)                          | [READ] — course page + weeks list | Week order proof: Functions/Variables → Conditionals → Loops → Exceptions → Libraries → Unit Tests → File I/O → … Functions taught in week 1; exceptions and unit tests treated as beginner-core, not advanced                                                                         |
| Exercism Python track                                              | [SURVEY]                          | Concept-led exercise model (17 concepts / 146 exercises); small-exercise density as the practice engine                                                                                                                                                                                |
| freeCodeCamp Scientific Computing with Python                      | [SURVEY]                          | Project-anchored certification structure; fundamentals before projects                                                                                                                                                                                                                 |
| roadmap.sh /python                                                 | [SURVEY]                          | Industry skill ordering; OOP positioned after fundamentals                                                                                                                                                                                                                             |
| pybit.es "learning mistakes" + r/learnpython threads               | [SURVEY]                          | Recurring failure modes: tutorial paralysis, improper sequencing, obsessing over "Pythonic" style too early, not reading error messages                                                                                                                                                |
| Code Journey internal: Course 1 + Course 2 practice-first revision | [READ] — repo                     | PracticeSet architecture (Learn/Practice separation), deliberate-practice levels, two-sided challenge harness                                                                                                                                                                          |

## 2. What a true Python beginner needs (synthesis)

1. **The execution model, early.** Interpreter vs REPL vs `.py` files; "code runs top to bottom";
   indentation _is_ structure. Official tutorial assumes this; beginners cannot.
2. **Error literacy before error handling.** Reading a traceback is a survival skill (community
   consensus: "READ THE ERROR MESSAGES"). Handling (`try/except`) comes after.
3. **Functions earlier than "objects".** CS50P teaches functions in week 1 and defers OOP to week 9.
   Decomposition is the beginner's superpower; classes are not.
4. **Collections as everyday tools.** Lists and dicts are the working structures; tuples/sets are
   introduced as "the right container for the job", not trivia.
5. **Files + JSON as a persistence milestone.** Programs that _remember things_ are the motivation
   jump-start for real projects (CS50P places File I/O in week 7; we agree).
6. **Environment hygiene at the end of fundamentals, not the start.** venv/pip only matter once a
   learner writes multi-file programs that want a third-party package. Teaching it on day 1 causes
   setup paralysis (tutorial-paralysis finding).
7. **Testing as a habit.** Assertions and a test-first exercise ("make the failing tests pass") are
   beginner-appropriate (CS50P week 6; Exercism's test-driven model).

## 3. Sequencing decisions (and what we intentionally delay)

**Order chosen:** programs → variables/types → strings → decisions → collections → loops →
functions → errors/debugging → files/data → modules/stdlib → venv/pip → testing → problem-solving
→ CLI apps → capstone.

- **Strings before decisions:** string manipulation is the most motivating early feedback loop
  (`print`, f-strings) and needs only variables. Official tutorial introduces text with numbers.
- **Loops after collections:** `for item in items:` reads naturally when lists already exist;
  `range()` is then taught as "counting", not as the primary loop form (differs from C-family order).
- **Functions after loops:** learners must first _feel_ the repetition that functions remove
  (refactoring exercises force this).
- **Errors module after functions:** syntax/runtime error reading is woven in from Module 1;
  _handling_ (`try/except`) is taught once learners write multi-branch programs that can fail.
- **venv/pip after stdlib:** dependency isolation is motivated by "I want a package", not boilerplate.

**Intentionally excluded (belongs to Intermediate/Advanced):**
classes/OOP, comprehensions beyond recognition (taught as "you will meet these" in Intermediate),
decorators, generators/iterators protocol, regex, match statements (3.10+ syntax; our floor is 3.9),
async/await, typing module, packaging/publishing, web frameworks, data-science stack, AI/ML.
This is a _programming with Python_ course, not a data-science or AI course.

**Standard library scope (Module 10):** `math`, `random`, `datetime`, `pathlib`, `json`,
`statistics`, `collections.Counter` — practical, beginner-facing usage only.

## 4. Practice philosophy

Course 1/2 lesson: too much theory killed completion. Python Beginner is authored practice-first:

- Loop: **Learn → tiny example → micro practice → guided → independent → debug → mini build → project**.
- Learn/Practice are separate content types (existing `PracticeSet` architecture) with `afterLesson`
  interleaving — the UI already separates them; content honors it.
- Target density: **120–180 challenges**, quality-gated: every challenge ships a reference solution
  (must pass all tests) and a wrong solution (must fail ≥1 test). Filler is rejected at authoring time.
- Challenge mix: guided, independent, debugging (fix broken programs), prediction (output reading),
  code-reading, fill-in/fix-the-code, edge-case handling, real-world tasks, mini builds.
- AI-assistance skills (Module: embedded in problem-solving + mentor philosophy): ask for hints not
  solutions, review AI code by testing it, spot hallucinated APIs. The platform mentor stays
  hint-laddered (never full solutions) — course content teaches _why_.

## 5. Projects (progressive independence)

1. Personal Introduction Program (Module 1, guided)
2. Calculator + unit converter / bill splitter (Module 2–4 mini builds)
3. Text Formatter (Module 3) · CLI Number Guessing Game (Module 6)
4. Bug Hunt — repair broken applications (Module 8)
5. JSON Contact Manager / Expense Tracker (Module 9)
6. Python Utility Toolkit (Module 10)
7. Personal Task Manager CLI (Module 14)
8. **Capstone: Personal Finance CLI** (requirements + acceptance criteria + milestones; no
   step-by-step solution; decision-based grading where architecture allows)

## 6. Platform execution support (minimal, additive)

The existing sandbox executes JavaScript only (`node` in the sandbox image, JS assertion tests).
Python support is added with the smallest possible surface, preserving all existing behavior:

- Sandbox image gains `python3` (pinned Alpine package); container hardening unchanged.
- `challengeSchema` gains `language: "javascript" | "python"` **defaulting to `"javascript"`** —
  zero changes to any existing web-dev challenge.
- Job payload carries the language; the worker's job script branches: `solution.py` + Python test
  files (`python3 test-x.py`) vs the existing `solution.js` + JS tests. Verdict parsing unchanged.
- Python test contract: each test file `exec`s the student solution, then runs author assertions
  with the solution's names in scope; `builtins.input` is replaced with a clear "not available in
  challenge runs" error (challenges are parameter/return/printed-output based; interactive scripts
  are run locally by the learner).
- Content floor: Python 3.9-compatible syntax (matches the QA harness's host interpreter); the
  sandbox image ships a newer 3.x, so 3.9-compatible content runs everywhere.

## 7. Localization

English + Vietnamese, structurally synchronized (same ids everywhere), Vietnamese written
naturally — not machine-translated — using the platform's established terminology table
(Biến/Hàm/Vòng lặp/Điều kiện/Danh sách/Từ điển/Ngoại lệ/Gỡ lỗi/Kiểm thử), keeping universally
recognized technical terms (Python, pip, venv, CLI, JSON) in Latin script where Vietnamese
developers keep them.

## 8. Estimated balance (declared, reconciled at ship time)

~57 lessons (theory-minutes) vs ~130 challenges + 8 projects (practice-minutes) — target
≥ 55% of learner time in the editor. Final measured numbers are reported in
`docs/COURSE-PYTHON-BEGINNER.md` and the phase summary after validation.
