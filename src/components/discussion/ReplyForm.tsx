"use client";

import Link from "next/link";
import { useActionState } from "react";

import { addReply } from "@/server/actions/discussions";
import { useI18n } from "@/lib/i18n/provider";

type ActionState = { ok: true } | { ok: false; error: string } | null;

/** Reply form (COMM-02) — same auth UX as NewThreadForm. */
export function ReplyForm({ threadId, signedIn }: { threadId: string; signedIn: boolean }) {
  const [state, formAction, pending] = useActionState<ActionState, FormData>(
    async (_prev: ActionState, formData: FormData) => {
      return addReply(threadId, String(formData.get("body") ?? ""));
    },
    null,
  );
  const { d } = useI18n();

  if (!signedIn) {
    return (
      <p className="rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-3 text-sm text-zinc-400">
        <Link href="/login" className="text-emerald-400 underline underline-offset-2 hover:text-emerald-300">
          {d.discussion.signIn}
        </Link>{" "}
        {d.discussion.signInToReply}
      </p>
    );
  }

  return (
    <form action={formAction} className="flex flex-col gap-3">
      <textarea
        name="body"
        required
        maxLength={4000}
        rows={3}
        placeholder={d.discussion.replyPlaceholder}
        aria-label={d.discussion.replyFieldAria}
        className="rounded-lg border border-zinc-700 bg-zinc-900 px-3 py-2 text-sm text-zinc-100 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-400"
      />
      {state && !state.ok && (
        <p role="alert" className="text-sm text-rose-400">
          {state.error}
        </p>
      )}
      <button
        type="submit"
        disabled={pending}
        className="self-start rounded-lg bg-emerald-500 px-4 py-2 text-sm font-semibold text-zinc-950 hover:bg-emerald-400 shadow-sm shadow-emerald-500/20 disabled:opacity-60"
      >
        {pending ? d.discussion.posting : d.discussion.postReply}
      </button>
    </form>
  );
}
