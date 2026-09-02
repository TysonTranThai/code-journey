import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ChallengeWorkspace } from "@/components/challenge/ChallengeWorkspace";
import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import { getChallenge, getLesson, getTracks } from "@/lib/curriculum/loaders";
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
 * indexable (PLAT-07).
 */
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

  return (
    <article className="mx-auto flex w-full max-w-6xl flex-col gap-6">
      <Breadcrumbs
        items={[
          { label: "Learn", href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: courseId, href: `/learn/${trackId}/${courseId}` },
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
      />
    </article>
  );
}
