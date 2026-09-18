/**
 * Java execution support for the sandbox (Java — Beginner course).
 *
 * Mirrors the JS/Python/C++ job contracts in sandbox.ts / python-runtime.ts /
 * cpp-runtime.ts: the student solution and the challenge's test snippets are
 * written into /job as heredoc data (never interpreted by sh), then each test
 * runs as its own JVM process and exits 0 (pass) or non-zero (fail). The
 * marker-line protocol is the SAME one execute.ts already parses
 * (`__TEST_RESULT__ <name> status=N`).
 *
 * Java test contract (challenge authoring):
 *  - Each test file declares `import cj.harness.*;` and `import
 *    cj.learner.Solution;`… EXCEPT the harness cannot use a package for the
 *    solution: javac has no `#include`. Instead the solution is compiled as
 *    its own unit `Solution.java` (class `Solution`, no package statement —
 *    the unnamed package, like the C++ `solution.cpp` convention) and each
 *    test is compiled together with it: `javac Solution.java Test_x.java`.
 *  - The harness class `Cj` lives in the test file itself (generated, same
 *    single-file-compile-unit trick as the C++ harness): static CHECK-style
 *    methods throw RuntimeException with an educational message; `capture`
 *    redirects System.out and returns what was printed.
 *  - A learner-written `public static void main` inside Solution can never
 *    collide: the harness main is in the generated test class, and Solution's
 *    main is simply never invoked.
 *  - Graded entry convention: challenges grade named static members the
 *    Solution class defines (methods/fields/nested types), or a
 *    `static void program()` the snippet calls via Cj.capture(...).
 *  - Helpers inside snippets are local classes or lambdas (like C++).
 *
 * The solution is syntax-checked first (`javac -proc:none -d /tmp
 * Solution.java`): a solution that does not compile produces NO markers, so
 * execute.ts maps the job to verdict "error" with the compiler output — an
 * educational compile error, not N confusing per-test failures.
 *
 * Exported as raw module text (same pattern as CPP_TEST_HARNESS) so the
 * worker and the QA harness cannot drift.
 */

import { sanitizeTestName } from "./sanitize-name";

/**
 * The Java harness prepended to every generated test file. One public class
 * per file (Java rule), named after the file; helper `Cj` is a nested static
 * class. Defined once here so the sandbox worker and the content QA harness
 * build byte-identical test files.
 */
export const JAVA_TEST_HARNESS_PRELUDE = String.raw`// Code Journey Java test harness (injected; do not modify).
import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.TreeMap;
import java.util.TreeSet;
import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Iterator;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.Objects;
import java.util.regex.Pattern;
import java.util.stream.Collectors;
import java.util.stream.Stream;
// Advanced-course prelude extension (Phase 20): on-demand imports so advanced
// snippets can use concurrency/network/IO/annotation/reflection APIs without
// per-test import noise. Single-type imports above still win over these;
// existing challenges are unaffected (unused on-demand imports are legal).
import java.util.concurrent.*;
import java.util.concurrent.atomic.*;
import java.util.concurrent.locks.*;
import java.net.*;
import java.nio.file.*;
import java.lang.annotation.*;
import java.lang.reflect.*;
import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Shared test utilities: CHECK-style assertions throw RuntimeException with
 * an educational message; capture() runs code with System.out redirected and
 * returns what it printed.
 */
class CjTestBase {
    static void fail(String msg) { throw new RuntimeException(msg); }

    static void check(boolean cond, String what) {
        if (!cond) fail("check failed: " + what);
    }

    static void checkEq(Object actual, Object expected, String what) {
        if (!same(actual, expected)) {
            fail(what + " — expected " + render(expected) + " but got " + render(actual));
        }
    }

    /** Array-aware equality: Objects.equals compares arrays by identity. */
    static boolean same(Object a, Object b) {
        if (a == null || b == null) return a == b;
        if (a instanceof int[] x && b instanceof int[] y) return Arrays.equals(x, y);
        if (a instanceof long[] x && b instanceof long[] y) return Arrays.equals(x, y);
        if (a instanceof double[] x && b instanceof double[] y) return Arrays.equals(x, y);
        if (a instanceof boolean[] x && b instanceof boolean[] y) return Arrays.equals(x, y);
        if (a instanceof Object[] x && b instanceof Object[] y) return Arrays.deepEquals(x, y);
        return a.equals(b);
    }

    static void checkTrue(boolean cond, String what) {
        if (!cond) fail(what);
    }

    static void checkContains(String haystack, String needle) {
        if (!haystack.contains(needle)) {
            fail("expected output to contain \"" + needle + "\"");
        }
    }

    /** Every fragment must appear, in order (multi-line output without newline escapes). */
    static void checkLines(String haystack, String... needles) {
        int from = 0;
        for (String n : needles) {
            int p = haystack.indexOf(n, from);
            if (p < 0) fail("expected output to contain, in order: \"" + n + "\"");
            from = p + n.length();
        }
    }

    static void checkNear(double actual, double expected, double eps, String what) {
        if (!(Math.abs(actual - expected) <= eps)) {
            fail(what + " — expected ~" + expected + " within " + eps + ", got " + actual);
        }
    }

    /** The statement must throw (any RuntimeException or Exception). */
    static void checkThrows(Runnable r, String what) {
        try {
            r.run();
        } catch (RuntimeException e) {
            return;
        } catch (Error e) {
            return;
        }
        fail(what + " — expected an exception but none was thrown");
    }

    /** Run code with System.out redirected; return everything it printed. */
    static String capture(Runnable r) {
        PrintStream old = System.out;
        ByteArrayOutputStream buf = new ByteArrayOutputStream();
        System.setOut(new PrintStream(buf, true, StandardCharsets.UTF_8));
        try {
            r.run();
        } finally {
            System.out.flush();
            System.setOut(old);
        }
        return buf.toString(StandardCharsets.UTF_8);
    }

    private static String render(Object o) {
        if (o == null) return "null";
        if (o instanceof String s) return "\"" + s + "\"";
        if (o instanceof Object[] arr) return Arrays.toString(arr);
        if (o instanceof int[] arr) return Arrays.toString(arr);
        if (o instanceof long[] arr) return Arrays.toString(arr);
        if (o instanceof double[] arr) return Arrays.toString(arr);
        if (o instanceof boolean[] arr) return Arrays.toString(arr);
        return String.valueOf(o);
    }
}
`;

