/**
 * C execution support for the sandbox (C — Beginner course).
 *
 * Mirrors the C++ job contract in cpp-runtime.ts (same heredoc strategy, same
 * `__TEST_RESULT__ <name> status=N` marker protocol, same syntax gate), with
 * a C-specific failure protocol: **no exceptions** — CHECK macros set a
 * message and longjmp to a guard in main.
 *
 * C test contract (challenge authoring):
 *  - Each test file `#include "solution.c"` AFTER `#define main
 *    cj_learner_main`, so a learner-written main cannot collide with the
 *    harness main at link time (the learner's main never runs).
 *  - Helpers inside a snippet are `static` functions at file scope (legal in
 *    C, unlike C++ main-scope restrictions).
 *  - `cj_capture(fn)` redirects fd 1 through a pipe + dup2 and returns
 *    everything `fn()` printed — the graded entry convention is `void
 *    program()` for output challenges.
 *  - Solution is syntax-gated first (`gcc -std=c23 -fsyntax-only`): a solution
 *    that does not compile produces NO markers, so execute.ts maps the job to
 *    verdict "error" with the compiler output.
 *
 * Standard: C23 baseline (`-std=c23`, GCC 14.2.0 in the sandbox image —
 * probed 2026-09-14, see docs/CURRICULUM-RESEARCH-C-BEGINNER.md). ASan is NOT
 * available in the image (Alpine splits sanitizers out; probe failed to link)
 * — no sanitizer claims exist in this runtime or course.
 *
 * Exported as raw module text (same pattern as CPP_TEST_HARNESS) so the
 * worker and the content QA harness cannot drift.
 */

import { sanitizeTestName } from "./sanitize-name";

/**
 * The C harness injected at the top of every test file. Defined once here so
 * the sandbox worker and the QA harness build byte-identical test files.
 */
export const C_TEST_HARNESS = String.raw`/* Code Journey C test harness (injected; do not modify). */
#include <setjmp.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

/* The learner's solution is compiled into this test's translation unit, so
   its functions/structs/globals are visible below as ordinary names. A
   learner-written main is renamed so it can never collide with ours. */
#define main cj_learner_main
#include "solution.c"
#undef main

static jmp_buf cj_env;
static char cj_msg[512];

static void cj_fail(const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    vsnprintf(cj_msg, sizeof cj_msg, fmt, ap);
    va_end(ap);
    longjmp(cj_env, 1);
}

/* Run fn() with fd 1 redirected into a pipe; return everything it printed
   (up to 8 KiB — challenges never print more). Marked used: unused-in-a-given-
   test warnings would pollute the failure-hint channel. */
static char cj_cap_buf[8192] __attribute__((unused));
static const char *cj_capture(void (*fn)(void)) __attribute__((unused));
static const char *cj_capture(void (*fn)(void)) {
    int saved = dup(1);
    int fds[2];
    if (pipe(fds) != 0) cj_fail("harness: pipe failed");
    fflush(stdout);
    dup2(fds[1], 1);
    close(fds[1]);
    fn();
    fflush(stdout);
    ssize_t n = read(fds[0], cj_cap_buf, sizeof cj_cap_buf - 1);
    if (n < 0) n = 0;
    cj_cap_buf[n] = '\0';
    dup2(saved, 1);
    close(saved);
    close(fds[0]);
    if (n > 0) {
        fwrite(cj_cap_buf, 1, (size_t)n, stdout);
        fflush(stdout);
    }
    return cj_cap_buf;
}

#define CHECK(cond) \
    do { if (!(cond)) cj_fail("check failed: %s", #cond); } while (0)

/* Integer equality with the operands shown in the failure message. */
#define CHECK_EQ(a, b) \
    do { \
        long long _cja = (long long)(a); \
        long long _cjb = (long long)(b); \
        if (_cja != _cjb) cj_fail("expected %s == %s but got %lld vs %lld", #a, #b, _cja, _cjb); \
    } while (0)

/* Floating equality within an absolute epsilon (doubles rendered via %.6g). */
#define CHECK_NEAR(a, b, eps) \
    do { \
        double _cja = (double)(a); \
        double _cjb = (double)(b); \
        double _cje = (double)(eps); \
        if (!(_cja - _cjb <= _cje && _cjb - _cja <= _cje)) \
            cj_fail("expected %s ~= %s within %g, got %.6g", #a, #b, _cje, _cja); \
    } while (0)

/* C-string equality (either side may be NULL -> fails with a message). */
#define CHECK_STR_EQ(got, want) \
    do { \
        const char *_cjg = (got); \
        const char *_cjw = (want); \
        if (_cjg == NULL || _cjw == NULL) { \
            if (_cjg != _cjw) cj_fail("expected %s == \"%s\" but got NULL", #got, #want); \
        } else if (strcmp(_cjg, _cjw) != 0) { \
            cj_fail("expected %s == \"%s\" but got \"%s\"", #got, #want, _cjg); \
        } \
    } while (0)

#define CHECK_NULL(p) \
    do { if ((p) != NULL) cj_fail("expected %s to be NULL", #p); } while (0)

#define CHECK_NOT_NULL(p) \
    do { if ((p) == NULL) cj_fail("expected %s to be non-NULL", #p); } while (0)

/* Substring containment (needle must appear in the captured output). */
#define CHECK_CONTAINS(haystack, needle) \
    do { \
        const char *_cjh = (haystack); \
        const char *_cjn = (needle); \
        if (_cjh == NULL || _cjn == NULL || strstr(_cjh, _cjn) == NULL) { \
            cj_fail("expected output to contain \"%s\"", _cjn ? _cjn : "(null)"); \
        } \
    } while (0)
`;

