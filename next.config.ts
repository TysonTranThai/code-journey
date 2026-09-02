import type { NextConfig } from "next";
import createMDX from "@next/mdx";
import path from "node:path";

// NOTE: no remark/rehype options here — Turbopack requires MDX loader options
// to be serializable, and plugin functions are not. If GFM transformations
// (e.g. autolinks, task lists) become necessary, render bodies via
// @mdx-js/mdx compile() at load time instead (documented fallback, D-14).
const withMDX = createMDX({});

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Pin file tracing to this repo (a stray package-lock.json in $HOME otherwise
  // triggers a Next.js warning).
  outputFileTracingRoot: path.join(import.meta.dirname),
  pageExtensions: ["ts", "tsx", "mdx"],
};

export default withMDX(nextConfig);
