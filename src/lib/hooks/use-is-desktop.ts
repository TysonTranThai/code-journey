"use client";

import { useSyncExternalStore } from "react";

const QUERY = "(min-width: 1024px)"; // Tailwind `lg`

function subscribe(onChange: () => void) {
  const mql = window.matchMedia(QUERY);
  mql.addEventListener("change", onChange);
  return () => mql.removeEventListener("change", onChange);
}

/**
 * True when the viewport is desktop-sized (Tailwind `lg` and up).
 *
 * 07-06: the challenge workspace previously rendered the editor in BOTH the
 * desktop grid and the mobile tabs (CSS-hidden copies). Two Monaco instances
 * mounted; the hidden desktop copy confused measurements and wasted resources.
 * Rendering a single branch driven by the real media query removes that entire
 * class of bugs. SSR renders the mobile layout, then switches after hydration
 * (useSyncExternalStore contract — no hydration mismatch).
 */
export function useIsDesktop(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(QUERY).matches,
    () => false,
  );
}
