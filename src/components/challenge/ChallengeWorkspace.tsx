"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { useSession } from "next-auth/react";

import type { PerTestResult, Verdict } from "@/lib/execution/types";
import { useDraft } from "@/lib/challenges/use-draft";
import { useIsDesktop } from "@/lib/hooks/use-is-desktop";
import { useIsWide } from "@/lib/hooks/use-is-wide";
import { useI18n } from "@/lib/i18n/provider";
import { MentorPanel } from "./MentorPanel";
import { CodeEditor } from "./CodeEditor";
import { LiveConsole } from "./LiveConsole";
import { LivePreview, looksLikeMarkup } from "./LivePreview";
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
 *  - Output pane is a LIVE display: HTML/CSS render as they type (sandboxed
 *    iframe); JS runs live in a sandboxed worker console (LiveConsole).
 *  - "Submit" posts to /api/challenges/run (auth required, DECIDED 07-02),
 *    polls the verdict endpoint, shows per-test educational results (CHAL-05).
 *    Auto-check: signed-in learners' edits re-submit after a short debounce
 *    so progress records hands-free — but SILENTLY (learner request
 *    2026-09-06): the results panel, console output, and errors render only
 *    for an explicit Submit press; auto-checks never touch visible state.
 *  - code drafts persist in localStorage per challenge (CHAL-06)
 */

/**
 * Polling: 1s interval, capped at ~20s, then a friendly retry message.
 */

/** Pause between auto-checks while the learner types. */
const AUTO_CHECK_DEBOUNCE_MS = 1500;

