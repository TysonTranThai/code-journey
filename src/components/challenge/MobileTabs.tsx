"use client";

import { useId, type ReactNode } from "react";

import { useI18n } from "@/lib/i18n/provider";

/**
 * Accessible tab switcher used on tablet/mobile (PLAT-06): the desktop
 * side-by-side workspace reflows to tabs — intentionally designed mobile
 * layout, not a shrunken desktop. Hidden on desktop via parent CSS.
 *
 * 07-06: panels are lazily rendered — only the ACTIVE tab's content mounts,
 * so Monaco never initializes inside a display:none panel (the root cause of
 * the 0×0 invisible editor). 07-07: `active`/`onChange` are controlled so the
 * parent action bar can switch tabs (e.g. "View results" → Output).
 */
export function MobileTabs({
  tabs,
  active,
  onChange,
}: {
  tabs: { id: string; label: string; content: ReactNode }[];
  active: string;
  onChange: (id: string) => void;
}) {
  const { d } = useI18n();
  const baseId = useId();

  if (tabs.length === 0) return null;

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div
        role="tablist"
        aria-label={d.workspace.panelsAria}
        className="flex shrink-0 border-b border-white/[0.08] bg-[#07090e] rounded-t-2xl p-1.5 gap-1.5"
      >
        {tabs.map((tab) => {
          const selected = tab.id === active;
          return (
            <button
              key={tab.id}
              role="tab"
              id={`${baseId}-tab-${tab.id}`}
              aria-selected={selected}
              aria-controls={`${baseId}-panel-${tab.id}`}
              tabIndex={selected ? 0 : -1}
              onClick={() => onChange(tab.id)}
              className={`flex-1 rounded-xl px-3 py-2 text-xs font-mono font-medium transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 ${
                selected
                  ? "bg-white/[0.1] text-emerald-400 border border-emerald-500/30 shadow-sm"
                  : "border border-transparent text-zinc-400 hover:text-white"
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>
      {tabs.map((tab) =>
        tab.id === active ? (
          <div
            key={tab.id}
            role="tabpanel"
            id={`${baseId}-panel-${tab.id}`}
            aria-labelledby={`${baseId}-tab-${tab.id}`}
            className="flex min-h-0 flex-1 flex-col overflow-auto pt-3"
          >
            {tab.content}
          </div>
        ) : null,
      )}
    </div>
  );
}