export const C_STANDARD_FLAG = "-std=c23";
export const C_TEST_WARNING_FLAGS = "-Wall -Wextra -Wpedantic";

export type CJobInput = {
  code: string;
  testFiles: { name: string; code: string }[];
};

/** Sanitize a test name into a safe C filename fragment (mirrors worker). */
export function cSanitizeName(name: string): string {
  return sanitizeTestName(name);
}

/**
 * Build one test translation unit: harness + the author's snippet (as the
 * body of cj_test_body) + PASS/exit-code protocol.
 */
export function buildCTestFile(test: { name: string; code: string }): string {
  const indented = test.code
    .split("\n")
    .map((line) => (line.trim().length > 0 ? `    ${line}` : line))
    .join("\n");
  return [
    C_TEST_HARNESS,
    "",
    "/* author snippet (function cj_test_body) — defined before main so the",
    "   C23 no-implicit-declaration rule never bites. */",
    "static void cj_test_body(void) {",
    indented,
    "}",
    "",
    "int main(void) {",
    "    if (setjmp(cj_env) == 0) {",
    "        cj_test_body();",
    '        printf("PASS\\n");',
    "        return 0;",
    "    }",
    '    fprintf(stderr, "%s\\n", cj_msg);',
    "    return 1;",
    "}",
  ].join("\n");
}

/**
 * Full POSIX sh job script for a C run. Same heredoc strategy, same marker
 * protocol, same per-test isolation as the C++ path.
 */
export function buildCJobScript(job: CJobInput, delim: string): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("solution.c", job.code, delim));
  // Solution must compile on its own before any test runs.
  parts.push(
    [
      `gcc ${C_STANDARD_FLAG} -fsyntax-only solution.c 2> /job/_syntax.log`,
      "if [ $? -ne 0 ]; then",
      '  echo "Your code did not compile. Compiler output:" >&2',
      "  cat /job/_syntax.log >&2",
      "  exit 1",
      "fi",
    ].join("\n"),
  );
  for (const test of job.testFiles) {
    const name = cSanitizeName(test.name);
    parts.push(heredoc(`test-${name}.c`, buildCTestFile(test), delim));
  }
  for (const test of job.testFiles) {
    const name = cSanitizeName(test.name);
    parts.push(
      [
        `gcc ${C_STANDARD_FLAG} ${C_TEST_WARNING_FLAGS} -o "/tmp/t-${name}" "test-${name}.c" -lm 2> "/job/_build-${name}.log"`,
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
