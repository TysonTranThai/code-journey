import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { createElement } from "react";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { LessonPager } from "@/components/learn/LessonPager";
import { DifficultyBadge } from "@/components/learn/LessonList";
import {
  getCourse,
  getCurriculumModule,
  getLesson,
  getLessonPractices,
  getLinearLessons,
  getLinearNeighbors,
  getTracks,
} from "@/lib/curriculum/loaders";
import { countLessonThreads } from "@/lib/discussions/threads";
import { getLessonMdx } from "@/lib/curriculum/mdx-map";
import { getServerI18n } from "@/lib/i18n/server";
import { siteConfig } from "@/lib/site-config";

interface LessonPageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
  }>;
}

export function generateStaticParams() {
  // Flatten the full curriculum into every lesson route.
  return getTracks().flatMap((track) => {
    const linear = getLinearLessons(track.id);
    return linear.map((lesson) => ({
      trackId: track.id,
      courseId: lesson.courseId,
      moduleId: lesson.moduleId,
      lessonId: lesson.id,
    }));
  });
}

export async function generateMetadata({ params }: LessonPageProps): Promise<Metadata> {
  const { trackId, courseId, moduleId, lessonId } = await params;
  try {
    const lesson = getLesson(trackId, courseId, moduleId, lessonId);
    return {
      title: lesson.title,
      description: lesson.description,
      alternates: {
        canonical: `${siteConfig.url}/learn/${trackId}/${courseId}/${moduleId}/${lessonId}`,
      },
    };
  } catch {
    return { title: "Lesson not found" };
  }
}

export default async function LessonPage({ params }: LessonPageProps) {
  const { trackId, courseId, moduleId, lessonId } = await params;

  const { locale, d, tp, t } = await getServerI18n();

  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId, undefined, locale);
  } catch {
    notFound();
  }

  const course = getCourse(trackId, courseId, undefined, locale);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId, undefined, locale);
  const { prev, next } = getLinearNeighbors(trackId, lessonId, undefined, locale);
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);
  const threadCount = await countLessonThreads(lessonId);

  const MdxBody = getLessonMdx(lesson.contentPath, locale);
  // Practice sets anchored to this lesson — the “now you code” step of the
  // Learn → Practice flow (Course 1 revision).
  const anchoredPractices = getLessonPractices(trackId, courseId, moduleId, lessonId, undefined, locale);

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          {
            label: course.title,
            href: `/learn/${trackId}/${courseId}`,
          },
          { label: moduleData.title },
        ]}
      />

      <header className="flex flex-col gap-3">
        <div className="flex items-center gap-2">
          <span className="badge-pixel badge-pixel-level">📜 {d.lesson.waypointBadge}</span>
        </div>
        <h1 className="text-3xl font-black tracking-tight text-white sm:text-4xl">
          {lesson.title}
        </h1>
        <div className="flex flex-wrap items-center gap-2 font-mono text-xs text-zinc-400">
          <DifficultyBadge level={lesson.difficulty} />
          <span className="badge-pixel badge-pixel-quest">⏳ {t(d.lesson.minRead, { count: lesson.minutes })}</span>
          <span className="badge-pixel badge-pixel-xp">
            📍 {t(d.lesson.position, {
              index: lesson.linearIndex + 1,
              total: getLinearLessons(trackId).length,
            })}
          </span>
        </div>
        <p className="text-sm text-zinc-300 leading-relaxed">{lesson.description}</p>
      </header>

      {MdxBody ? (
        <div className="lesson-body flex flex-col gap-4 text-zinc-300 leading-relaxed">
          {/* createElement (not JSX) — the component comes from the static
              MDX import map; a PascalCase JSX variable here trips the
              react-compiler "create components during render" rule. */}
          {createElement(MdxBody)}
        </div>
      ) : (
        <p className="rounded-xl border-2 border-amber-500/40 bg-amber-950/40 px-4 py-3 text-sm text-amber-300">
          {d.lesson.missingBody}
        </p>
      )}

      {anchoredPractices.length > 0 && (
        <section
          aria-labelledby="practice-callout-heading"
          className="glass-panel rounded-2xl flex flex-col gap-4 border border-emerald-500/30 bg-emerald-500/[0.04] p-6 shadow-xl"
        >
          <div className="flex items-center justify-between">
            <h2
              id="practice-callout-heading"
              className="badge-pixel badge-pixel-emerald"
            >
              ⚡ {d.lesson.nowPractice}
            </h2>
            <span className="text-xs font-mono font-medium text-emerald-400">{d.lesson.readyToCode}</span>
          </div>
          {anchoredPractices.map((set) => (
            <a
              key={set.id}
              href={`/learn/${trackId}/${courseId}/${moduleId}/practice/${set.id}`}
              className="group flex items-start justify-between gap-4 rounded-xl border border-emerald-500/20 bg-[#0c1322] p-4 transition-all hover:border-emerald-400/50 hover:bg-[#0e1729] shadow-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
            >
              <div>
                <span className="block font-semibold text-zinc-100 group-hover:text-emerald-300 transition-colors">
                  {set.title}
                </span>
                <span className="mt-1 block text-xs text-zinc-400 leading-relaxed">{set.description}</span>
              </div>
              <span className="mt-1 shrink-0 font-mono text-xs text-emerald-400 font-semibold">
                {tp(set.challenges.length, d.lessonList.challengeCount)}·{" "}
                {t(d.lesson.minutes, { count: set.minutes })}
              </span>
            </a>
          ))}
        </section>
      )}

      <nav
        aria-label={d.lesson.discussion}
        className="glass-card rounded-xl flex items-center justify-between gap-3 p-4 transition-all hover:border-emerald-400/50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400"
      >
        <a
          href={`/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/discussion`}
          className="flex w-full items-center justify-between"
        >
          <span className="font-medium text-sm text-zinc-200">💬 {d.lesson.discussion}</span>
          <span className="font-mono text-xs text-zinc-400">
            {threadCount === 0 ? d.lesson.beFirst : tp(threadCount, d.lesson.threads)}
          </span>
        </a>
      </nav>

      <LessonPager trackId={trackId} prev={prev} next={next} />
    </article>
  );
}
