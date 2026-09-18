"use client";

import { useState } from "react";

import type { HintLevel } from "@/lib/mentor/types";
import { useI18n } from "@/lib/i18n/provider";

interface MentorPanelProps {
  mentorAvailable: boolean;
  signedIn: boolean;
  testHints: string[];
  challengeId: string;
  challengeTitle: string;
  prompt: string;
  /** The current failed test, when the latest verdict has one. */
  failedTest: { name: string; message: string } | null;
}

interface MentorState {
  text: string;
  refused: boolean;
}

/**
 * Mentor UI (AI-01/02/04): graduated hint button (level 1→3) and
 * "explain my error" wired to the latest failing test. All requests go
 * through the server action (auth, quota, refusal filter live there).
 * Renders NOTHING when no provider is configured beyond content hints —
 * actually NullMentor still serves hints, so the panel shows hints but no
 * AI branding; the platform stays fully functional either way.
 */
export function MentorPanel(props: MentorPanelProps) {
  const { mentorAvailable, signedIn, failedTest } = props;
  const { d, t, locale } = useI18n();
  const [level, setLevel] = useState<HintLevel | null>(null);
  const [hint, setHint] = useState<MentorState | null>(null);
  const [explanation, setExplanation] = useState<MentorState | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  if (!mentorAvailable && !signedIn) {
    return null;
  }

  const context = {
    challengeId: props.challengeId,
    challengeTitle: props.challengeTitle,
    prompt: props.prompt,
    testHints: props.testHints,
    locale,
  };

  async function nextHint() {
    setPending(true);
    setError(null);
    try {
      const { requestHint } = await import("@/server/actions/mentor");
      const next = ((level ?? 0) + 1) as HintLevel;
      const result = await requestHint(context, next);
      if (result.ok) {
        setLevel(next);
        setHint({ text: result.text, refused: result.refused });
      } else {
        setError(result.error);
      }
    } finally {
      setPending(false);
    }
  }

  async function explain() {
    if (!failedTest) return;
    setPending(true);
    setError(null);
    try {
      const { explainError } = await import("@/server/actions/mentor");
      const result = await explainError(context, failedTest.name, failedTest.message);
      if (result.ok) {
        setExplanation({ text: result.text, refused: result.refused });
      } else {
        setError(result.error);
      }
    } finally {
      setPending(false);
    }
  }

  return (
    <section
      aria-label={d.mentor.aria}
      className="conductor-window rounded-xl flex flex-col gap-3.5 border border-white/[0.1] bg-[#0c101b] p-4 shadow-xl"
    >
      <div className="flex items-center justify-between border-b border-white/[0.08] pb-2.5">
        <div className="flex items-center gap-2.5">
          <div className="relative flex h-7 w-7 items-center justify-center rounded-lg bg-[#111726] border border-emerald-500/40 text-emerald-400 font-mono font-bold text-xs shadow-[0_0_10px_rgba(34,197,94,0.3)]">
            <span className="relative z-10">AI</span>
            {pending && <span className="beacon-pulse" />}
          </div>
          <div>
            <h3 className="text-xs font-semibold text-zinc-100">{d.mentor.title}</h3>
            <p className="text-[10px] font-mono text-emerald-400/80">{d.mentor.subtitle}</p>
          </div>
        </div>
        <span className="badge-pixel badge-pixel-level text-[10px]">{d.mentor.agentBadge}</span>
      </div>

      <div className="flex flex-wrap items-center gap-2 pt-1">
        <button
          type="button"
          onClick={nextHint}
          disabled={pending || level === 3 || !signedIn}
          className="btn-conductor-primary px-3.5 py-1.5 text-xs font-bold disabled:opacity-50 min-h-9"
        >
          {level === null
            ? d.mentor.getHint
            : level === 3
              ? d.mentor.allHints
              : t(d.mentor.anotherHint, { level })}
        </button>
        {failedTest && (
          <button
            type="button"
            onClick={explain}
            disabled={pending || !signedIn}
            className="btn-conductor-secondary px-3.5 py-1.5 text-xs font-medium disabled:opacity-50 min-h-9"
          >
            {d.mentor.explainError}
          </button>
        )}
      </div>

      {!signedIn && <p className="text-xs text-zinc-400 font-mono">⚡ {d.mentor.signInToUse}</p>}
      {error && (
        <p role="alert" className="rounded-lg border border-rose-500/30 bg-rose-950/20 p-3 text-xs font-mono text-rose-300">
          {error}
        </p>
      )}
      {hint && (
        <div className="rounded-lg border border-emerald-500/25 bg-[#091220] p-3 text-xs leading-relaxed text-zinc-200 shadow-sm" aria-live="polite">
          <div className="text-[10px] font-mono text-emerald-400 font-semibold mb-1">{d.mentor.guidanceLabel}</div>
          <p>{hint.text}</p>
        </div>
      )}
      {explanation && (
        <div className="rounded-lg border border-emerald-500/25 bg-[#091220] p-3 text-xs leading-relaxed text-zinc-200 shadow-sm" aria-live="polite">
          <div className="text-[10px] font-mono text-emerald-400 font-semibold mb-1">{d.mentor.errorAnalysisLabel}</div>
          <p>{explanation.text}</p>
        </div>
      )}
      {hint?.refused && <p className="text-xs text-zinc-400">{d.mentor.refusalNote}</p>}
    </section>
  );
}
