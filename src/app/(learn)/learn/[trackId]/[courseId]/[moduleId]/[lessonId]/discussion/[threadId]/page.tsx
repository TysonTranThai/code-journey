import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ReplyForm } from "@/components/discussion/ReplyForm";
import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { auth } from "@/lib/auth/config";
import { getLesson, getTracks } from "@/lib/curriculum/loaders";
import { getThread, getThreadLessonId } from "@/lib/discussions/threads";

interface ThreadPageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
    threadId: string;
  }>;
}

export const metadata: Metadata = { title: "Thread" };

/** Thread detail (COMM-02 reply, COMM-03 public read). */
export default async function ThreadPage({ params }: ThreadPageProps) {
  const { trackId, courseId, moduleId, lessonId, threadId } = await params;

  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId);
  } catch {
    notFound();
  }
  const thread = await getThread(threadId);
  if (!thread) notFound();
  // Threads may only be viewed under the lesson they anchor to.
  const threadLessonId = await getThreadLessonId(threadId);
  if (threadLessonId !== lessonId) notFound();
  const track = getTracks().find((t) => t.id === trackId);
  const session = await auth();
  const discussionBase = `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/discussion`;

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: lesson.title, href: `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}` },
          { label: "Discussion", href: discussionBase },
          { label: thread.title },
        ]}
      />

      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">{thread.title}</h1>
        <p className="text-sm text-zinc-400">
          {thread.replies[0]?.authorName ?? thread.authorName ?? "A learner"} ·{" "}
          {thread.createdAt.toLocaleDateString("en-US", { month: "long", day: "numeric" })}
        </p>
      </header>

      <ul className="flex flex-col gap-4" aria-label="Conversation">
        {thread.replies.map((reply, index) => (
          <li
            key={reply.id}
            className={`rounded-xl border px-4 py-3 ${
              index === 0 ? "border-sky-800/60 bg-sky-950/20" : "border-zinc-800 bg-zinc-900/50"
            }`}
          >
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-zinc-200">
              {reply.body}
            </p>
            <p className="mt-2 text-xs text-zinc-400">
              {reply.authorName ?? "A learner"} ·{" "}
              {reply.createdAt.toLocaleDateString("en-US", { month: "short", day: "numeric" })}
            </p>
          </li>
        ))}
      </ul>

      <section aria-label="Reply" className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">Your reply</h2>
        <ReplyForm threadId={thread.id} signedIn={Boolean(session?.user)} />
      </section>
    </article>
  );
}
