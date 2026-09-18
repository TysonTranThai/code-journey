"use client";

import { useEffect, useState } from "react";

import { useI18n } from "@/lib/i18n/provider";

/**
 * Practice-set progress (Course 1 revision). Server truth lives in
 * progress_events (contentType "challenge"), written only when the runner
 * records a passed verdict. This component reads the per-challenge status
 * endpoint and marks which items of the set are done.
 *
 * On static pages there is no session at render time, so this hydrates
 * client-side; the endpoint is read-only and returns only the caller's
 * own records.
 */
export function PracticeProgress({
  challengeIds,
  practiceHref,
}: {
  challengeIds: string[];
  practiceHref: string;
}) {
  const [completed, setCompleted] = useState<Set<string>>(new Set());
  const [loaded, setLoaded] = useState(false);
  const { d, t } = useI18n();

  useEffect(() => {
    let cancelled = false;
    fetch(`/api/progress/challenges?ids=${challengeIds.join(",")}`, { cache: "no-store" })
      .then((res) => (res.ok ? res.json() : null))
      .then((data: { completed?: string[] } | null) => {
        if (!cancelled && data?.completed) setCompleted(new Set(data.completed));
      })
      .catch(() => undefined)
      .finally(() => {
        if (!cancelled) setLoaded(true);
      });
    return () => {
      cancelled = true;
    };
  }, [challengeIds]);

  const done = challengeIds.filter((id) => completed.has(id)).length;
  const total = challengeIds.length;
  const pct = total === 0 ? 0 : Math.round((done / total) * 100);

  return (
    <div className="flex flex-col gap-2">
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-zinc-200">
          {loaded ? (
            <>{t(d.practiceProgress.complete, { done, total })}</>
          ) : (
            <span className="text-zinc-500">{d.practiceProgress.checking}</span>
          )}
        </span>
        <span className="text-zinc-400">{pct}%</span>
      </div>
      <div
        role="progressbar"
        aria-valuemin={0}
        aria-valuemax={total}
        aria-valuenow={done}
        aria-label={t(d.practiceProgress.ariaLabel, { done, total })}
        className="h-2 w-full overflow-hidden rounded-full bg-zinc-800"
      >
        <div
          className="h-full rounded-full bg-amber-400 transition-all"
          style={{ width: `${pct}%` }}
        />
      </div>
      <p className="text-xs text-zinc-500">
        {done === total && total > 0 ? <>{d.practiceProgress.setComplete}</> : null}
        {done < total && loaded ? (
          <>
            {d.practiceProgress.nextUp}{" "}
            <a
              href={`${practiceHref}/${challengeIds.find((id) => !completed.has(id))}`}
              className="text-amber-300 underline-offset-2 hover:underline"
            >
              {d.practiceProgress.continuePracticing}
            </a>
          </>
        ) : null}
      </p>
    </div>
  );
}
