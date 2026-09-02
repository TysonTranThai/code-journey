import { defineConfig } from "drizzle-kit";
import { readFileSync } from "node:fs";

// drizzle-kit does not load Next.js env files; read .env.local manually.
function databaseUrl(): string {
  if (process.env.DATABASE_URL) return process.env.DATABASE_URL;
  try {
    const envFile = readFileSync(".env.local", "utf8");
    const match = envFile.match(/^DATABASE_URL=["']?([^"'\n]+)["']?\s*$/m);
    if (match?.[1]) return match[1];
  } catch {
    // .env.local missing — fall through to the error below.
  }
  console.error(
    "DATABASE_URL is not set. Start the database with `pnpm db:up` and copy .env.example to .env.local.",
  );
  process.exit(1);
}

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/lib/db/schema.ts",
  out: "./src/lib/db/migrations",
  dbCredentials: { url: databaseUrl() },
});
