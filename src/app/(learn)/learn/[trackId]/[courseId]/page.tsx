import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { LessonList, type LessonFlowGroup } from "@/components/learn/LessonList";
import { getServerI18n } from "@/lib/i18n/server";
import {
  getCourse,
  getCurriculumModule,
  getLessonChallenges,
  getLessonPractices,
  getLinearLessons,
  getLoadedCourses,
  getTracks,
} from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";

interface CoursePageProps {
  params: Promise<{ trackId: string; courseId: string }>;
}

export function generateStaticParams() {
  // Loaded courses only (see getLoadedCourses): skip concurrently scaffolded
  // courses whose modules are still empty — there is no page to pre-render.
  return getTracks().flatMap((track) => {
    const loaded = getLoadedCourses(track.id);
    return loaded.map((course) => ({ trackId: track.id, courseId: course.id }));
  });
}

export async function generateMetadata({ params }: CoursePageProps): Promise<Metadata> {
  const { trackId, courseId } = await params;
  let course;
  try {
    course = getCourse(trackId, courseId);
  } catch {
    return { title: "Course not found" };
  }
  return {
    title: course.title,
    description: course.description,
    alternates: { canonical: `${siteConfig.url}/learn/${trackId}/${courseId}` },
  };
}

export default async function CoursePage({ params }: CoursePageProps) {
  const { trackId, courseId } = await params;

  const { d, tp, t, locale } = await getServerI18n();
  let course;
  try {
    course = getCourse(trackId, courseId, undefined, locale);
  } catch {
    notFound();
  }
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);

  const linearLessons = getLinearLessons(trackId, undefined, locale);
  const courseLessons = linearLessons.filter((l) => l.courseId === courseId);
  const totalMinutes = courseLessons.reduce((sum, l) => sum + l.minutes, 0);
  const hoursText =
    totalMinutes >= 90
      ? t(d.course.hours, { count: (Math.round(totalMinutes / 15) * 15) / 60 })
      : t(d.course.minutes, { count: totalMinutes });
  // Course 1 revision: challenge count = all practice-set challenges.
  const challengeCount = course.modules.reduce((sum, modRef) => {
    const practices = getLessonPractices(trackId, courseId, modRef.reference, "", undefined, locale);
    return sum + practices.reduce((s, p) => s + p.challenges.length, 0);
  }, 0);

  return (
    <div className="flex flex-col gap-8">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: course.title },
        ]}
      />

      <header className="conductor-window flex flex-col gap-4 rounded-2xl border border-white/[0.08] bg-[#0c101b] p-6 sm:p-8 shadow-xl">
        <div className="flex items-center gap-2">
          <span className="badge-pixel badge-pixel-quest font-mono">{d.course.questlineBadge}</span>
          <span className="text-emerald-400 text-sm font-mono" aria-hidden="true">✦</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-5xl">
          {course.title}
        </h1>
        <p className="max-w-2xl text-base text-zinc-300 leading-relaxed font-normal">{course.description}</p>
        <div className="flex flex-wrap items-center gap-2 pt-1 font-mono">
          <span className="badge-pixel badge-pixel-level">📜 {tp(courseLessons.length, d.course.lessons)}</span>
          <span className="badge-pixel badge-pixel-xp">⚡ {tp(challengeCount, d.course.challenges)}</span>
          <span className="badge-pixel badge-pixel-quest">⏳ ~{hoursText}</span>
          <span className="badge-pixel badge-pixel-emerald">⭐ {d.course.noExperience}</span>
        </div>

      {course.prerequisites?.length ? (
        <div className="flex flex-wrap items-center gap-2 rounded-xl border border-amber-500/30 bg-amber-950/20 px-4 py-3 text-sm text-amber-200">
          <span aria-hidden="true">🔒</span>
          <span className="font-semibold">{tp(course.prerequisites.length, d.course.prerequisite)}</span>
          {course.prerequisites.map((prereqId) => {
            const prereq = getTracks(undefined, locale)
              .flatMap((tr) => tr.courses.map((c) => c.reference))
              .includes(prereqId);
            const label = prereq
              ? getCourse(trackId, prereqId, undefined, locale).title
              : prereqId;
            return prereq ? (
              <Link
                key={prereqId}
                href={`/learn/${trackId}/${prereqId}`}
                className="font-semibold text-amber-300 underline underline-offset-2 hover:text-white"
              >
                {label}
              </Link>
            ) : (
              <span key={prereqId}>{label}</span>
            );
          })}
        </div>
      ) : null}
      </header>

      {course.audience ? (
        <section className="conductor-window max-w-2xl p-6 rounded-xl border border-white/[0.08] bg-[#0c101b] shadow-lg">
          <h2 className="badge-pixel badge-pixel-level mb-2 font-mono">
            {d.course.whoFor}
          </h2>
          <p className="mt-1 text-sm leading-relaxed text-zinc-300">{course.audience}</p>
        </section>
      ) : null}

      {course.outcomes?.length ? (
        <section className="conductor-window max-w-2xl p-6 rounded-xl border border-white/[0.08] bg-[#0c101b] shadow-lg">
          <h2 className="badge-pixel badge-pixel-emerald mb-3 font-mono">
            {d.course.outcomes}
          </h2>
          <ul className="grid gap-2 sm:grid-cols-2">
            {course.outcomes.map((outcome) => (
              <li key={outcome} className="flex items-start gap-2 text-sm text-zinc-300">
                <span aria-hidden="true" className="text-emerald-400 font-bold">
                  ✓
                </span>
                <span>{outcome}</span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <div className="flex flex-col gap-10">
        {course.modules.map((moduleRef, index) => {
          const moduleData = getCurriculumModule(trackId, courseId, moduleRef.reference, undefined, locale);
          const moduleLessons = linearLessons.filter((lesson) => lesson.moduleId === moduleData.id);
          // Each lesson groups its anchored practice sets + checkpoint
          // challenge so the list shows the Learn → Practice flow inline.
          const groups: LessonFlowGroup[] = moduleLessons.map((lesson) => ({
            lesson,
            practices: getLessonPractices(trackId, courseId, moduleData.id, lesson.id, undefined, locale).map(
              (set) => ({
                id: set.id,
                title: set.title,
                description: set.description,
                minutes: set.minutes,
                challenges: set.challenges,
              }),
            ),
            challenges: getLessonChallenges(trackId, courseId, moduleData.id, lesson.id, undefined, locale).map(
              (c) => ({ id: c.id, title: c.title }),
            ),
          }));
          return (
            <section key={moduleData.id} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <div className="flex items-center gap-2">
                  <span className="badge-pixel badge-pixel-level">{t(d.course.chapter, { count: index + 1 })}</span>
                  <span className="text-xs font-mono text-zinc-400">· {tp(groups.length, d.course.waypoints)}</span>
                </div>
                <h2 className="text-2xl font-black text-white">{moduleData.title}</h2>
                <p className="text-sm text-zinc-300">{moduleData.summary}</p>
              </div>
              <LessonList
                groups={groups}
                trackId={trackId}
                courseId={courseId}
                moduleId={moduleData.id}
              />
            </section>
          );
        })}
      </div>
    </div>
  );
}
