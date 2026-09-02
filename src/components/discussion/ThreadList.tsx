import Link from "next/link";

import type { ThreadSummary } from "@/lib/discussions/threads";

/** Thread list (COMM-03: public read). Plain links — user content is escaped by React. */
export function ThreadList({ threads, hrefBase }: { threads: ThreadSummary[]; hrefBase: string }) {
  if (threads.length === 0) {
    return (
      <p className="rounded-lg border border-zinc-800 bg-zinc-900/40 px-4 py-3 text-sm text-zinc-500">
        No questions yet — be the first to ask.
      </p>
    );
  }
  return (
    <ul className="flex flex-col gap-2">
      {threads.map((thread) => (
        <li key={thread.id}>
          <Link
            href={`${hrefBase}/${thread.id}`}
            className="flex items-center justify-between gap-3 rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-3 text-sm transition-colors hover:border-sky-500/60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400"
          >
            <span className="flex flex-col">
              <span className="font-medium text-zinc-100">{thread.title}</span>
              <span className="text-xs text-zinc-500">
                by {thread.authorName ?? "a learner"} ·{" "}
                {thread.createdAt.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })}
              </span>
            </span>
            <span className="whitespace-nowrap text-xs text-zinc-400">
              {thread.commentCount} {thread.commentCount === 1 ? "reply" : "replies"}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
