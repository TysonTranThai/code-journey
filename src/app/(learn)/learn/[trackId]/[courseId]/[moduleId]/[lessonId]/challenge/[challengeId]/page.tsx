import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ChallengeWorkspace } from "@/components/challenge/ChallengeWorkspace";
import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import {
  getChallenge,
  getCourse,
  getCurriculumModule,
  getLesson,
  getLessonChallenges,
  getLinearLessons,
  getTracks,
} from "@/lib/curriculum/loaders";
import { mentorAvailable } from "@/lib/mentor/types";
import { siteConfig } from "@/lib/site-config";

interface ChallengePageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    lessonId: string;
    challengeId: string;
  }>;
}

export async function generateMetadata({ params }: ChallengePageProps): Promise<Metadata> {
  const { trackId, courseId, moduleId, lessonId, challengeId } = await params;
  try {
    const challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId);
    return {
      title: `${challenge.title} — Challenge`,
      description: challenge.prompt.slice(0, 160),
      alternates: {
        canonical: `${siteConfig.url}/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/challenge/${challengeId}`,
      },
    };
  } catch {
    return { title: "Challenge not found" };
  }
}

/**
 * Challenge page (03-CONTEXT D-09): lives under its lesson so breadcrumbs
 * and curriculum context are preserved. Public educational content →
 * indexable (PLAT-07). Static (07-08): params enumerate every challenge.
 */
export function generateStaticParams() {
  return getTracks().flatMap((track) =>
    getLinearLessons(track.id).flatMap((lesson) =>
      getLessonChallenges(track.id, lesson.courseId, lesson.moduleId, lesson.id).map(
        (challenge) => ({
          trackId: track.id,
          courseId: lesson.courseId,
          moduleId: lesson.moduleId,
          lessonId: lesson.id,
          challengeId: challenge.id,
        }),
      ),
    ),
  );
}

export default async function ChallengePage({ params }: ChallengePageProps) {
  const { trackId, courseId, moduleId, lessonId, challengeId } = await params;

  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId);
  } catch {
    notFound();
  }
  let challenge;
  try {
    challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId);
  } catch {
    notFound();
  }
  const track = getTracks().find((t) => t.id === trackId);
  const course = getCourse(trackId, courseId);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId);

  // 07-08: the page renders statically; auth state for the mentor panel is
  // derived client-side in the workspace. Real authorization happens server-
  // side in the run API (requireUser + ownership), never in the page tree.

  return (
    <article className="mx-auto flex w-full max-w-6xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: course.title, href: `/learn/${trackId}/${courseId}` },
          {
            label: moduleData.title,
            href: `/learn/${trackId}/${courseId}#${moduleData.id}`,
          },
          {
            label: lesson.title,
            href: `/learn/${trackId}/${courseId}/${moduleId}/${lessonId}`,
          },
          { label: challenge.title },
        ]}
      />

      <header className="flex flex-col gap-2">
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100 sm:text-3xl">
          {challenge.title}
        </h1>
        <p className="text-sm text-zinc-400">Challenge on lesson: {lesson.title}</p>
      </header>

      <ChallengeWorkspace
        challengeId={challenge.id}
        title={challenge.title}
        prompt={challenge.prompt}
        difficulty={challenge.difficulty}
        boilerplate={challenge.boilerplate}
        lessonTitle={lesson.title}
        lessonHref={`/learn/${trackId}/${courseId}/${moduleId}/${lessonId}`}
        location={{ trackId, courseId, moduleId, lessonId }}
        mentorAvailable={mentorAvailable()}
        signedIn={undefined}
        testHints={challenge.tests.map((t) => t.hint)}
      />
    </article>
  );
}
