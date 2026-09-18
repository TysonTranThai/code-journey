import Link from "next/link";

import type { ThreadSummary } from "@/lib/discussions/threads";
import { INTL_TAG } from "@/lib/i18n/config";
import { getServerI18n } from "@/lib/i18n/server";

/** Thread list (COMM-03: public read). Plain links — user content is escaped by React. */
export async function ThreadList({
  threads,
  hrefBase,
}: {
  threads: ThreadSummary[];
  hrefBase: string;
}) {
  const { d, locale, tp, t } = await getServerI18n();
  if (threads.length === 0) {
    return (
      <p className="rounded-lg border border-zinc-800 bg-zinc-900/40 px-4 py-3 text-sm text-zinc-400">
        {d.discussion.noThreads}
      </p>
    );
  }
  return (
    <ul className="flex flex-col gap-2">
      {threads.map((thread) => (
        <li key={thread.id}>
          <Link
            href={`${hrefBase}/${thread.id}`}
            className="flex items-center justify-between gap-3 rounded-lg border border-zinc-800 bg-zinc-900/60 px-4 py-3 text-sm transition-colors hover:border-emerald-500/60 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-400"
          >
            <span className="flex flex-col">
              <span className="font-medium text-zinc-100">{thread.title}</span>
              <span className="text-xs text-zinc-400">
                {t(d.discussion.byline, {
                  author: thread.authorName ?? d.discussion.authorFallback,
                })}{" "}
                {thread.createdAt.toLocaleDateString(INTL_TAG[locale], {
                  month: "short",
                  day: "numeric",
                })}
              </span>
            </span>
            <span className="whitespace-nowrap text-xs text-zinc-400">
              {tp(thread.commentCount, d.discussion.replies)}
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
