import type { Dictionary } from "@/lib/i18n/dictionaries";

export interface ErrorExplanation {
  message: string;
  hint: string;
}

/**
 * Parses raw compiler, runtime, or worker error output and provides
 * a learner-friendly translated explanation and actionable hint (Socratic pedagogy).
 */
export function getErrorExplanation(
  rawError: string,
  d: Dictionary,
  language?: string,
): ErrorExplanation | null {
  if (!rawError || rawError.trim().length === 0) return null;

  const text = rawError.trim();
  const isC = language === "c" || language === "cpp";

  // 1. C/C++ in JavaScript console: "#include" parsed as private class field, or C code in JS worker
  if (
    text.includes("Private field '#include'") ||
    (text.includes("Private field") && text.includes("#include")) ||
    (text.includes("#include") && (text.includes("Private field") || text.includes("SyntaxError"))) ||
    (text.includes("Error:") && text.includes("#include")) ||
    (isC &&
      (text.includes("SyntaxError") ||
        text.includes("Unexpected token") ||
        text.includes("Unexpected identifier")))
  ) {
    return {
      message: d.console.explainPrivateFieldInclude,
      hint: d.console.explainPrivateFieldIncludeHint,
    };
  }

  // 2. Syntax errors (unexpected token, identifier, invalid syntax)
  if (
    text.includes("SyntaxError") ||
    text.includes("Unexpected token") ||
    text.includes("Unexpected identifier") ||
    text.includes("Invalid or unexpected token")
  ) {
    return {
      message: d.console.explainSyntaxError,
      hint: d.console.explainSyntaxErrorHint,
    };
  }

  // 3. Reference errors (variable / identifier is not defined)
  if (text.includes("ReferenceError") || text.includes("is not defined")) {
    return {
      message: d.console.explainReferenceError,
      hint: d.console.explainReferenceErrorHint,
    };
  }

  // 4. Type errors (calling non-function, reading property of null/undefined)
  if (
    text.includes("TypeError") ||
    text.includes("is not a function") ||
    text.includes("Cannot read properties of") ||
    text.includes("Cannot read property of")
  ) {
    return {
      message: d.console.explainTypeError,
      hint: d.console.explainTypeErrorHint,
    };
  }

  // 5. Range errors (maximum call stack size exceeded / infinite recursion)
  if (text.includes("RangeError") || text.includes("Maximum call stack size exceeded")) {
    return {
      message: d.console.explainRangeError,
      hint: d.console.explainRangeErrorHint,
    };
  }

  // 6. Timeout / Stopped after 2.5s (infinite loop)
  if (
    text.includes("kiểm tra vòng lặp vô hạn") ||
    text.includes("check for infinite loops") ||
    text.includes("chạy quá") ||
    text.includes("ran longer than")
  ) {
    return {
      message: d.console.explainTimeout,
      hint: d.console.explainTimeoutHint,
    };
  }

  // 7. Test assertion failure
  if (text.includes("AssertionError") || (text.includes("expected") && text.includes("to be"))) {
    return {
      message: d.console.explainAssertionError,
      hint: d.console.explainAssertionErrorHint,
    };
  }

  // 8. General runtime error
  if (text.startsWith("Error:") || text.includes("Error:") || text.startsWith("Lỗi:")) {
    return {
      message: d.console.explainGenericError,
      hint: d.console.explainGenericErrorHint,
    };
  }

  return null;
}
