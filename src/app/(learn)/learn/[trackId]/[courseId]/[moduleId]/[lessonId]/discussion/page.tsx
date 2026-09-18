import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { NewThreadForm } from "@/components/discussion/NewThreadForm";
import { ThreadList } from "@/components/discussion/ThreadList";
import { auth } from "@/lib/auth/config";
import { getLesson, getTracks } from "@/lib/curriculum/loaders";
import { getServerI18n } from "@/lib/i18n/server";
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

  const { d, t, locale } = await getServerI18n();
  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId, undefined, locale);
  } catch {
    notFound();
  }
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);
  const [threads, session] = await Promise.all([
    getLessonThreads(lessonId),
    auth(),
    getServerI18n(),
  ]);
  const hrefBase = `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/discussion`;

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: lesson.title, href: `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}` },
          { label: d.discussion.crumb },
        ]}
      />

      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100 sm:text-3xl">
          {d.discussion.title}
        </h1>
        <p className="text-sm text-zinc-400">{t(d.discussion.onLesson, { title: lesson.title })}</p>
      </header>

      <section aria-label={d.discussion.askAQuestion} className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">{d.discussion.askAQuestion}</h2>
        <NewThreadForm lessonId={lessonId} signedIn={Boolean(session?.user)} />
      </section>

      <section aria-label={d.discussion.allThreads} className="flex flex-col gap-3">
        <h2 className="text-lg font-semibold text-zinc-100">{d.discussion.allThreads}</h2>
        <ThreadList threads={threads} hrefBase={hrefBase} />
      </section>
    </article>
  );
}
