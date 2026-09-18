import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";

import { ChallengeWorkspace } from "@/components/challenge/ChallengeWorkspace";
import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import {
  findPracticeForChallenge,
  getChallenge,
  getCourse,
  getCurriculumModule,
  getLesson,
  getLessonChallenges,
  getLinearLessons,
  getTracks,
} from "@/lib/curriculum/loaders";
import { mentorAvailable } from "@/lib/mentor/types";
import { getServerI18n } from "@/lib/i18n/server";
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
  const { d, locale } = await getServerI18n();
  try {
    const challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId, undefined, locale);
    return {
      title: `${challenge.title} ${d.workspace.challengeSuffix}`,
      description: challenge.prompt.slice(0, 160),
      alternates: {
        canonical: `${siteConfig.url}/learn/${trackId}/${courseId}/${moduleId}/${lessonId}/challenge/${challengeId}`,
      },
    };
  } catch {
    return { title: d.workspace.challengeNotFound };
  }
}

/**
 * Challenge page (03-CONTEXT D-09): lives under its lesson so breadcrumbs
 * and curriculum context are preserved. Public educational content →
 * indexable (PLAT-07). Static (07-08): params enumerate every LESSON-ATTACHED
 * challenge (checkpoints). Challenge ids that moved into practice sets (Course
 * 1 revision phase 2) render dynamically and redirect to their practice URL.
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

  const { locale } = await getServerI18n();
  let lesson;
  try {
    lesson = getLesson(trackId, courseId, moduleId, lessonId, undefined, locale);
  } catch {
    notFound();
  }
  let challenge;
  try {
    challenge = getChallenge(trackId, courseId, moduleId, lessonId, challengeId, undefined, locale);
  } catch {
    // Course 1 revision phase 2: the challenge moved into a practice set.
    // Old URLs (books, saved links, existing sessions) redirect to the new
    // practice challenge — never a dead end.
    const practiceSet = findPracticeForChallenge(trackId, courseId, moduleId, challengeId, undefined, locale);
    if (practiceSet) {
      redirect(
        `/learn/${trackId}/${courseId}/${moduleId}/practice/${practiceSet.id}/${challengeId}`,
      );
    }
    notFound();
  }
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);
  const course = getCourse(trackId, courseId, undefined, locale);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId, undefined, locale);
  const { d, t } = await getServerI18n();

  // 07-08: the page renders statically; auth state for the mentor panel is
  // derived client-side in the workspace. Real authorization happens server-
  // side in the run API (requireUser + ownership), never in the page tree.

  return (
    <article className="mx-auto flex w-full max-w-6xl flex-col gap-6 2xl:max-w-[1800px]">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
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
        <p className="text-sm text-zinc-400">{t(d.workspace.onLesson, { title: lesson.title })}</p>
      </header>

      <ChallengeWorkspace
        challengeId={challenge.id}
        title={challenge.title}
        prompt={challenge.prompt}
        difficulty={challenge.difficulty}
        boilerplate={challenge.boilerplate}
        language={challenge.language}
        lessonTitle={lesson.title}
        lessonHref={`/learn/${trackId}/${courseId}/${moduleId}/${lessonId}`}
        location={{ trackId, courseId, moduleId, lessonId }}
        mentorAvailable={mentorAvailable()}
        signedIn={undefined}
        testHints={challenge.tests.map((t) => t.hint)}
        testNames={challenge.tests.map((t) => t.name)}
      />
    </article>
  );
}
