import { defineConfig } from "@playwright/test";

/**
 * Playwright E2E (Phase 6, PLAT-03).
 *
 * - Chromium locally; webServer boots `pnpm dev` on :3456 (3100 is taken by
 *   an unrelated desktop-app sidecar on this machine); DB URL is loaded from
 *   .env.local via dotenv for the webServer command.
 * - Tests that need Docker (DB/sandbox) skip with a clear message when the
 *   infra is down — same convention as integration suites.
 */
export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 120_000, // register + browse + sandbox cold start + verdict
  reporter: [["list"]],
  use: {
    baseURL: "http://localhost:3456",
    trace: "retain-on-failure",
  },
  webServer: {
    command: "node -r dotenv/config ./scripts/dev-e2e.mjs --port 3456",
    env: { DOTENV_CONFIG_PATH: ".env.local" },
    url: "http://localhost:3456/health",
    reuseExistingServer: true,
    timeout: 60_000,
  },
});
