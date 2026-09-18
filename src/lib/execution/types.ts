/**
 * Typed verdict + job model shared between the web tier, the queue, and the
 * runner worker (03-CONTEXT D-05).
 *
 * The web tier may enqueue jobs and read verdicts; it never executes code.
 * Job payloads carry ONLY code + tests + limits — never env vars or secrets.
 */

export type ExecutionStatus = "queued" | "claimed" | "running" | "completed" | "failed";

export type Verdict = "passed" | "failed" | "timeout" | "error";

/**
 * One test's outcome. `message` is the educational hint shown to the student
 * on failure (CHAL-05) — never a bare boolean.
 */
export interface PerTestResult {
  name: string;
  passed: boolean;
  message: string;
}

/**
 * Written once by the runner worker into the job row (and mirrored onto the
 * submission). `output` is truncated at write time (OUTPUT_LIMIT_CHARS) and
 * never contains env/secrets.
 */
export interface VerdictPayload {
  verdict: Verdict;
  perTestResults: PerTestResult[];
  runtimeMs: number | null;
  output: string;
}

/**
 * Everything the sandbox needs. This is the ONLY data that crosses the
 * web-tier → queue → worker boundary.
 */
export interface JobPayload {
  code: string;
  testFiles: { name: string; code: string }[];
  timeoutMs: number;
  memoryMb: number;
  /** Execution language (Python, C++, Java, C, and C# tracks). Default "javascript". */
  language?: "javascript" | "python" | "cpp" | "java" | "c" | "csharp";
}

/** Hard cap so a runaway console.log can't flood the verdict payload. */
export const OUTPUT_LIMIT_CHARS = 10_000;

export function truncateOutput(output: string): string {
  return output.length > OUTPUT_LIMIT_CHARS
    ? output.slice(0, OUTPUT_LIMIT_CHARS) + "\n… (output truncated)"
    : output;
}
