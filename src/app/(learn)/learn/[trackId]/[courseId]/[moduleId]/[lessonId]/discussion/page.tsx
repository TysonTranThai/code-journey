import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { NewThreadForm } from "@/components/discussion/NewThreadForm";
import { ThreadList } from "@/components/discussion/ThreadList";
import { auth } from "@/lib/auth/config";
import { getLesson, getTracks } from "@/lib/curriculum/loaders";
import { getLessonThreads } from "@/lib/discussions/threads";

interface DiscussionPageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
  }>;
}

export const metadata: Metadata = { title: "Discussion" };

/** Lesson discussion index (COMM-03 public read). */
export default async function DiscussionPage({ params }: DiscussionPageProps) {
  const { trackId, courseId, moduleId, lessonId } = await params;

  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId);
  } catch {
    notFound();
  }
  const track = getTracks().find((t) => t.id === trackId);
  const [threads, session] = await Promise.all([getLessonThreads(lessonId), auth()]);
  const hrefBase = `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/discussion`;

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: lesson.title, href: `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}` },
          { label: "Discussion" },
        ]}
      />

      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100 sm:text-3xl">
          Questions & discussion
        </h1>
        <p className="text-sm text-zinc-400">On lesson: {lesson.title}</p>
      </header>

      <section aria-label="Ask a question" className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">Ask a question</h2>
        <NewThreadForm lessonId={lessonId} signedIn={Boolean(session?.user)} />
      </section>

      <section aria-label="Threads" className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">All threads</h2>
        <ThreadList threads={threads} hrefBase={hrefBase} />
      </section>
    </article>
  );
}
