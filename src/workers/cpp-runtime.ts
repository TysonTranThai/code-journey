/**
 * C++ execution support for the sandbox (C++ — Beginner course).
 *
 * Mirrors the JS/Python job contracts in sandbox.ts / python-runtime.ts:
 * the student solution and the challenge's test snippets are written into
 * /job as heredoc data (never interpreted by sh), then each test runs as
 * its own process and exits 0 (pass) or non-zero (fail). The marker-line
 * protocol is the SAME one execute.ts already parses
 * (`__TEST_RESULT__ <name> status=N`).
 *
 * C++ test contract (challenge authoring):
 *  - Each test file `#include "solution.cpp"` BEFORE the snippet, so the
 *    solution's functions/classes are visible as ordinary declarations —
 *    the preprocessor does the "name injection" Python's exec provided.
 *  - `#define main cj_learner_main` wraps the include: a learner who wrote
 *    their own `int main()` (habit from runnable lessons) cannot collide
 *    with the harness's main at link time. The learner's main never runs.
 *  - The harness redirects std::cout; the snippet runs INSIDE main's try
 *    block and signals failure by throwing (CHECK macros throw
 *    std::runtime_error with an educational message; execute.ts maps the
 *    first stderr line to the test hint, same as Python).
 *  - `capture(fn)` runs `fn()` with std::cout redirected and returns what
 *    it printed — the C++ equivalent of Python's `printed`/`stdout`.
 *  - Graded entry convention: challenges either grade named functions the
 *    solution defines, or a `void program()` the snippet calls via capture.
 *  - Helpers inside a snippet are lambdas or local classes (definitions of
 *    free functions are not possible inside main; lambdas cover the need).
 *
 * The solution is syntax-checked first (`g++ -fsyntax-only`): a solution
 * that does not compile produces NO markers, so execute.ts maps the job to
 * verdict "error" with the compiler output — an educational compile error,
 * not N confusing per-test failures.
 *
 * Exported as the raw module text (same pattern as STUBS_MODULE /
 * PY_TEST_HARNESS) so the worker and the QA harness cannot drift.
 */

/**
 * The C++ harness injected at the top of every test file. Defined once here
 * so the sandbox worker and the content QA harness build byte-identical
 * test files.
 */
import { sanitizeTestName } from "./sanitize-name";

export const CPP_TEST_HARNESS = String.raw`// Code Journey C++ test harness (injected; do not modify).
#include <algorithm>
#include <cctype>
#include <cmath>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <iterator>
#include <limits>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

// The learner's solution is compiled into this test's translation unit,
// so its functions/classes/structs are visible below as ordinary names.
// A learner-written main is renamed so it can never collide with ours.
#define main cj_learner_main
#include "solution.cpp"
#undef main

// Run fn() with std::cout redirected; return everything it printed.
template <typename F>
std::string capture(F&& fn) {
    std::ostringstream _cj_oss;
    auto* _cj_old = std::cout.rdbuf(_cj_oss.rdbuf());
    try {
        fn();
    } catch (...) {
        std::cout.rdbuf(_cj_old);
        throw;
    }
    std::cout.rdbuf(_cj_old);
    return _cj_oss.str();
}

#define CJ_FAIL(msg) throw std::runtime_error(msg)

#define CHECK(cond) \
    do { if (!(cond)) CJ_FAIL(std::string("check failed: ") + #cond); } while (0)

// CHECK_EQ renders both operands with operator<< into the failure message.
#define CHECK_EQ(a, b) \
    do { \
        const auto& _cj_a = (a); \
        const auto& _cj_b = (b); \
        if (!(_cj_a == _cj_b)) { \
            std::ostringstream _cj_m; \
            _cj_m << "expected " << #a << " == " << #b \
                  << " but got " << _cj_a << " vs " << _cj_b; \
            CJ_FAIL(_cj_m.str()); \
        } \
    } while (0)

#define CHECK_NE(a, b) \
    do { if (!((a) != (b))) CJ_FAIL(std::string("expected ") + #a + " != " + #b); } while (0)

#define CHECK_CONTAINS(haystack, needle) \
    do { \
        const std::string& _cj_h = (haystack); \
        const std::string& _cj_n = (needle); \
        if (_cj_h.find(_cj_n) == std::string::npos) { \
            CJ_FAIL("expected output to contain \"" + _cj_n + "\""); \
        } \
    } while (0)

// CHECK_LINES(haystack, "a", "b", ...) — every fragment must appear, in
// order (multi-line output checked without newline escapes in literals).
// Variadic: macro arguments are split at top-level commas by the
// PREPROCESSOR (braces do NOT protect commas in macro invocations), so the
// brace form used by early drafts was a hard compile error.
inline void cj_check_lines(const std::string& _cj_h, std::initializer_list<const char*> _cj_needles) {
    std::size_t _cj_from = 0;
    for (const char* _cj_n : _cj_needles) {
        const std::size_t _cj_p = _cj_h.find(_cj_n, _cj_from);
        if (_cj_p == std::string::npos) {
            CJ_FAIL(std::string("expected output to contain, in order: \"") + _cj_n + "\"");
        }
        _cj_from = _cj_p + std::strlen(_cj_n);
    }
}

#define CHECK_LINES(haystack, ...) \
    do { \
        const std::string& _cj_h = (haystack); \
        cj_check_lines(_cj_h, { __VA_ARGS__ }); \
    } while (0)

#define CHECK_NEAR(a, b, eps) \
    do { \
        double _cj_a = (a); \
        double _cj_b = (b); \
        double _cj_e = (eps); \
        if (!(std::fabs(_cj_a - _cj_b) <= _cj_e)) { \
            std::ostringstream _cj_m; \
            _cj_m << "expected " << #a << " ~= " << _cj_b \
                  << " within " << _cj_e << ", got " << _cj_a; \
            CJ_FAIL(_cj_m.str()); \
        } \
    } while (0)

// CHECK_THROWS(stmt...) — the statement must throw (any exception).
// Variadic statement form: a plain "fn" parameter would expand as "fn()",
// calling the RESULT of the author's expression instead of the expression.
#define CHECK_THROWS(...) \
    do { \
        bool _cj_threw = false; \
        try { __VA_ARGS__; } catch (...) { _cj_threw = true; } \
        if (!_cj_threw) CJ_FAIL("expected an exception but none was thrown"); \
    } while (0)
`;

