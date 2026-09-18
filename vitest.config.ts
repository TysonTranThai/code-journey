import { defineConfig, type Plugin } from "vitest/config";
import { readFileSync } from "node:fs";
import path from "node:path";

/**
 * Compile MDX for vitest with the same @mdx-js/mdx the Next build uses
 * (next.config.ts has no remark/rehype options, so the defaults match).
 * Keeps tests that import the generated mdx-map (static lesson-body
 * imports) runnable in plain Node.
 */
const mdxPlugin: Plugin = {
  name: "vitest-mdx",
  enforce: "pre",
  async transform(_code, id) {
    if (!id.endsWith(".mdx")) return undefined;
    const { compile } = await import("@mdx-js/mdx");
    const source = readFileSync(id.replace(/\?.*$/, ""), "utf8");
    // Default outputFormat (ESM) — Vite's SSR transform handles the exports.
    const compiled = String(await compile(source, {}));
    return { code: compiled, map: null };
  },
};

// Load .env.local into process.env for integration tests (DATABASE_URL etc.).
// Keys already set in the real environment win.
try {
  const envFile = readFileSync(path.resolve(__dirname, ".env.local"), "utf8");
  for (const line of envFile.split("\n")) {
    const match = line.match(/^([A-Z0-9_]+)=["']?([^"'\n]*)["']?\s*$/);
    const key = match?.[1];
    const value = match?.[2];
    if (key && value && !process.env[key]) {
      process.env[key] = value;
    }
  }
} catch {
  // .env.local missing — integration DB tests will skip themselves.
}

export default defineConfig({
  plugins: [mdxPlugin],
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
    testTimeout: 15_000,
    fileParallelism: false,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      // The real `server-only` package throws outside RSC — vitest runs in
      // plain Node, so alias it to an empty stub. Next's production build
      // still enforces the real guard.
      "server-only": path.resolve(__dirname, "tests/stubs/server-only.ts"),
    },
  },
});
