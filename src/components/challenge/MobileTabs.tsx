"use client";

import { useId, type ReactNode } from "react";

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
  label = "Workspace panels",
}: {
  tabs: { id: string; label: string; content: ReactNode }[];
  active: string;
  onChange: (id: string) => void;
  label?: string;
}) {
  const baseId = useId();

  if (tabs.length === 0) return null;

  return (
    <div className="flex min-h-0 flex-1 flex-col">
      <div role="tablist" aria-label={label} className="flex shrink-0 border-b border-zinc-800">
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
              className={`flex-1 px-3 py-2 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400 ${
                selected
                  ? "border-b-2 border-sky-400 text-zinc-100"
                  : "border-b-2 border-transparent text-zinc-400 hover:text-zinc-300"
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
