#!/usr/bin/env node
import { spawn } from "node:child_process";

// 1. Sync Monaco
const sync = spawn("node", ["scripts/sync-monaco.mjs"], { stdio: "inherit" });
sync.on("close", (code) => {
  if (code !== 0) process.exit(code ?? 1);

  console.log("\x1b[36m[dev] Starting Next.js web server and runner worker...\x1b[0m");

  // 2. Start Next.js
  const next = spawn("pnpm", ["next", "dev", "--port", "3000"], {
    stdio: "inherit",
    env: process.env,
  });

  // 3. Start runner worker
  const worker = spawn(
    "node",
    ["--import", "tsx", "--import", "./scripts/worker-imports.mjs", "src/workers/runner.ts"],
    {
      stdio: "inherit",
      env: process.env,
    },
  );

  const shutdown = () => {
    next.kill("SIGTERM");
    worker.kill("SIGTERM");
    process.exit(0);
  };

  process.on("SIGINT", shutdown);
  process.on("SIGTERM", shutdown);
});
