import type { NextConfig } from "next";
import path from "node:path";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Pin file tracing to this repo (a stray package-lock.json in $HOME otherwise
  // triggers a Next.js warning).
  outputFileTracingRoot: path.join(import.meta.dirname),
};

export default nextConfig;
