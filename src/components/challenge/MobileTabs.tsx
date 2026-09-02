"use client";

import { useId, useState, type ReactNode } from "react";

/**
 * Accessible tab switcher used on tablet/mobile (PLAT-06): the desktop
 * side-by-side workspace reflows to tabs — intentionally designed mobile
 * layout, not a shrunken desktop. Hidden on desktop via parent CSS.
 */
export function MobileTabs({
  tabs,
}: {
  tabs: { id: string; label: string; content: ReactNode }[];
}) {
  const [active, setActive] = useState(tabs[0]?.id ?? "");
  const baseId = useId();

  if (tabs.length === 0) return null;

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div
        role="tablist"
        aria-label="Workspace panels"
        className="flex shrink-0 border-b border-zinc-800"
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
              onClick={() => setActive(tab.id)}
              className={`flex-1 px-3 py-2 text-sm font-medium transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-sky-400 ${
                selected
                  ? "border-b-2 border-sky-400 text-zinc-100"
                  : "border-b-2 border-transparent text-zinc-500 hover:text-zinc-300"
              }`}
            >
              {tab.label}
            </button>
          );
        })}
      </div>
      {tabs.map((tab) => (
        <div
          key={tab.id}
          role="tabpanel"
          id={`${baseId}-panel-${tab.id}`}
          aria-labelledby={`${baseId}-tab-${tab.id}`}
          hidden={tab.id !== active}
          className="min-h-0 flex-1 overflow-auto pt-3"
        >
          {tab.content}
        </div>
      ))}
    </div>
  );
}
