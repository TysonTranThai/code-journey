import type { Metadata } from "next";

/**
 * Shared SEO helpers (PLAT-07).
 *
 * Public educational pages are indexable; private pages (auth flows, and later
 * dashboards/profiles) must never be indexed.
 */

/** Metadata for private pages: keep them out of search indexes. */
export function noIndexMetadata(title: string): Metadata {
  return {
    title,
    robots: { index: false, follow: false },
  };
}
