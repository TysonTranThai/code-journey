import { defineConfig } from "@playwright/test";

/**
 * Beta-deployment E2E config (Phase 9).
 *
 * Runs the SAME specs as the local suite against a deployed beta over its
 * public HTTPS URL — proving the learner loop works through the real entry
 * point (tunnel / reverse proxy), not just on loopback.
 *
 * Usage:
 *   BETA_BASE_URL=https://<beta-host> E2E_INVITE_CODE=<code> \
 *     npx playwright test --config=playwright.beta.config.ts
 *
 * - No webServer block: the beta must already be up.
 * - No globalSetup: the beta database is production-like; rate-limiter state
 *   is managed by the deployment, not wiped by tests.
 * - ngrok free tunnels show an interstitial unless this header is present.
 */
const baseURL = process.env.BETA_BASE_URL;

if (!baseURL) {
  throw new Error("BETA_BASE_URL is required (e.g. https://your-beta.ngrok-free.dev)");
}

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 150_000, // tunnel latency + sandbox cold start + verdict
  reporter: [["list"]],
  use: {
    baseURL,
    trace: "retain-on-failure",
    extraHTTPHeaders: {
      "ngrok-skip-browser-warning": "true",
    },
  },
});