/** Java language level for challenge builds (modern baseline: Java 21 LTS features). */
export const JAVA_RELEASE_FLAG = "--release 21";
/** The same flag split for spawnSync-style invocations (QA harness). */
export const JAVA_RELEASE_ARGS: readonly string[] = ["--release", "21"];

/** Compiler note flags for test builds (loud, not fatal). */
export const JAVA_TEST_WARNING_FLAGS = "-Xlint:all,-serial,-this-escape";

export type JavaJobInput = {
  code: string;
  testFiles: { name: string; code: string }[];
};

/** Sanitize a test name into a safe Java class-name fragment (mirrors worker). */
export function javaSanitizeName(name: string): string {
  // Class-fragment sanitizer: letters/digits/underscore, starting with a
  // letter; Vietnamese diacritics are stripped to their ASCII base by the
  // shared sanitizer, and a leading digit is prefixed to stay legal.
  const base = sanitizeTestName(name).replace(/[^A-Za-z0-9_]/g, "");
  return /^[0-9]/.test(base) ? `T${base}` : base || "Test";
}

/**
 * Build one test compilation unit: prelude (imports + Cj helpers) + the
 * author's snippet wrapped in a public test class whose main() runs inside a
 * broad try/catch and signals PASS/exit-code protocol. The snippet is placed
 * inside main as statements — helper local classes and lambdas are legal
 * there, same as the C++ snippet-in-main convention.
 */
export function buildJavaTestFile(test: { name: string; code: string }): string {
  const className = `Test_${javaSanitizeName(test.name)}`;
  // Indent the author snippet into main's try block (8 spaces inside the
  // class+method nesting), preserving blank lines.
  const indented = test.code
    .split("\n")
    .map((line) => (line.trim().length > 0 ? `        ${line}` : line))
    .join("\n");
  return [
    JAVA_TEST_HARNESS_PRELUDE,
    `public class ${className} extends CjTestBase {`,
    "    public static void main(String[] args) {",
    "        try {",
    indented,
    '            System.out.println("PASS");',
    "            return;",
    "        } catch (RuntimeException e) {",
    "            System.err.println(e.getMessage());",
    "            System.exit(1);",
    "        } catch (Exception e) {",
    '            System.err.println("test failed: " + e);',
    "            System.exit(1);",
    "        }",
    "    }",
    "}",
  ].join("\n");
}

/**
 * Full POSIX sh job script for a Java run. Same heredoc strategy, same
 * marker protocol, same per-test isolation as the JS/Python/C++ paths.
 *
 * Flow: write Solution.java → syntax-check it (no markers on failure, so a
 * compile error surfaces as verdict "error" with the compiler output) →
 * write each test .java → compile Solution+test together (javac accepts
 * multiple files; classes land in /tmp/classes on the tmpfs) → run each
 * test JVM → marker line per test.
 *
 * Javac notes: `-d /tmp/classes` writes .class files to exec-able tmpfs;
 * `--release 21` pins the language level; `-nowarn` keeps success output
 * clean. The JVM runs with the same /tmp exec-able tmpfs the C++ binaries
 * use. Each test compiles afresh (the compiler recompiles Solution.java
 * alongside the test — single source-dir state, no stale-class risk).
 */
export function buildJavaJobScript(job: JavaJobInput, delim: string): string {
  const parts: string[] = ["set -u", "cd /job"];
  parts.push(heredoc("Solution.java", job.code, delim));
  // Solution must compile on its own before any test runs.
  parts.push(
    [
      `mkdir -p /tmp/classes && javac ${JAVA_RELEASE_FLAG} -nowarn -d /tmp/classes Solution.java 2> /job/_syntax.log`,
      "if [ $? -ne 0 ]; then",
      '  echo "Your code did not compile. Compiler output:" >&2',
      "  cat /job/_syntax.log >&2",
      "  exit 1",
      "fi",
    ].join("\n"),
  );
  for (const test of job.testFiles) {
    const name = javaSanitizeName(test.name);
    parts.push(heredoc(`Test_${name}.java`, buildJavaTestFile(test), delim));
  }
  for (const test of job.testFiles) {
    const name = javaSanitizeName(test.name);
    // Learner-visible marker name: the author's test name with whitespace
    // collapsed to dashes (execute.ts parses these and shows them as test
    // names). File/class names stay class-safe; markers stay readable.
    const markerName = test.name.replace(/\s+/g, "-");
    parts.push(
      [
        `rm -rf /tmp/classes && mkdir -p /tmp/classes`,
        `javac ${JAVA_RELEASE_FLAG} -nowarn -d /tmp/classes Solution.java "Test_${name}.java" 2> "/job/_build-${name}.log"`,
        `if [ $? -ne 0 ]; then echo "__TEST_RESULT__ ${markerName} status=1"; cat "/job/_build-${name}.log" >&2; continue; fi`,
        `java -XX:+UseSerialGC -Xss4m -cp /tmp/classes "Test_${name}" 2> "/job/_run-${name}.log"`,
        `status=$?`,
        `echo "__TEST_RESULT__ ${markerName} status=$status"`,
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
