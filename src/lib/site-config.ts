export const siteConfig = {
  name: "Code Journey",
  tagline: "Learn to code. Free, forever.",
  description:
    "A free, next-generation coding education platform: structured curriculum, interactive auto-graded challenges, and an AI mentor that teaches instead of solving.",
  /** Canonical origin for metadata, sitemap, and robots. */
  url: process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000",
} as const;
