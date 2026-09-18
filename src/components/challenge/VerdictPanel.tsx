"use client";

import type { PerTestResult, Verdict } from "@/lib/execution/types";
import type { Dictionary } from "@/lib/i18n/dictionaries";
import { useI18n } from "@/lib/i18n/provider";
import { getErrorExplanation } from "@/lib/mentor/error-explainer";
import { ErrorExplanationCard } from "./ErrorExplanationCard";

/**
 * Verdict display (CHAL-05): every test shows pass/fail WITH its
 * educational message on failure — never a bare boolean. Distinct states
 * for pending, timeout, and error.
 */

const VERDICT_STYLES: Record<Verdict, { className: string }> = {
  passed: {
    className: "conductor-window border border-emerald-500/40 bg-[#091510] text-emerald-300 shadow-[0_0_30px_rgba(34,197,94,0.25)]",
  },
  failed: {
    className: "conductor-window border border-rose-500/40 bg-[#160a0f] text-rose-300 shadow-[0_0_30px_rgba(244,63,94,0.2)]",
  },
  timeout: {
    className: "conductor-window border border-amber-500/40 bg-[#161209] text-amber-300 shadow-[0_0_30px_rgba(245,158,11,0.2)]",
  },
  error: {
    className: "conductor-window border border-white/[0.1] bg-[#0c101b] text-zinc-300 shadow-xl",
  },
};

/** Shared with the mobile action bar so its live region can announce the verdict. */
export function verdictLabel(verdict: Verdict, d: Dictionary): string {
  const labels: Record<Verdict, string> = {
    passed: d.verdict.passed,
    failed: d.verdict.failed,
    timeout: d.verdict.timeout,
    error: d.verdict.error,
  };
  return labels[verdict];
}

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

export function VerdictPanel({
  state,
  testNames,
  language,
}: {
  state: RunState;
  /**
   * Authoritative, locale-correct test names from the challenge data
   * (same order as the tests the worker ran). Preferred over the
   * worker's sanitized marker id for display — the id is an execution
   * detail; the learner should read the authored name (e.g. Vietnamese).
   */
  testNames?: string[];
  language?: string;
}) {
  const { d, t } = useI18n();
  const isBackend =
    Boolean(language) &&
    language !== "javascript" &&
    language !== "js" &&
    language !== "html";

  if (state.phase === "idle") {
    const [before, after] = d.verdict.idle.split("{submit}");

    return (
      <section
        aria-label={d.verdict.backendSandboxTitle}
        className="glass-card p-4 rounded-2xl flex flex-col gap-2.5 shadow-xl border border-white/[0.08] bg-[#0c101b]"
      >
        <div className="flex items-center justify-between gap-2 border-b border-white/[0.08] pb-2">
          <div className="flex items-center gap-2">
            <span className="text-sm">🧪</span>
            <h3 className="font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300">
              {d.verdict.backendSandboxTitle}
            </h3>
          </div>
          <span className="badge-pixel badge-pixel-level text-[10px] uppercase font-mono">
            {(language ?? "SANDBOX").toUpperCase()}
          </span>
        </div>
        <p className="text-xs text-zinc-400">
          {before}
          <span className="font-semibold text-emerald-400">{d.workspace.submit}</span>
          {after}
        </p>
        {testNames && testNames.length > 0 && (
          <div className="mt-2 border-t border-white/[0.06] pt-2">
            <p className="text-[11px] font-semibold text-zinc-400 uppercase tracking-wider mb-1.5 font-mono">
              {d.verdict.expectedTests} ({testNames.length}):
            </p>
            <ul className="flex flex-col gap-1 text-[11px] font-mono text-zinc-400">
              {testNames.map((name, i) => (
                <li key={i} className="flex items-center gap-1.5 truncate">
                  <span className="text-zinc-600">○</span>
                  <span className="truncate">{name}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>
    );
  }

  if (state.phase === "running") {
    return (
      <section
        aria-label={d.verdict.backendSandboxTitle}
        className="glass-card p-4 rounded-2xl flex flex-col gap-2.5 shadow-xl border border-white/[0.08] bg-[#0c101b]"
      >
        <div className="flex items-center justify-between gap-2 border-b border-white/[0.08] pb-2">
          <div className="flex items-center gap-2">
            <span className="text-sm">🧪</span>
            <h3 className="font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300">
              {d.verdict.backendSandboxTitle}
            </h3>
          </div>
          <span className="badge-pixel badge-pixel-level text-[10px] uppercase font-mono">
            {(language ?? "SANDBOX").toUpperCase()}
          </span>
        </div>
        <p className="flex items-center gap-2 text-sm text-zinc-300 p-2 font-mono" role="status" aria-live="polite">
          <span
            className="inline-block h-3.5 w-3.5 animate-spin rounded-full border-2 border-emerald-400 border-t-transparent motion-reduce:animate-none"
            aria-hidden="true"
          />
          {d.verdict.running}
        </p>
      </section>
    );
  }

  const style = VERDICT_STYLES[state.verdict];
  const labels: Record<Verdict, string> = {
    passed: d.verdict.passed,
    failed: d.verdict.failed,
    timeout: d.verdict.timeout,
    error: d.verdict.error,
  };

  return (
    <div
      className={`flex flex-col gap-3 rounded-2xl p-5 ${style.className}`}
      role="status"
      aria-live="polite"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2.5">
          <span className="text-base" aria-hidden="true">
            {state.verdict === "passed" ? "✓" : state.verdict === "failed" ? "✕" : "⚠️"}
          </span>
          <span className="font-semibold text-sm">{labels[state.verdict]}</span>
        </div>
        <div className="flex items-center gap-2">
          {state.verdict === "passed" && (
            <span className="badge-pixel badge-pixel-xp text-[10px]">{d.verdict.xpEarned}</span>
          )}
          {state.runtimeMs !== null && (
            <span className="font-mono text-xs opacity-75">{state.runtimeMs} ms</span>
          )}
        </div>
      </div>

      {state.verdict === "timeout" && <p className="text-sm">{d.verdict.timeoutHint}</p>}

      {state.verdict === "error" && (
        <div className="flex flex-col gap-2.5">
          <pre className="max-h-40 overflow-auto whitespace-pre-wrap rounded-xl border border-rose-500/30 bg-[#160a0f] p-3.5 font-mono text-xs text-rose-300">
            {state.output}
          </pre>
          {(() => {
            const explanation = getErrorExplanation(state.output, d);
            return explanation ? <ErrorExplanationCard explanation={explanation} /> : null;
          })()}
        </div>
      )}

      {/* Sandbox console output (console.log etc.) — show whenever there is
          any, not only on errors, so JS challenges give visible feedback. */}
      {state.verdict !== "error" && state.output.trim().length > 0 && (
        <section aria-label={d.verdict.sandboxOutput} className="flex flex-col gap-1">
          <h3 className="text-xs font-semibold uppercase tracking-widest text-zinc-400">
            {d.verdict.consoleOutput}
          </h3>
          <pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded-md border border-zinc-800 bg-zinc-950/70 px-3 py-2 text-xs text-zinc-300">
            {state.output}
          </pre>
        </section>
      )}

      {state.perTestResults.length > 0 && (
        <ul className="flex flex-col gap-2">
          {state.perTestResults.map((result, index) => (
            <li key={result.name} className="flex flex-col gap-1">
              <span className="flex items-center gap-2 text-sm">
                <span aria-hidden="true">{result.passed ? "✅" : "❌"}</span>
                <span className={result.passed ? "text-emerald-200" : "text-rose-200"}>
                  {testNames?.[index] ?? result.name}
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
