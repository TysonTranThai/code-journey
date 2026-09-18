import type { Metadata } from "next";
import { notFound } from "next/navigation";

import { ChallengeWorkspace } from "@/components/challenge/ChallengeWorkspace";
import { Breadcrumbs } from "@/components/learn/Breadcrumbs";
import {
  getCourse,
  getLoadedCourses,
  getCurriculumModule,
  getModulePractices,
  getPracticeChallenge,
  getPracticeChallenges,
  getPracticeSet,
  getTracks,
} from "@/lib/curriculum/loaders";
import { mentorAvailable } from "@/lib/mentor/types";
import { getServerI18n } from "@/lib/i18n/server";
import { siteConfig } from "@/lib/site-config";

interface PracticeChallengePageProps {
  params: Promise<{
    trackId: string;
    courseId: string;
    moduleId: string;
    practiceId: string;
    challengeId: string;
  }>;
}

/**
 * Practice challenge page (Course 1 revision). NOTE: the challenge id is a
 * direct child segment of the practice set (`/practice/<set>/<challenge>`),
 * NOT nested under a static `challenge/` segment. Inside the `(learn)` route
 * group, an 8-segment dynamic route deterministically overflows the stack in
 * Next 16.3.4 Turbopack dev (7 and 9 segments are unaffected; verified by
 * isolated repro). 7 segments also keeps practice URLs shorter.
 */
export function generateStaticParams() {
  // Loaded courses only (see getLoadedCourses): skip concurrently scaffolded
  // courses whose modules are still empty — nothing to pre-render.
  return getTracks().flatMap((track) =>
    getLoadedCourses(track.id).flatMap((course) => {
      const courseId = course.id;
      return course.modules.flatMap((moduleRef) => {
        const moduleId = moduleRef.reference;
        return getModulePractices(track.id, courseId, moduleId).flatMap((practiceSet) =>
          getPracticeChallenges(track.id, courseId, moduleId, practiceSet.id).map((challenge) => ({
            trackId: track.id,
            courseId,
            moduleId,
            practiceId: practiceSet.id,
            challengeId: challenge.id,
          })),
        );
      });
    }),
  );
}

export async function generateMetadata({ params }: PracticeChallengePageProps): Promise<Metadata> {
  const { trackId, courseId, moduleId, practiceId, challengeId } = await params;
  const { d, locale } = await getServerI18n();
  try {
    const challenge = getPracticeChallenge(trackId, courseId, moduleId, practiceId, challengeId, undefined, locale);
    return {
      title: `${challenge.title} — ${d.practice.badge}`,
      description: challenge.prompt.slice(0, 160),
      alternates: {
        canonical: `${siteConfig.url}/learn/${trackId}/${courseId}/${moduleId}/practice/${practiceId}/${challengeId}`,
      },
    };
  } catch {
    return { title: d.practice.badge };
  }
}

export default async function PracticeChallengePage({ params }: PracticeChallengePageProps) {
  const { trackId, courseId, moduleId, practiceId, challengeId } = await params;

  const { locale } = await getServerI18n();
  let practiceSet;
  try {
    practiceSet = getPracticeSet(trackId, courseId, moduleId, practiceId, undefined, locale);
  } catch {
    notFound();
  }
  let challenge;
  try {
    challenge = getPracticeChallenge(trackId, courseId, moduleId, practiceId, challengeId, undefined, locale);
  } catch {
    notFound();
  }
  const track = getTracks(undefined, locale).find((t) => t.id === trackId);
  const course = getCourse(trackId, courseId, undefined, locale);
  const moduleData = getCurriculumModule(trackId, courseId, moduleId, undefined, locale);
  const setChallenges = getPracticeChallenges(trackId, courseId, moduleId, practiceId, undefined, locale);
  const index = setChallenges.findIndex((c) => c.id === challengeId);
  const next = index >= 0 && index < setChallenges.length - 1 ? setChallenges[index + 1] : null;
  const prev = index > 0 ? setChallenges[index - 1] : null;

  const practiceHref = `/learn/${trackId}/${courseId}/${moduleId}/practice/${practiceId}`;
  const { d, t } = await getServerI18n();

  return (
    // Workspace, not article: on very wide screens use the room so the
    // three-pane layout (instructions | code | output) gets real width.
    <article className="mx-auto flex w-full max-w-6xl flex-col gap-6 2xl:max-w-[1800px]">
      <Breadcrumbs
        items={[
          { label: d.breadcrumb.learn, href: "/learn" },
          { label: track?.title ?? trackId, href: `/learn/${trackId}` },
          { label: course.title, href: `/learn/${trackId}/${courseId}` },
          { label: moduleData.title, href: `/learn/${trackId}/${courseId}#${moduleData.id}` },
          { label: `${d.practice.badge}: ${practiceSet.title}`, href: practiceHref },
          { label: challenge.title },
        ]}
      />

      <header className="flex flex-col gap-2">
        <p className="inline-flex w-fit items-center gap-2 rounded-full border border-amber-500/40 bg-amber-950/40 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-amber-300">
          <span aria-hidden>⚡</span>{" "}
          {t(d.practice.position, { index: index + 1, total: setChallenges.length })}
        </p>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100 sm:text-3xl">
          {challenge.title}
        </h1>
      </header>

      <ChallengeWorkspace
        challengeId={challenge.id}
        title={challenge.title}
        prompt={challenge.prompt}
        difficulty={challenge.difficulty}
        boilerplate={challenge.boilerplate}
        language={challenge.language}
        lessonTitle={`${d.practice.badge}: ${practiceSet.title}`}
        lessonHref={practiceHref}
        location={{
          trackId,
          courseId,
          moduleId,
          // Practice challenges carry their set id in the lessonId slot; the
          // run API prefers practiceId and ignores this for practice runs.
          lessonId: practiceId,
        }}
        practiceId={practiceId}
        mentorAvailable={mentorAvailable()}
        signedIn={undefined}
        testHints={challenge.tests.map((t) => t.hint)}
        testNames={challenge.tests.map((t) => t.name)}
      />

      <nav
        aria-label={d.practice.navAria}
        className="flex items-center justify-between gap-3 text-sm"
      >
        {prev ? (
          <a
            href={`${practiceHref}/${prev.id}`}
            className="rounded-lg border border-zinc-800 px-4 py-2 text-zinc-300 hover:border-zinc-600 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-400"
          >
            ← {prev.title}
          </a>
        ) : (
          <span />
        )}
        {next ? (
          <a
            href={`${practiceHref}/${next.id}`}
            className="rounded-lg border border-amber-500/40 bg-amber-950/30 px-4 py-2 font-medium text-amber-200 hover:border-amber-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-amber-300"
          >
            {t(d.practice.nextChallenge, { title: next.title })}
          </a>
        ) : (
          <a
            href={practiceHref}
            className="rounded-lg border border-emerald-500/40 bg-emerald-950/30 px-4 py-2 font-medium text-emerald-200 hover:border-emerald-400 focus-visible:outline focus-visible:outline-2 focus-visible:outline-emerald-300"
          >
            {d.practice.backToOverview}
          </a>
        )}
      </nav>
    </article>
  );
}
