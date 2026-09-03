import "server-only";

/**
 * Observability seam (06-03). Vendor-neutral by design: structured JSON log
 * lines plus a single error-capture hook. No SDK is wired today; when an
 * observability provider is chosen, only these two functions change —
 * call sites stay untouched.
 *
 * Rules:
 *  - NEVER log student code, environment variables, secrets, or tokens.
 *  - Job/execution logs carry job ids and statuses only.
 *  - `captureError` is the single funnel for unexpected errors; dev prints to
 *    console.error, and the seam notes where a vendor (Sentry-style) hooks in.
 */

type LogData = Record<string, unknown>;

function emit(level: "info" | "warn" | "error", scope: string, message: string, data?: LogData) {
  const line = JSON.stringify({
    ts: new Date().toISOString(),
    level,
    scope,
    msg: message,
    ...(data ? { data: redact(data) } : {}),
  });
  if (level === "error") console.error(line);
  else if (level === "warn") console.warn(line);
  else console.log(line);
}

/**
 * Strip keys that commonly carry secrets. Deliberately conservative: if a
 * value looks like it might be sensitive, it is replaced, not logged.
 */
const REDACT_KEYS = /^(password|token|secret|authorization|cookie|apikey|api_key|env)$/i;

function redact(data: LogData): LogData {
  const out: LogData = {};
  for (const [key, value] of Object.entries(data)) {
    out[key] = REDACT_KEYS.test(key) ? "[redacted]" : value;
  }
  return out;
}

export function logEvent(scope: string, message: string, data?: LogData): void {
  emit("info", scope, message, data);
}

export function logWarn(scope: string, message: string, data?: LogData): void {
  emit("warn", scope, message, data);
}

export function logError(scope: string, message: string, data?: LogData): void {
  emit("error", scope, message, data);
}

/**
 * Capture an unexpected error. Dev behavior: structured console output.
 * Production seam: replace the body with the chosen vendor's SDK call —
 * the single place anyone should need to touch.
 */
export function captureError(scope: string, err: unknown, context?: LogData): void {
  const message = err instanceof Error ? err.message : String(err);
  const stack = err instanceof Error ? err.stack : undefined;
  emit("error", scope, message, {
    ...context,
    // Stacks can contain filesystem paths — acceptable server-side, and the
    // key name is kept out of the REDACT pattern.
    stack,
  });
}
