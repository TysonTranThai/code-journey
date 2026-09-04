import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { LessonList } from "@/components/learn/LessonList";
import {
  getCourse,
  getCurriculumModule,
  getLessonChallenges,
  getLinearLessons,
  getTracks,
} from "@/lib/curriculum/loaders";
import { siteConfig } from "@/lib/site-config";

interface CoursePageProps {
  params: Promise<{ trackId: string; courseId: string }>;
}

export function generateStaticParams() {
  return getTracks().flatMap((track) =>
    track.courses.map((ref) => ({ trackId: track.id, courseId: ref.reference })),
  );
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

  let course;
  try {
    course = getCourse(trackId, courseId);
  } catch {
    notFound();
  }
  const track = getTracks().find((t) => t.id === trackId);

  const linearLessons = getLinearLessons(trackId);
  const courseLessons = linearLessons.filter((l) => l.courseId === courseId);
  const totalMinutes = courseLessons.reduce((sum, l) => sum + l.minutes, 0);
  const hoursText =
    totalMinutes >= 90
      ? `${(Math.round(totalMinutes / 15) * 15) / 60} hours`
      : `${totalMinutes} minutes`;
  const challengeCount = courseLessons.reduce((sum, l) => {
    try {
      return sum + getLessonChallenges(trackId, courseId, l.moduleId, l.id).length;
    } catch {
      return sum;
    }
  }, 0);

  return (
    <div className="flex flex-col gap-8">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: course.title },
        ]}
      />

      <header className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
          {course.title}
        </h1>
        <p className="max-w-2xl text-zinc-400">{course.description}</p>
        <p className="flex flex-wrap gap-x-4 gap-y-1 text-sm text-zinc-500">
          <span>{courseLessons.length} lessons</span>
          <span>{challengeCount} challenges</span>
          <span>~{hoursText}</span>
          <span>Beginner — no experience needed</span>
        </p>
      </header>

      {course.audience ? (
        <section className="max-w-2xl rounded-lg border border-zinc-800 bg-zinc-900/50 p-5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-400">
            Who this course is for
          </h2>
          <p className="mt-2 text-sm leading-relaxed text-zinc-300">{course.audience}</p>
        </section>
      ) : null}

      {course.outcomes?.length ? (
        <section className="max-w-2xl">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-zinc-400">
            What you will be able to do
          </h2>
          <ul className="mt-3 grid gap-2 sm:grid-cols-2">
            {course.outcomes.map((outcome) => (
              <li key={outcome} className="flex gap-2 text-sm text-zinc-300">
                <span aria-hidden className="text-emerald-400">
                  ✓
                </span>
                <span>{outcome}</span>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <div className="flex flex-col gap-10">
        {course.modules.map((moduleRef) => {
          const moduleData = getCurriculumModule(trackId, courseId, moduleRef.reference);
          const moduleLessons = linearLessons.filter((lesson) => lesson.moduleId === moduleData.id);
          return (
            <section key={moduleData.id} className="flex flex-col gap-4">
              <div className="flex flex-col gap-1">
                <h2 className="text-xl font-semibold text-zinc-100">{moduleData.title}</h2>
                <p className="text-sm text-zinc-400">{moduleData.summary}</p>
              </div>
              <LessonList lessons={moduleLessons} />
            </section>
          );
        })}
      </div>
    </div>
  );
}
