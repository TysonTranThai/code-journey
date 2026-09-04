"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { useSession } from "next-auth/react";

import type { PerTestResult, Verdict } from "@/lib/execution/types";
import { useDraft } from "@/lib/challenges/use-draft";
import { useIsDesktop } from "@/lib/hooks/use-is-desktop";
import { MentorPanel } from "./MentorPanel";
import { CodeEditor } from "./CodeEditor";
import { MobileTabs } from "./MobileTabs";
import { VerdictPanel, verdictLabel, type RunState } from "./VerdictPanel";

/**
 * Renders an authored prompt with `inline code` spans (07-09). Text is split
 * on backtick runs; React escapes everything (no raw HTML), so authored
 * angle brackets/ampersands stay literal and safe.
 */
function PromptText({ text }: { text: string }) {
  const parts = text.split(/`([^`]+)`/);
  return (
    <p className="whitespace-pre-wrap">
      {parts.map((part, i) =>
        i % 2 === 1 ? (
          <code
            key={i}
            className="rounded bg-zinc-800 px-1.5 py-0.5 font-mono text-[0.85em] text-zinc-200"
          >
            {part}
          </code>
        ) : (
          part
        ),
      )}
    </p>
  );
}

/**
 * Challenge workspace (03-CONTEXT D-10):
 *  - desktop: side-by-side editor | instructions+output
 *  - tablet/mobile: Instructions / Code / Output tabs (accessible tablist)
 *  - Run posts to /api/challenges/run (auth required, DECIDED 07-02), polls
 *    the verdict endpoint, shows per-test educational results (CHAL-05)
 *  - code drafts persist in localStorage per challenge (CHAL-06)
 *
 * Polling: 1s interval, capped at ~20s, then a friendly retry message.
 */
export function ChallengeWorkspace({
  challengeId,
  title,
  prompt,
  difficulty,
  boilerplate,
  lessonTitle,
  lessonHref,
  location,
  mentorAvailable,
  signedIn,
  testHints,
}: {
  challengeId: string;
  title: string;
  prompt: string;
  difficulty: string;
  boilerplate: string;
  lessonTitle: string;
  lessonHref: string;
  location: {
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
  };
  mentorAvailable: boolean;
  /** Optional (07-08): when omitted, derived client-side from the session. */
  signedIn?: boolean;
  testHints: string[];
}) {
  const { code, setCode, clearDraft, hasDraft } = useDraft(challengeId, boilerplate);
  const { status: sessionStatus } = useSession();
  // 07-08: pages render statically, so the session flag (mentor panel only)
  // hydrates client-side. Never a trust boundary — the run API enforces auth.
  const resolvedSignedIn = signedIn ?? sessionStatus === "authenticated";
  const [runState, setRunState] = useState<RunState>({ phase: "idle" });
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("instructions");
  const isDesktop = useIsDesktop();
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stopPolling = useCallback(() => {
    if (pollTimer.current) {
      clearTimeout(pollTimer.current);
      pollTimer.current = null;
    }
  }, []);

  useEffect(() => stopPolling, [stopPolling]); // cleanup on unmount

  // Polling loop lives behind a ref so the recursion (202 → poll again)
  // doesn't self-reference the callback during declaration.
  const pollRef = useRef<(submissionId: string, attempts: number) => void>(() => undefined);

  const startPolling = useCallback(
    (submissionId: string, attempts: number) => {
      stopPolling();
      if (attempts > 20) {
        setRunState({ phase: "idle" });
        setError("The sandbox is taking longer than expected. Try again in a moment.");
        return;
      }
      pollTimer.current = setTimeout(async () => {
        try {
          const res = await fetch(`/api/challenges/run/${submissionId}`, {
            cache: "no-store",
          });
          if (res.status === 202) {
            pollRef.current(submissionId, attempts + 1);
            return;
          }
          if (!res.ok) {
            setRunState({ phase: "idle" });
            setError("Could not fetch your results. Try running again.");
            return;
          }
          const data = (await res.json()) as {
            verdict: Verdict;
            perTestResults: PerTestResult[];
            runtimeMs: number | null;
            output: string;
          };
          setRunState({
            phase: "done",
            verdict: data.verdict,
            perTestResults: data.perTestResults,
            runtimeMs: data.runtimeMs,
            output: data.output,
          });
        } catch {
          setRunState({ phase: "idle" });
          setError("Network error while fetching results. Try again.");
        }
      }, 1000);
    },
    [stopPolling],
  );
  // Assign the polling ref in an effect (refs must not be written during render).
  useEffect(() => {
    pollRef.current = startPolling;
  }, [startPolling]);

  const run = useCallback(async () => {
    setError(null);
    setRunState({ phase: "running" });
    try {
      const res = await fetch("/api/challenges/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, challengeId, ...location }),
      });
      if (res.status === 202) {
        const { submissionId } = (await res.json()) as { submissionId: string };
        startPolling(submissionId, 0);
        return;
      }
      setRunState({ phase: "idle" });
      if (res.status === 401) {
        // DECIDED (07-02): code execution requires a session.
        setError("log_in_to_run");
        return;
      }
      const data = (await res.json().catch(() => null)) as { error?: string } | null;
      setError(data?.error ?? "Could not start the run. Try again.");
    } catch {
      setRunState({ phase: "idle" });
      setError("Network error — could not start the run.");
    }
  }, [code, challengeId, location, startPolling]);

  // The latest failing test (if the verdict is done + failed) feeds "explain my error".
  const failedTest =
    runState.phase === "done" && runState.verdict === "failed"
      ? (runState.perTestResults.find((r) => !r.passed) ?? null)
      : null;

  const instructions = (
    <div className="flex flex-col gap-4 text-sm leading-relaxed text-zinc-300">
      <PromptText text={prompt} />
      <p className="text-xs uppercase tracking-wide text-zinc-400">Difficulty: {difficulty}</p>
      <MentorPanel
        mentorAvailable={mentorAvailable}
        signedIn={resolvedSignedIn}
        testHints={testHints}
        challengeId={challengeId}
        challengeTitle={title}
        prompt={prompt}
        failedTest={failedTest}
      />
      {hasDraft && (
        <p className="text-xs text-zinc-400">
          Draft restored from your last session.{" "}
          <button
            type="button"
            onClick={clearDraft}
            className="underline underline-offset-2 hover:text-zinc-300"
          >
            Reset to starter code
          </button>
        </p>
      )}
    </div>
  );

  const editor = (
    <div className="flex min-h-[18rem] flex-1 flex-col gap-2">
      <CodeEditor value={code} onChange={setCode} ariaLabel={`Code editor for ${title}`} />
    </div>
  );

  const output = (
    <div className="flex flex-col gap-3">
      <VerdictPanel state={runState} />
      {error === "log_in_to_run" ? (
        <p className="rounded-lg border border-rose-800 bg-rose-950/60 px-4 py-3 text-sm text-rose-300">
          You need to be logged in to run code.{" "}
          <Link href="/login" className="font-semibold underline underline-offset-2">
            Log in
          </Link>{" "}
          to submit and check your solution.
        </p>
      ) : error ? (
        <p className="rounded-lg border border-rose-800 bg-rose-950/60 px-4 py-3 text-sm text-rose-300">
          {error}
        </p>
      ) : null}
    </div>
  );

  const runButton = (
    <button
      type="button"
      onClick={run}
      disabled={runState.phase === "running"}
      className="rounded-lg bg-sky-500 px-5 py-2 text-sm font-semibold text-zinc-950 transition-colors hover:bg-sky-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400 disabled:cursor-not-allowed disabled:opacity-60"
    >
      {runState.phase === "running" ? "Running…" : "Run code"}
    </button>
  );

  if (isDesktop) {
    // Desktop (≥1024px): side-by-side. A single branch renders — no hidden
    // duplicate editor (07-06).
    return (
      <section aria-label={`Challenge: ${title}`} className="flex flex-col gap-4">
        <div className="grid gap-6 lg:grid-cols-2">
          <div className="flex flex-col gap-4">
            {instructions}
            {runButton}
          </div>
          <div className="flex min-h-[28rem] flex-col gap-4">
            {editor}
            {output}
          </div>
        </div>
        <p className="text-xs text-zinc-400">
          Back to lesson:{" "}
          <Link href={lessonHref} className="underline underline-offset-2 hover:text-zinc-300">
            {lessonTitle}
          </Link>
        </p>
      </section>
    );
  }

  return (
    <section aria-label={`Challenge: ${title}`} className="flex flex-col gap-4">
      {/* Tablet/mobile: tabs (Instructions / Code / Output) + sticky action bar.
          07-06: single-branch render (no hidden duplicate editor), definite
          height so lazy-mounted Monaco resolves non-zero dimensions; 07-07:
          persistent bottom action bar keeps Run reachable from every tab. */}
      <div className="flex h-[70vh] min-h-[28rem] flex-col">
        <MobileTabs
          active={activeTab}
          onChange={setActiveTab}
          tabs={[
            {
              id: "instructions",
              label: "Instructions",
              content: instructions,
            },
            { id: "code", label: "Code", content: editor },
            { id: "output", label: "Output", content: output },
          ]}
        />
        <div
          aria-label="Challenge actions"
          className="sticky bottom-0 mt-2 flex shrink-0 items-center gap-3 border-t border-zinc-800 bg-zinc-950/95 px-1 py-3"
        >
          {runButton}
          <div role="status" aria-live="polite" className="min-w-0 flex-1 text-sm text-zinc-400">
            {runState.phase === "running" ? (
              "Running…"
            ) : runState.phase === "done" ? (
              <span className="inline-flex items-center gap-3">
                <span
                  className={runState.verdict === "passed" ? "text-emerald-400" : "text-rose-400"}
                >
                  {verdictLabel(runState.verdict)}
                </span>
                <button
                  type="button"
                  onClick={() => setActiveTab("output")}
                  className="underline underline-offset-2 hover:text-zinc-300"
                >
                  View results
                </button>
              </span>
            ) : error ? (
              <span className="text-rose-400">Run failed — see details</span>
            ) : (
              <span className="hidden sm:inline">Run your code to check each test.</span>
            )}
          </div>
        </div>
      </div>

      <p className="text-xs text-zinc-400">
        Back to lesson:{" "}
        <Link href={lessonHref} className="underline underline-offset-2 hover:text-zinc-300">
          {lessonTitle}
        </Link>
      </p>
    </section>
  );
}
