/**
 * E2E web-server entry (Playwright webServer command):
 *   node -r dotenv/config ./scripts/dev-e2e.mjs --port 3456
 *
 * dotenv preloads .env.local (DATABASE_URL etc.), then spawns:
 *  - the challenge runner worker (`pnpm worker`) so the full
 *    register → run → verdict loop works in E2E without manual setup
 *  - `next dev` on the requested port
 *
 * Both children are torn down when this entry exits, so Playwright's
 * webServer shutdown takes the worker with it.
 */
import { spawn } from "node:child_process";

const port = process.argv.includes("--port")
  ? process.argv[process.argv.indexOf("--port") + 1]
  : "3456";

const children = [];

function spawnChild(name, command, args) {
  const child = spawn(command, args, { stdio: "inherit", env: process.env });
  child.on("exit", (code) => {
    if (code !== null && code !== 0) {
      console.error(`[dev-e2e] ${name} exited with code ${code}`);
    }
  });
  children.push(child);
  return child;
}

spawnChild("worker", "node", [
  "--import",
  "tsx",
  "--import",
  "./scripts/worker-imports.mjs",
  "src/workers/runner.ts",
]);

spawnChild("next", "pnpm", ["exec", "next", "dev", "-p", port]);

function teardown() {
  for (const child of children) {
    try {
      child.kill("SIGTERM");
    } catch {
      // already gone
    }
  }
}
process.on("SIGINT", teardown);
process.on("SIGTERM", teardown);
process.on("exit", teardown);
