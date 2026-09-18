"use client";

import { useSyncExternalStore } from "react";

const QUERY = "(min-width: 1440px)"; // Tailwind `2xl`

function subscribe(onChange: () => void) {
  const mql = window.matchMedia(QUERY);
  mql.addEventListener("change", onChange);
  return () => mql.removeEventListener("change", onChange);
}

/**
 * True when the viewport fits the three-pane challenge layout
 * (instructions | code | output side by side — Tailwind `2xl` and up).
 * Same single-branch pattern as useIsDesktop (07-06): exactly one layout
 * renders, so Monaco never mounts twice.
 */
export function useIsWide(): boolean {
  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(QUERY).matches,
    () => false,
  );
}
