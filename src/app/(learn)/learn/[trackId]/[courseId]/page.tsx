import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { LessonList } from "@/components/learn/LessonList";
import {
  getCourse,
  getCurriculumModule,
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
      </header>

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
