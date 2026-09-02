"use client";

import { useState } from "react";

import type { HintLevel } from "@/lib/mentor/types";

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
      aria-label="Mentor"
      className="flex flex-col gap-3 rounded-lg border border-indigo-800/60 bg-indigo-950/30 px-4 py-3"
    >
      <h3 className="text-sm font-semibold text-indigo-200">Stuck? Ask the mentor</h3>

      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          onClick={nextHint}
          disabled={pending || level === 3 || !signedIn}
          className="rounded-lg border border-indigo-500/60 px-3 py-1.5 text-xs font-medium text-indigo-200 hover:bg-indigo-900/50 disabled:cursor-not-allowed disabled:opacity-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-indigo-400"
        >
          {level === null
            ? "Get a hint"
            : level === 3
              ? "That's all the hints"
              : `Another hint (${level}/3)`}
        </button>
        {failedTest && (
          <button
            type="button"
            onClick={explain}
            disabled={pending || !signedIn}
            className="rounded-lg border border-indigo-500/60 px-3 py-1.5 text-xs font-medium text-indigo-200 hover:bg-indigo-900/50 disabled:cursor-not-allowed disabled:opacity-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-indigo-400"
          >
            Explain my error
          </button>
        )}
      </div>

      {!signedIn && <p className="text-xs text-zinc-400">Sign in to use the mentor.</p>}
      {error && (
        <p role="alert" className="text-xs text-amber-300">
          {error}
        </p>
      )}
      {hint && (
        <p className="text-sm leading-relaxed text-zinc-200" aria-live="polite">
          {hint.text}
        </p>
      )}
      {explanation && (
        <p className="text-sm leading-relaxed text-zinc-200" aria-live="polite">
          {explanation.text}
        </p>
      )}
      {hint?.refused && (
        <p className="text-xs text-zinc-400">
          (The mentor is designed to guide you, not finish the challenge for you.)
        </p>
      )}
    </section>
  );
}
