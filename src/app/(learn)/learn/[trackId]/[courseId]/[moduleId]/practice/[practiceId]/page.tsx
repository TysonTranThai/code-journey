import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { DifficultyBadge } from "@/components/learn/LessonList";
import { PracticeProgress } from "@/components/learn/PracticeProgress";
import {
  getCourse,
  getLoadedCourses,
  getCurriculumModule,
  getModulePractices,
  getPracticeChallenges,
  getPracticeSet,
  getTracks,
} from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";
import type { PracticeLevel } from "@/lib/curriculum/schema";
import { getServerI18n } from "@/lib/i18n/server";

interface PracticePageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    practiceId: string;
  }>;
}

export function generateStaticParams() {
  // Loaded courses only (see getLoadedCourses): skip concurrently scaffolded
  // courses whose modules are still empty — nothing to pre-render.
  return getTracks().flatMap((track) =>
    getLoadedCourses(track.id).flatMap((course) =>
      course.modules.flatMap((moduleRef) =>
        getModulePractices(track.id, course.id, moduleRef.reference).map((practice) => ({
          trackId: track.id,
          courseId: course.id,
          moduleId: moduleRef.reference,
          practiceId: practice.id,
        })),
      ),
    ),
  );
}

export async function generateMetadata({ params }: PracticePageProps): Promise<Metadata> {
  const { trackId, courseId, moduleId, practiceId } = await params;
  try {
    const practiceSet = getPracticeSet(trackId, courseId, moduleId, practiceId);
    const { d } = await getServerI18n();
    return {
      title: `${d.practice.badge}: ${practiceSet.title}`,
      description: practiceSet.description,
      alternates: {
        canonical: `${siteConfig.url}/learn/${trackId}/${courseId}/${moduleId}/practice/${practiceId}`,
      },
    };
  } catch {
    const { d } = await getServerI18n();
    return { title: `${d.practice.badge}: 404` };
  }
}

export default async function PracticePage({ params }: PracticePageProps) {
  const { trackId, courseId, moduleId, practiceId } = await params;

  const { d, tp, t, locale } = await getServerI18n();
  let practiceSet;
  try {
    practiceSet = getPracticeSet(trackId, courseId, moduleId, practiceId, undefined, locale);
  } catch {
    notFound();
  }
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);
  const course = getCourse(trackId, courseId, undefined, locale);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId, undefined, locale);
  const challenges = getPracticeChallenges(trackId, courseId, moduleId, practiceId, undefined, locale);

  const practiceHref = `/learn/${trackId}/${courseId}/${moduleId}/practice/${practiceId}`;
  const backToLesson = practiceSet.afterLesson
    ? `/learn/${trackId}/${courseId}/${moduleId}/${practiceSet.afterLesson}`
    : null;

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: course.title, href: `/learn/${trackId}/${courseId}` },
          { label: moduleData.title, href: `/learn/${trackId}/${courseId}#${moduleData.id}` },
          { label: `${d.practice.badge}: ${practiceSet.title}` },
        ]}
      />

      <header className="flex flex-col gap-3">
        <p className="inline-flex w-fit items-center gap-2 rounded-full border border-amber-500/40 bg-amber-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-amber-300">
          <span aria-hidden>⚡</span> {d.practice.badge}
        </p>
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
          {practiceSet.title}
        </h1>
        <div className="flex flex-wrap items-center gap-3 text-sm text-zinc-400">
          <DifficultyBadge level={practiceSet.difficulty} />
          <span>{t(d.practice.minutesOfCoding, { count: practiceSet.minutes })}</span>
          <span>{tp(challenges.length, d.practice.challengeCount)}</span>
        </div>
        <p className="text-zinc-400">{practiceSet.description}</p>
      </header>

      <section
        aria-label={d.practice.progressAria}
        className="rounded-xl border border-zinc-800 bg-zinc-900/40 p-4"
      >
        <PracticeProgress challengeIds={challenges.map((c) => c.id)} practiceHref={practiceHref} />
      </section>

      <section aria-labelledby="practice-what" className="flex flex-col gap-3">
        <h2
          id="practice-what"
          className="text-sm font-semibold uppercase tracking-wide text-zinc-400"
        >
          {d.practice.whatYouWillPractice}
        </h2>
        <ol className="flex flex-col divide-y divide-zinc-800/60 rounded-xl border border-zinc-800">
          {challenges.map((challenge, index) => (
            <li key={challenge.id}>
              <Link
                href={`${practiceHref}/${challenge.id}`}
                className="flex items-center justify-between gap-4 px-4 py-3.5 hover:bg-zinc-900/60 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-400"
              >
                <span className="flex items-center gap-3">
                  <span
                    aria-hidden
                    className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-zinc-700 text-xs font-semibold text-zinc-300"
                  >
                    {index + 1}
                  </span>
                  <span className="font-medium text-zinc-100">{challenge.title}</span>
                </span>
                <span className="flex shrink-0 items-center gap-3 text-sm text-zinc-400">
                  {challenge.level ? (
                    <span className="hidden rounded-full border border-indigo-500/40 bg-indigo-950/40 px-2 py-0.5 text-xs font-medium text-indigo-300 sm:inline">
                      {d.level[challenge.level as PracticeLevel]}
                    </span>
                  ) : null}
                  <DifficultyBadge level={challenge.difficulty} />
                </span>
              </Link>
            </li>
          ))}
        </ol>
      </section>

      {backToLesson ? (
        <p className="text-sm text-zinc-500">
          {d.practice.needConceptFirst}{" "}
          <Link href={backToLesson} className="text-indigo-400 underline-offset-2 hover:underline">
            {d.practice.rereadLesson}
          </Link>
          .
        </p>
      ) : null}
    </article>
  );
}
