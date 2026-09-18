/**
 * Python execution support for the sandbox (Python — Beginner course).
 *
 * Mirrors the JS job contract in sandbox.ts: the student solution and the
 * challenge's test snippets are written into /job as heredoc data (never
 * interpreted by sh), then each test file runs as its own `python3` process
 * and exits 0 (pass) or non-zero (fail). The marker-line protocol is the
 * SAME one execute.ts already parses (`__TEST_RESULT__ <name> status=N`).
 *
 * Python test contract (challenge authoring):
 *  - A test file receives the student's solution already executed, with the
 *    solution's top-level names in scope, PLUS `printed` (list of strings the
 *    solution printed to stdout) and `stdout` (full captured output string).
 *  - `builtins.input` is replaced with a clear failure — challenges grade
 *    parameters/returns/printed output; interactive scripts are run locally.
 *  - Author snippets raise AssertionError (or any exception) to fail a test.
 *
 * Exported as the raw module text (same pattern as STUBS_MODULE) so both the
 * worker and the QA harness build byte-identical test files.
 */

import { sanitizeTestName } from "./sanitize-name";

/**
 * The runner script injected into every Python test file. Defined once here
 * so the sandbox worker and the content QA harness cannot drift.
 */
export const PY_TEST_HARNESS = String.raw`
import builtins as _builtins
import io as _io
import json as _json
import sys as _sys
from contextlib import redirect_stdout as _redirect_stdout


def _run_solution():
    _buf = _io.StringIO()
    _g = {"__name__": "__solution__", "__builtins__": _builtins}
    with _redirect_stdout(_buf):
        exec(_SOLUTION_SOURCE, _g)
    return _buf.getvalue(), _g


_STDOUT_TEXT, _GLOBALS = _run_solution()
printed = [line for line in _STDOUT_TEXT.splitlines()]
stdout = _STDOUT_TEXT
code = _SOLUTION_SOURCE  # learner's raw source, mirroring the JS test contract

# Make the solution's top-level names directly visible to author snippets:
# tests reference add(), prices, etc. as bare names, exactly as if the
# solution module had been imported into this file's namespace. Keep
# __builtins__ in _GLOBALS: functions defined by the solution hold this dict
# as their globals, so builtins (sum, len, ValueError...) must resolve through
# it when tests call those functions later. _GLOBALS also carries the
# solution's __name__ ("__solution__": its if-__main__ guard intentionally
# does NOT run during grading), so restore this test module's real __name__
# afterwards.
globals().update(_GLOBALS)
__name__ = "__main__"


def _no_input(*_a, **_k):
    raise AssertionError(
        "input() is not available in graded challenge runs - "
        "challenge solutions take parameters or print output. "
        "Run interactive versions of programs locally."
    )


_builtins.input = _no_input
`;

export type PyJobInput = {
  code: string;
  testFiles: { name: string; code: string }[];
};

/** Sanitize a test name into a safe Python filename fragment (mirrors worker). */
export function pySanitizeName(name: string): string {
  // Shared diacritic-preserving sanitizer (Vietnamese names stay readable).
  return sanitizeTestName(name);
}

/**
 * Full POSIX sh job script for a Python run. Same heredoc strategy, same
 * marker protocol, and the same per-test isolation as the JS path.
 */
export function buildPyJobScript(job: PyJobInput, delim: string): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.py", job.code, delim));
  // The harness is injected at the TOP of every test file so author snippets
  // only contain their own assertions (same ergonomics as the JS stubs.mjs).
  for (const test of job.testFiles) {
    // Author snippets arrive unindented; indent them under the try: block.
    // (Multi-line template strings swallow leading whitespace, so the runtime
    // must be robust to arbitrary snippet indentation — textwrap.indent is
    // applied only to non-empty lines.)
    const indented = test.code
      .split("\n")
      .map((line) => (line.trim().length > 0 ? `  ${line}` : line))
      .join("\n");
    const testFile = [
      "import sys",
      `with open('/job/solution.py', 'r', encoding='utf-8') as _f:`,
      "    _SOLUTION_SOURCE = _f.read()",
      PY_TEST_HARNESS,
      "try:",
      indented,
      '  print("PASS")',
      "except BaseException as _err:",
      "  print(_err, file=sys.stderr)",
      "  sys.exit(1)",
    ].join("\n");
    parts.push(heredoc(`test-${pySanitizeName(test.name)}.py`, testFile, delim));
  }
  for (const test of job.testFiles) {
    parts.push(
      `python3 "test-${pySanitizeName(test.name)}.py" ; ` +
        `echo "__TEST_RESULT__ ${pySanitizeName(test.name)} status=$?"`,
    );
  }
  return parts.join("\n") + "\n";
}

/** Quoted-delimiter heredoc (no interpolation) — same as sandbox.ts. */
function heredoc(name: string, content: string, delim: string): string {
  return `cat > "${name}" << '${delim}'\n${content}\n${delim}`;
}
