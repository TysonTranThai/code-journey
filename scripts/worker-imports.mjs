/**
 * Preload for the runner worker (`pnpm worker`): stubs the `server-only`
 * guard for both module systems — ESM (via module.register) and CJS (tsx
 * compiles TS to CJS, which routes through Module._require).
 * See scripts/worker-resolve-hook.mjs.
 */
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { register } from "node:module";
import Module from "node:module";

// Load .env.local (tsx/node don't read it like next dev does).
// Real environment wins over file values.
try {
  const envFile = readFileSync(new URL("../.env.local", import.meta.url), "utf8");
  for (const line of envFile.split("\n")) {
    const match = line.match(/^([A-Z0-9_]+)=["']?([^"'\n]*)["']?\s*$/);
    const key = match?.[1];
    const value = match?.[2];
    if (key && value && !process.env[key]) {
      process.env[key] = value;
    }
  }
} catch {
  // no .env.local — fail later with the clear DATABASE_URL error
}

register("./scripts/worker-resolve-hook.mjs", pathToFileURL("./"));

// CJS path: tsx's compiled output requires "server-only" via Module._compile.
const originalRequire = Module.prototype.require;
Module.prototype.require = function (specifier, ...args) {
  if (specifier === "server-only") {
    return {};
  }
  return originalRequire.call(this, specifier, ...args);
};
