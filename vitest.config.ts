import { defineConfig } from "vitest/config";
import { readFileSync } from "node:fs";
import path from "node:path";

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
  test: {
    environment: "node",
    include: ["tests/**/*.test.ts"],
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
