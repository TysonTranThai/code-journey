import type { PerTestResult, Verdict } from "@/lib/execution/types";

/**
 * Verdict display (CHAL-05): every test shows pass/fail WITH its
 * educational message on failure — never a bare boolean. Distinct states
 * for pending, timeout, and error.
 */

const VERDICT_STYLES: Record<Verdict, { label: string; className: string }> = {
  passed: {
    label: "All tests passed 🎉",
    className: "border-emerald-700 bg-emerald-950/60 text-emerald-300",
  },
  failed: {
    label: "Some tests failed",
    className: "border-rose-800 bg-rose-950/60 text-rose-300",
  },
  timeout: {
    label: "Your code took too long",
    className: "border-amber-700 bg-amber-950/60 text-amber-300",
  },
  error: {
    label: "Something went wrong running your code",
    className: "border-zinc-700 bg-zinc-900 text-zinc-300",
  },
};

export type RunState =
  | { phase: "idle" }
  | { phase: "running" }
  | {
      phase: "done";
      verdict: Verdict;
      perTestResults: PerTestResult[];
      runtimeMs: number | null;
      output: string;
    };

export function VerdictPanel({ state }: { state: RunState }) {
  if (state.phase === "idle") {
    return <p className="text-sm text-zinc-400">Run your code to see test results here.</p>;
  }

  if (state.phase === "running") {
    return (
      <p className="flex items-center gap-2 text-sm text-zinc-400" role="status" aria-live="polite">
        <span
          className="inline-block h-3 w-3 animate-spin rounded-full border-2 border-zinc-600 border-t-transparent motion-reduce:animate-none"
          aria-hidden="true"
        />
        Running your code in the sandbox…
      </p>
    );
  }

  const style = VERDICT_STYLES[state.verdict];

  return (
    <div
      className={`flex flex-col gap-3 rounded-lg border px-4 py-3 ${style.className}`}
      role="status"
      aria-live="polite"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="font-medium">{style.label}</span>
        {state.runtimeMs !== null && (
          <span className="text-xs opacity-75">{state.runtimeMs} ms</span>
        )}
      </div>

      {state.verdict === "timeout" && (
        <p className="text-sm">
          Check for infinite loops or operations that never complete, then run again.
        </p>
      )}

      {state.verdict === "error" && (
        <pre className="max-h-40 overflow-auto whitespace-pre-wrap text-xs text-zinc-400">
          {state.output}
        </pre>
      )}

      {state.perTestResults.length > 0 && (
        <ul className="flex flex-col gap-2">
          {state.perTestResults.map((result) => (
            <li key={result.name} className="flex flex-col gap-1">
              <span className="flex items-center gap-2 text-sm">
                <span aria-hidden="true">{result.passed ? "✅" : "❌"}</span>
                <span className={result.passed ? "text-emerald-200" : "text-rose-200"}>
                  {result.name}
                </span>
              </span>
              {!result.passed && result.message && (
                <span className="ml-6 text-xs text-zinc-300">{result.message}</span>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
