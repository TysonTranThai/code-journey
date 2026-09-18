"use client";

import { useEffect, useState } from "react";

import { useI18n } from "@/lib/i18n/provider";

/**
 * Live preview for markup challenges (Course 1 revision): renders the
 * learner's code in a heavily sandboxed iframe so they can SEE the page
 * they are building while they type.
 *
 * Security: `sandbox=""` (no allow-scripts, no allow-same-origin) — the
 * embedded document cannot execute script or touch the parent. srcdoc
 * inherits the app CSP; style-src allows inline styles, which is all a
 * static render needs. Purely client-side: nothing is executed or stored
 * server-side.
 */

/** True when the current code contains markup worth previewing. */
export function looksLikeMarkup(code: string): boolean {
  // HTML comments count: starter boilerplates are often just
  // `<!-- Write your page below this line -->`, and the learner should see
  // the (empty) page render from the very first keystroke, not a dead pane.
  return (
    /<\s*!--/.test(code) ||
    /<\s*(!doctype|html|head|body|title|meta|h[1-6]|p|div|span|nav|ul|ol|li|a|img|figure|figcaption|section|article|header|footer|main|form|input|button|label|select|option|textarea|fieldset|legend|table|thead|tbody|tr|td|th|caption|style|strong|em|br|hr)\b/i.test(
      code,
    )
  );
}

/** Full document if the learner wrote one; otherwise wrap in a minimal shell. */
function buildPreviewDoc(code: string): string {
  if (/<\s*!doctype html/i.test(code) || /<\s*html[\s>]/i.test(code)) return code;
  return `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body>${code}</body></html>`;
}

export function LivePreview({ code }: { code: string }) {
  const { d } = useI18n();
  // Debounce updates so typing stays smooth (Monaco fires per keystroke).
  const [doc, setDoc] = useState(() => buildPreviewDoc(code));
  useEffect(() => {
    const t = setTimeout(() => setDoc(buildPreviewDoc(code)), 400);
    return () => clearTimeout(t);
  }, [code]);

  return (
    <section aria-label={d.preview.aria} className="glass-card p-4 rounded-2xl flex flex-col gap-2.5 shadow-xl">
      <div className="flex items-center justify-between gap-2 border-b border-white/[0.08] pb-2">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-rose-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/80 inline-block" aria-hidden="true" />
          <h3 className="font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300 ml-1">
            {d.preview.heading}
          </h3>
        </div>
        <span className="badge-pixel badge-pixel-quest text-[10px]">{d.preview.badge}</span>
      </div>
      <iframe
        // sandbox="" = maximum restriction: no scripts, no same-origin, no
        // forms/navigation. The preview is a static render of the markup.
        sandbox=""
        title={d.preview.title}
        srcDoc={doc}
        className="h-72 w-full rounded-xl border border-white/[0.1] bg-white shadow-inner"
      />
      <p className="font-mono text-[11px] text-zinc-400">● {d.preview.caption}</p>
    </section>
  );
}
