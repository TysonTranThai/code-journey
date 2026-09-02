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
  getLinearLessons,
  getLinearNeighbors,
  getTracks,
} from "@/lib/curriculum/loaders";
import { getLessonMdx } from "@/lib/curriculum/mdx-map";
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

  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId);
  } catch {
    notFound();
  }

  const course = getCourse(trackId, courseId);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId);
  const { prev, next } = getLinearNeighbors(trackId, lessonId);
  const track = getTracks().find((t) => t.id === trackId);

  const MdxBody = getLessonMdx(lesson.contentPath);

  return (
    <article className="mx-auto flex w-full max-w-3xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          {
            label: course.title,
            href: `/learn/${trackId}/${courseId}`,
          },
          { label: moduleData.title },
        ]}
      />

      <header className="flex flex-col gap-3">
        <h1 className="text-3xl font-bold tracking-tight text-zinc-100 sm:text-4xl">
          {lesson.title}
        </h1>
        <div className="flex flex-wrap items-center gap-3 text-sm text-zinc-400">
          <DifficultyBadge level={lesson.difficulty} />
          <span>{lesson.minutes} min read</span>
          <span>
            Lesson {lesson.linearIndex + 1} of {getLinearLessons(trackId).length}
          </span>
        </div>
        <p className="text-zinc-400">{lesson.description}</p>
      </header>

      {MdxBody ? (
        <div className="lesson-body flex flex-col gap-4 text-zinc-300">
          {/* createElement (not JSX) — the component comes from the static
              MDX import map; a PascalCase JSX variable here trips the
              react-compiler "create components during render" rule. */}
          {createElement(MdxBody)}
        </div>
      ) : (
        <p className="rounded-lg bg-amber-950/60 px-4 py-3 text-sm text-amber-300">
          Lesson body is missing from the build map. This is a content pipeline bug — please report
          it.
        </p>
      )}

      <LessonPager trackId={trackId} prev={prev} next={next} />
    </article>
  );
}
