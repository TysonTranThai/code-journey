#!/usr/bin/env node
/**
 * Sync the locally installed monaco-editor into public/monaco-vs so the
 * browser loads it from our own origin instead of the jsDelivr CDN (07-06).
 *
 * Why: the CDN is a third-party availability dependency for the CORE
 * challenge editor; when it is slow or blocked the editor never mounts
 * (observed in E2E: "Loading editor…" forever). Self-hosting removes the
 * network dependency, keeps E2E deterministic, and avoids a third-party
 * script origin (CSP-friendly later).
 *
 * Idempotent: skips the copy when the target matches the installed version.
 * Run via `pnpm monaco:sync` (also wired into `predev` / `prestart`).
 */
import { cpSync, existsSync, mkdirSync, readFileSync, rmSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const require = createRequire(join(root, "package.json"));
const monacoPkg = JSON.parse(readFileSync(require.resolve("monaco-editor/package.json"), "utf8"));
const src = join(root, "node_modules", "monaco-editor", "min", "vs");
const dst = join(root, "public", "monaco-vs");
const marker = join(dst, ".synced-version");

if (existsSync(marker) && readFileSync(marker, "utf8").trim() === monacoPkg.version) {
  console.log(`[monaco:sync] public/monaco-vs already at ${monacoPkg.version} — skipping`);
  process.exit(0);
}

rmSync(dst, { recursive: true, force: true });
mkdirSync(dst, { recursive: true });
cpSync(src, dst, { recursive: true });
// Keep node_modules copy authoritative; public/ is a build artifact.
rmSync(join(dst, "README.md"), { force: true });
import { writeFileSync } from "node:fs";
writeFileSync(marker, monacoPkg.version);
console.log(`[monaco:sync] copied monaco-editor ${monacoPkg.version} → public/monaco-vs`);
