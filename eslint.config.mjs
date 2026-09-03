import { defineConfig, globalIgnores } from "eslint/config";
import coreWebVitals from "eslint-config-next/core-web-vitals";
import typescript from "eslint-config-next/typescript";

export default defineConfig([
  globalIgnores([
    ".next/**",
    "node_modules/**",
    "coverage/**",
    "playwright-report/**",
    "test-results/**",
    // Self-hosted third-party editor bundle (07-06): minified, not our code.
    "public/monaco-vs/**",
  ]),
  ...coreWebVitals,
  ...typescript,
  {
    rules: {
      // TypeScript-aware overrides can be added here as the codebase grows.
    },
  },
]);