/** Runtime compile flags for challenge builds (C++20 baseline). */
export const CPP_STANDARD_FLAG = "-std=c++20";
export const CPP_TEST_WARNING_FLAGS = "-Wall -Wextra -Wpedantic";

export type CppJobInput = {
  code: string;
  testFiles: { name: string; code: string }[];
};

/** Sanitize a test name into a safe C++ filename fragment (mirrors worker). */
export function cppSanitizeName(name: string): string {
  // Shared diacritic-preserving sanitizer (Vietnamese names stay readable).
  return sanitizeTestName(name);
}

/**
 * Build one test translation unit: harness + the author's snippet (as the
 * body of main, inside its try block) + PASS/exit-code protocol. The
 * snippet is indented into main; preprocessor directives inside the snippet
 * keep their leading `#` (legal with indentation).
 */
export function buildCppTestFile(test: { name: string; code: string }): string {
  // Indent the author snippet into main's try block (4 spaces), preserving
  // blank lines (preprocessor "#" lines stay valid when indented).
  const indented = test.code
    .split("\n")
    .map((line) => (line.trim().length > 0 ? `    ${line}` : line))
    .join("\n");
  return [
    CPP_TEST_HARNESS,
    "int main() {",
    "    try {",
    indented,
    '        std::cout << "PASS" << std::endl;',
    "        return 0;",
    "    } catch (const std::exception& _cj_e) {",
    '        std::cerr << _cj_e.what() << std::endl;',
    "        return 1;",
    "    } catch (...) {",
    '        std::cerr << "test failed: unexpected exception" << std::endl;',
    "        return 1;",
    "    }",
    "}",
  ].join("\n");
}

/**
 * Full POSIX sh job script for a C++ run. Same heredoc strategy, same
 * marker protocol, same per-test isolation as the JS/Python paths.
 *
 * Flow: write solution.cpp → syntax-check it (no markers on failure, so a
 * compile error surfaces as verdict "error" with the compiler output) →
 * write each test .cpp → compile+run each test → marker line per test.
 * Binaries are compiled to /tmp, which the sandbox mounts exec-able
 * (nosuid/nodev retained) so the graded test binaries can run; chmod +x is
 * still required because files created by shell redirection lack the exec
 * bit under the container's umask. /job stays noexec (data only). Per-test
 * build logs go to /job/_build-<name>.log and are echoed to stderr only on
 * failure (keeps success stderr clean for the hint channel).
 */
export function buildCppJobScript(job: CppJobInput, delim: string): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.cpp", job.code, delim));
  // Solution must compile on its own before any test runs.
  parts.push(
    [
      `g++ ${CPP_STANDARD_FLAG} -fsyntax-only solution.cpp 2> /job/_syntax.log`,
      "if [ $? -ne 0 ]; then",
      '  echo "Your code did not compile. Compiler output:" >&2',
      "  cat /job/_syntax.log >&2",
      "  exit 1",
      "fi",
    ].join("\n"),
  );
  for (const test of job.testFiles) {
    const name = cppSanitizeName(test.name);
    parts.push(heredoc(`test-${name}.cpp`, buildCppTestFile(test), delim));
  }
  for (const test of job.testFiles) {
    const name = cppSanitizeName(test.name);
    parts.push(
      [
        `g++ ${CPP_STANDARD_FLAG} ${CPP_TEST_WARNING_FLAGS} -o "/tmp/t-${name}" "test-${name}.cpp" 2> "/job/_build-${name}.log"`,
        `if [ $? -ne 0 ]; then echo "__TEST_RESULT__ ${name} status=1"; cat "/job/_build-${name}.log" >&2; continue; fi`,
        `chmod +x "/tmp/t-${name}"`,
        `"/tmp/t-${name}" 2> "/job/_run-${name}.log"`,
        `status=$?`,
        `echo "__TEST_RESULT__ ${name} status=$status"`,
        `if [ $status -ne 0 ] && [ -s "/job/_run-${name}.log" ]; then cat "/job/_run-${name}.log" >&2; fi`,
        `if [ $status -ne 0 ] && [ -s "/job/_build-${name}.log" ]; then cat "/job/_build-${name}.log" >&2; fi`,
      ].join("\n"),
    );
  }
  return parts.join("\n") + "\n";
}

/** Quoted-delimiter heredoc (no interpolation) — same as sandbox.ts. */
function heredoc(name: string, content: string, delim: string): string {
  return `cat > "${name}" << '${delim}'\n${content}\n${delim}`;
}
