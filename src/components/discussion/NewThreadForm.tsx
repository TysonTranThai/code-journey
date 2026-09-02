"use client";

import Link from "next/link";
import { useActionState } from "react";

import { createThread } from "@/server/actions/discussions";

type ActionState = { ok: true; threadId: string } | { ok: false; error: string } | null;

/**
 * New-thread form (COMM-01). Signed-in users post; anonymous users get a
 * sign-in prompt (server still enforces auth — this is UX only).
 */
export function NewThreadForm({ lessonId, signedIn }: { lessonId: string; signedIn: boolean }) {
  const [state, formAction, pending] = useActionState<ActionState, FormData>(
    async (_prev: ActionState, formData: FormData) => {
      return createThread(
        lessonId,
        String(formData.get("title") ?? ""),
        String(formData.get("body") ?? ""),
      );
    },
    null,
  );

  if (!signedIn) {
    return (
      <p className="rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-3 text-sm text-zinc-400">
        <Link href="/login" className="text-sky-400 underline underline-offset-2">
          Sign in
        </Link>{" "}
        to ask a question.
      </p>
    );
  }

  if (state?.ok) {
    return (
      <p className="rounded-lg border border-emerald-700 bg-emerald-950/50 px-4 py-3 text-sm text-emerald-300">
        Thread posted.
      </p>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-3">
      <input
        type="text"
        name="title"
        required
        maxLength={200}
        placeholder="Your question in one line"
        aria-label="Question title"
        className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400"
      />
      <textarea
        name="body"
        required
        maxLength={4000}
        rows={4}
        placeholder="What would you like to ask? Share what you tried, too."
        aria-label="Question details"
        className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400"
      />
      {state && !state.ok && (
        <p role="alert" className="text-sm text-rose-400">
          {state.error}
        </p>
      )}
      <button
        type="submit"
        disabled={pending}
        className="self-start rounded-lg bg-sky-500 px-4 py-2 text-sm font-semibold text-zinc-950 hover:bg-sky-400 disabled:opacity-60"
      >
        {pending ? "Posting…" : "Post question"}
      </button>
    </form>
  );
}