/** Difficulty label keys (mirrors the schema's difficulty enum). */
type DifficultyKey = "beginner" | "intermediate" | "advanced";
export function ChallengeWorkspace({
  challengeId,
  title,
  prompt,
  difficulty,
  boilerplate,
  language = "javascript",
  lessonTitle,
  lessonHref,
  location,
  practiceId,
  mentorAvailable,
  signedIn,
  testHints,
  testNames,
}: {
  challengeId: string;
  title: string;
  prompt: string;
  difficulty: string;
  boilerplate: string;
  /** Editor highlighting language (Python track). Default "javascript". */
  language?: string;
  lessonTitle: string;
  lessonHref: string;
  location: {
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
  };
  /** Present for practice-set challenges; the run API prefers it over lessonId. */
  practiceId?: string;
  mentorAvailable: boolean;
  /** Optional (07-08): when omitted, derived client-side from the session. */
  signedIn?: boolean;
  testHints: string[];
  /** Locale-correct test names (same order as testHints) for verdict display. */
  testNames: string[];
}) {
  const { code, setCode, clearDraft, hasDraft } = useDraft(challengeId, boilerplate);
  const { status: sessionStatus } = useSession();
  // 07-08: pages render statically, so the session flag (mentor panel only)
  // hydrates client-side. Never a trust boundary — the run API enforces auth.
  const resolvedSignedIn = signedIn ?? sessionStatus === "authenticated";
  const [runState, setRunState] = useState<RunState>({ phase: "idle" });
  const [error, setError] = useState<string | null>(null);
  /** Latest submission currently being polled (dedupe for auto-check). */
  const latestSubmission = useRef<string | null>(null);
  /** True while a manual Submit's check is in flight (auto-checks yield to it). */
  const manualInFlightRef = useRef(false);
  /** Code captured at the last submission (manual or auto) — dedupes auto-checks. */
  const submittedRef = useRef(code);
  /** Mirror of the visible run phase; the auto timer reads it without re-subscribing. */
  const runPhaseRef = useRef<RunState["phase"]>("idle");
  const [activeTab, setActiveTab] = useState("instructions");
  const isDesktop = useIsDesktop();
  const isWide = useIsWide();
  const pollTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const { d, t } = useI18n();

  const stopPolling = useCallback(() => {
    if (pollTimer.current) {
      clearTimeout(pollTimer.current);
      pollTimer.current = null;
    }
  }, []);

  useEffect(() => stopPolling, [stopPolling]); // cleanup on unmount

  // Polling loop lives behind a ref so the recursion (202 → poll again)
  // doesn't self-reference the callback during declaration.
  const pollRef = useRef<(submissionId: string, attempts: number, auto?: boolean) => void>(
    () => undefined,
  );

  const startPolling = useCallback(
    (submissionId: string, attempts: number, auto = false) => {
      stopPolling();
      if (attempts > 20) {
        if (!auto) {
          manualInFlightRef.current = false;
          setRunState({ phase: "idle" });
          setError(t(d.workspace.errSlow));
        }
        return;
      }
      pollTimer.current = setTimeout(async () => {
        try {
          const res = await fetch(`/api/challenges/run/${submissionId}`, {
            cache: "no-store",
          });
          if (res.status === 202) {
            pollRef.current(submissionId, attempts + 1, auto);
            return;
          }
          if (!res.ok) {
            if (!auto) {
              manualInFlightRef.current = false;
              setRunState({ phase: "idle" });
              setError(t(d.workspace.errFetch));
            }
            return;
          }
          const data = (await res.json()) as {
            verdict: Verdict;
            perTestResults: PerTestResult[];
            runtimeMs: number | null;
            output: string;
          };
          // Drop stale verdicts: a newer submission may have superseded this
          // poll (racing submissions while typing).
          if (submissionId !== latestSubmission.current) {
            if (!auto) manualInFlightRef.current = false;
            return;
          }
          // Auto-checks are silent (learner request 2026-09-06): they record
          // progress but never render results — the panel is Submit-only.
          if (auto) return;
          manualInFlightRef.current = false;
          setRunState({
            phase: "done",
            verdict: data.verdict,
            perTestResults: data.perTestResults,
            runtimeMs: data.runtimeMs,
            output: data.output,
          });
        } catch {
          if (!auto) {
            manualInFlightRef.current = false;
            setRunState({ phase: "idle" });
            setError(t(d.workspace.errNetwork));
          }
        }
      }, 1000);
    },
    [stopPolling, d, t],
  );
  // Assign the polling ref in an effect (refs must not be written during render).
  useEffect(() => {
    pollRef.current = startPolling;
  }, [startPolling]);

  const run = useCallback(
    async (options?: { auto?: boolean }) => {
      const auto = options?.auto === true;
      // A manual Submit always wins over an in-flight auto-check, and
      // auto-checks are silent (learner request 2026-09-06): they never
      // touch the visible panel or error state. (Guard before recording the
      // code, so a yielded auto-check re-fires for the newer code later.)
      if (auto && (manualInFlightRef.current || runPhaseRef.current === "running")) return;
      // Record what was just submitted so the auto-check effect doesn't
      // re-fire for code a submission is already grading.
      submittedRef.current = code;
      if (!auto) {
        manualInFlightRef.current = true;
        setError(null);
        setRunState({ phase: "running" });
      }
      try {
        const res = await fetch("/api/challenges/run", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code,
            challengeId,
            ...location,
            ...(practiceId ? { practiceId } : {}),
          }),
        });
        if (res.status === 202) {
          const { submissionId } = (await res.json()) as { submissionId: string };
          // A manual Submit started while this auto-check was posting:
          // abandon the auto submission so it can't supersede the panel's poll.
          if (auto && manualInFlightRef.current) return;
          latestSubmission.current = submissionId;
          startPolling(submissionId, 0, auto);
          return;
        }
        if (!auto) setRunState({ phase: "idle" });
        if (res.status === 401) {
          // DECIDED (07-02): code execution requires a session.
          if (!auto) {
            manualInFlightRef.current = false;
            setError("log_in_to_run");
          }
          return;
        }
        if (res.status === 429 && auto) return; // silently back off while typing
        const data = (await res.json().catch(() => null)) as { error?: string } | null;
        manualInFlightRef.current = false;
        setError(data?.error ?? t(d.workspace.errStart));
      } catch {
        if (!auto) {
          manualInFlightRef.current = false;
          setRunState({ phase: "idle" });
          setError(t(d.workspace.errNetworkStart));
        }
      }
    },
    [code, challengeId, location, practiceId, startPolling, d, t],
  );

  // Auto-check (signed-in): re-submit after the learner stops typing so
  // progress records hands-free — silently (see run()); a manual Submit in
  // flight always wins.
  const autoTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const canAutoCheck = resolvedSignedIn;
  useEffect(() => {
    runPhaseRef.current = runState.phase;
  }, [runState]);
  useEffect(() => {
    if (!canAutoCheck) return;
    if (code === submittedRef.current) return;
    if (autoTimer.current) clearTimeout(autoTimer.current);
    autoTimer.current = setTimeout(() => {
      void run({ auto: true });
    }, AUTO_CHECK_DEBOUNCE_MS);
    return () => {
      if (autoTimer.current) clearTimeout(autoTimer.current);
    };
  }, [code, canAutoCheck, run]);

  // Keyboard shortcut: Cmd+Enter / Ctrl+Enter triggers run
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "Enter") {
        e.preventDefault();
        void run();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [run]);

  // The latest failing test (if the verdict is done + failed) feeds "explain my error".
  const failedTest =
    runState.phase === "done" && runState.verdict === "failed"
      ? (runState.perTestResults.find((r) => !r.passed) ?? null)
      : null;

  const instructions = (
    <div className="conductor-window rounded-xl flex flex-col gap-4 p-5 text-sm leading-relaxed text-zinc-300 shadow-xl bg-[#0c101b]">
      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-white/[0.08] pb-3">
        <span className="badge-pixel badge-pixel-quest">{d.workspace.challengeBadge}</span>
        <div className="flex items-center gap-2">
          <span className="badge-pixel badge-pixel-level">
            {t(d.workspace.difficulty, {
              level: d.difficulty[difficulty as DifficultyKey] ?? difficulty,
            })}
          </span>
          <span className="badge-pixel badge-pixel-xp">+25 XP</span>
        </div>
      </div>
      <PromptText text={prompt} />
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
        <p className="font-mono text-xs text-zinc-400">
          {d.workspace.draftRestored}{" "}
          <button
            type="button"
            onClick={clearDraft}
            className="text-emerald-400 underline underline-offset-2 hover:text-emerald-300 font-semibold"
          >
            {d.workspace.resetToStarter}
          </button>
        </p>
      )}
    </div>
  );

  const editor = (
    <div className="conductor-window overflow-hidden rounded-xl flex min-h-[18rem] flex-1 flex-col border border-emerald-500/20 shadow-[0_20px_50px_-15px_rgba(0,0,0,0.8),0_0_30px_rgba(34,197,94,0.12)] bg-[#090d16]">
      <div className="flex items-center justify-between border-b border-white/[0.08] bg-[#070b14] px-4 py-2.5">
        <div className="flex items-center gap-2.5">
          <span className="h-2.5 w-2.5 rounded-full bg-rose-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/80 inline-block" aria-hidden="true" />
          <span className="ml-2 font-mono text-xs font-semibold text-zinc-300 flex items-center gap-1.5">
            <span className="text-emerald-400">🌿</span>
            <span>{title}</span>
          </span>
        </div>
        <span className="badge-pixel badge-pixel-quest text-[10px]">
          {language.toUpperCase()}
        </span>
      </div>
      <div className="flex-1 p-2 bg-[#05070e]">
        <CodeEditor
          value={code}
          onChange={setCode}
          onRun={() => void run()}
          language={language}
          ariaLabel={t(d.workspace.editorAria, { title })}
        />
      </div>
    </div>
  );

  // Markup challenges (HTML/CSS in <style>) get a live sandboxed preview:
  // the learner should SEE the page they are building, not just test verdicts.
  // JavaScript challenges get the live worker console (in-browser evaluation).
  const showPreview = looksLikeMarkup(code);

  const output = (
    <div className="flex flex-col gap-3">
      {showPreview ? (
        <LivePreview code={code} />
      ) : (
        <LiveConsole
          code={code}
          boilerplate={boilerplate}
          language={language}
          serverOutput={runState.phase === "done" ? runState.output : undefined}
          isServerRunning={runState.phase === "running"}
        />
      )}
      <VerdictPanel state={runState} testNames={testNames} language={language} />
      {error === "log_in_to_run" ? (
        <p className="rounded-xl border border-rose-500/40 bg-rose-950/40 p-4 text-sm text-rose-300 shadow-lg font-mono">
          {d.workspace.logInToRunBefore}
          <Link href="/login" className="font-semibold underline underline-offset-2 text-white ml-1">
            {d.workspace.logIn}
          </Link>
          {d.workspace.logInToRunAfter}
        </p>
      ) : error ? (
        <p className="rounded-xl border border-rose-500/40 bg-rose-950/40 p-4 text-sm text-rose-300 shadow-lg font-mono">
          {error}
        </p>
      ) : null}
    </div>
  );

  const runButton = (
    <button
      type="button"
      onClick={() => void run()}
      disabled={runState.phase === "running"}
      className="btn-conductor-primary px-7 py-3 text-sm font-bold min-h-11 disabled:cursor-not-allowed disabled:opacity-60 shadow-[0_0_20px_rgba(34,197,94,0.4)] flex items-center justify-center gap-2"
    >
      <span className="font-mono" aria-hidden="true">{runState.phase === "running" ? "⏳" : "▶"}</span>
      <span>{runState.phase === "running" ? d.workspace.checking : d.workspace.submit}</span>
      <kbd className="hidden sm:inline-block ml-1 rounded bg-black/40 px-1.5 py-0.5 font-mono text-[10px] text-emerald-300/80 border border-emerald-500/20">
        ⌘↵
      </kbd>
    </button>
  );

  if (isWide) {
    // Wide desktop (≥1440px): three panes — instructions | code | output —
    // so the live preview and results are visible WHILE coding. Single-branch
    // render (07-06): one Monaco instance.
    return (
      <section aria-label={t(d.workspace.challengeAria, { title })} className="flex flex-col gap-4">
        <div className="grid gap-5 xl:grid-cols-[22rem_1fr_26rem]">
          <div className="flex flex-col gap-4">{instructions}</div>
          <div className="flex min-h-[30rem] flex-col gap-3">
            {editor}
            {runButton}
          </div>
          <div className="flex flex-col gap-3">{output}</div>
        </div>
        <p className="font-mono text-xs text-zinc-400">
          {d.workspace.backToLesson}{" "}
          <Link href={lessonHref} className="text-emerald-400 font-semibold underline underline-offset-2 hover:text-white">
            {lessonTitle}
          </Link>
        </p>
      </section>
    );
  }

  if (isDesktop) {
    // Desktop (≥1024px): side-by-side. A single branch renders — no hidden
    // duplicate editor (07-06).
    return (
      <section aria-label={t(d.workspace.challengeAria, { title })} className="flex flex-col gap-4">
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
        <p className="font-mono text-xs text-zinc-400">
          {d.workspace.backToLesson}{" "}
          <Link href={lessonHref} className="text-emerald-400 font-semibold underline underline-offset-2 hover:text-white">
            {lessonTitle}
          </Link>
        </p>
      </section>
    );
  }

  return (
    <section aria-label={t(d.workspace.challengeAria, { title })} className="flex flex-col gap-4">
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
              label: d.workspace.tabInstructions,
              content: instructions,
            },
            { id: "code", label: d.workspace.tabCode, content: editor },
            { id: "output", label: d.workspace.tabOutput, content: output },
          ]}
        />
        <div
          aria-label={d.workspace.actionsAria}
          className="sticky bottom-0 mt-2 flex shrink-0 items-center gap-3 rounded-xl border border-white/10 bg-[#080c14]/95 px-3 py-3 backdrop-blur-xl shadow-2xl"
        >
          {runButton}
          <div role="status" aria-live="polite" className="min-w-0 flex-1 text-sm text-zinc-400">
            {runState.phase === "running" ? (
              d.workspace.checking
            ) : runState.phase === "done" ? (
              <span className="inline-flex items-center gap-3">
                <span
                  className={runState.verdict === "passed" ? "text-emerald-400 font-semibold" : "text-rose-400 font-semibold"}
                >
                  {verdictLabel(runState.verdict, d)}
                </span>
                <button
                  type="button"
                  onClick={() => setActiveTab("output")}
                  className="underline underline-offset-2 hover:text-zinc-300 font-mono text-xs"
                >
                  {d.workspace.viewResults}
                </button>
              </span>
            ) : error ? (
              <span className="text-rose-400">{d.workspace.checkFailed}</span>
            ) : (
              <span className="hidden sm:inline">{d.workspace.pressSubmit}</span>
            )}
          </div>
        </div>
      </div>

      <p className="text-xs text-zinc-400 font-mono">
        {d.workspace.backToLesson}{" "}
        <Link href={lessonHref} className="text-emerald-400 font-semibold underline underline-offset-2 hover:text-white">
          {lessonTitle}
        </Link>
      </p>
    </section>
  );
}
