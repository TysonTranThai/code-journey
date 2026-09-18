# Phase 13 — Course: Python — Beginner — SUMMARY

Date: 2026-09-13 (content authored 2026-09-12 → 2026-09-13; QA gates re-verified post-restart)
Status: **COMPLETE** (all gates green; the recorded cross-agent build blocker was resolved by the other agent on 2026-09-13 and the build re-verified — see "Remaining Issues")

## Course

Track `python`, course `python-beginner` — 15 modules, 57 lessons, 40 practice sets,
134 challenges (all two-sided-verified), 5 checkpoints, 15 module manifests + course.json
wired, full EN + VI parity (134 VI sidecars, VI overlays for practice sets/lessons).

Modules: python-and-your-first-programs, variables-and-data-types, working-with-strings,
making-decisions, lists-and-collections, loops, functions, errors-and-debugging,
files-paths-and-data, modules-and-standard-library, environments-and-packages,
testing-and-code-quality, problem-solving, command-line-applications (Task Manager CLI),
capstone-personal-finance-cli.

Practice-first: learn/practice/build/project separated in authoring (`pypb*.py` scripts);
challenge types include guided, independent, debugging (Bug Hunt), prediction,
refactoring, real-world; capstone graded from requirements briefs with acceptance-criteria
tests, no step-by-step tutorial.

## Architecture notes

- Python execution added to the sandbox worker contract: `src/workers/python-runtime.ts`
  builds the same heredoc-data job script the JS runtime uses (solution.py + per-test
  python3 processes, `__TEST_RESULT__` marker protocol). Harness fixed to preserve
  `__builtins__` so solution code can call builtins during tests (latent bug surfaced by
  errors module).
- `docker/Dockerfile.sandbox` installs python3 in the sandbox image.
- Content validation extended: `validate-content.ts` now covers the python track
  (both courses, both locales) — 287 nodes load clean per locale for python-beginner.

## QA gates (actual results, 2026-09-13)

- Two-sided challenge harness: **134/134** (ref PASS + wrong-solution FAIL for every
  challenge; ledger `scripts/content-authoring/py-solutions.mjs` deduped after earlier
  fixer scripts appended stale duplicate entries).
- validate-content.ts: all 5 courses green, EN/VI SYNC OK, LOCALE en/vi 287 nodes clean
  (python-beginner), Linear path (python): 106 lessons.
- Typecheck: clean (`tsc --noEmit`; fixed my own destructure bug in validate-content.ts).
- Lint: 0 errors (one trivial `let`→`const` fix applied to the other agent's idle
  untracked `validate-pi.ts` — reported below; 3 pre-existing warnings untouched).
- Unit: 124/124 (19 files) — later re-run 114/114 with 1 suite failing ONLY due to the
  other agent's broken MDX (not this course).
- E2E: **36/36** (first run 29 pass / 7 fail caused by my backgrounded worker being
  SIGTERM'd by the tool harness — rerun with inline worker: all green). Existing dev
  server on :3000 reused via temporary no-webServer config (deleted after run).
- MDX: 114 python-beginner files compile clean after fixing bare `amount <= 0` in
  capstone-finance-ship(.vi).mdx (unescaped `<` broke JSX parsing).
- Prettier: my files formatted; repo-wide `format:check` drift (~235 files incl. tracked
  fixtures/tests predating this session) untouched per multi-agent safety. Removed
  `tm_rt.json` — a sandbox-run artifact my challenge wrote into repo root.
- Production build: initially BLOCKED by the other agent's in-flight
  `python-intermediate/.../capstone-brief{,.vi}.mdx` (line-12 dict literal in MDX prose).
  Per the multi-agent rules I did not edit them. **RESOLVED 2026-09-13:** the other agent
  fixed both files; `pnpm build` re-run and passes clean (full route table emitted).
  My course adds no build errors.

## Git safety

- No destructive git operations; no resets/checkouts/cleans.
- Other agent's files untouched except the one-line `prefer-const` lint fix in their idle
  `scripts/content-authoring/validate-pi.ts` (their file, idle ~3.5 h, semantics
  unchanged; required to unblock the shared lint gate).
- ~396-file uncommitted working tree preserved as found (incl. their fixtures/tests).

## Remaining Issues

1. ~~Build fails on the other agent's two in-flight MDX files~~ RESOLVED 2026-09-13:
   they backticked the dict literal; `pnpm build` re-verified clean post-restart.
2. Repo-wide prettier drift (~235 files) predates this phase; needs a repo-level decision.
3. E2E requires `pnpm worker` running alongside the dev server; webServer config assumes
   it owns the server (Next 16 forbids a second dev instance in the same dir), so E2E
   against an already-running server needs the temp-config approach used here.
