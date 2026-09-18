"use client";

import type { ErrorExplanation } from "@/lib/mentor/error-explainer";
import { useI18n } from "@/lib/i18n/provider";

export function ErrorExplanationCard({
  explanation,
}: {
  explanation: ErrorExplanation;
}) {
  const { d } = useI18n();

  return (
    <div
      role="region"
      aria-label={d.console.errorExplanationTitle}
      className="conductor-window rounded-xl border border-amber-500/30 bg-gradient-to-br from-amber-950/40 via-[#181109]/70 to-[#0d0d14] p-3.5 shadow-lg backdrop-blur-md transition-all duration-200 animate-in fade-in slide-in-from-top-1"
    >
      <div className="flex items-center justify-between gap-2 border-b border-amber-500/20 pb-2 mb-2.5">
        <div className="flex items-center gap-2">
          <span
            className="flex h-5 w-5 items-center justify-center rounded-md bg-amber-500/20 text-amber-300 text-xs font-bold"
            aria-hidden="true"
          >
            💡
          </span>
          <h4 className="font-sans text-xs font-bold uppercase tracking-wider text-amber-200">
            {d.console.errorExplanationTitle}
          </h4>
        </div>
        <span className="badge-pixel badge-pixel-streak text-[9px] border-amber-500/30 text-amber-300 bg-amber-950/50">
          {d.console.errorExplanationBadge}
        </span>
      </div>

      <div className="flex flex-col gap-2.5 text-xs">
        <div className="flex flex-col gap-1">
          <span className="font-mono text-[10px] font-semibold uppercase tracking-wider text-amber-400/90">
            › {d.console.errorMeaningLabel}:
          </span>
          <p className="text-zinc-200 leading-relaxed pl-3 border-l-2 border-amber-500/30">
            {explanation.message}
          </p>
        </div>

        <div className="flex flex-col gap-1">
          <span className="font-mono text-[10px] font-semibold uppercase tracking-wider text-emerald-400/90">
            › {d.console.errorFixLabel}:
          </span>
          <p className="text-emerald-300 leading-relaxed pl-3 border-l-2 border-emerald-500/30">
            {explanation.hint}
          </p>
        </div>
      </div>
    </div>
  );
}
