import "server-only";

import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

import * as schema from "./schema";

/**
 * Server-only Drizzle client (postgres-js driver).
 * Singleton via globalThis so dev HMR / route re-imports reuse one connection pool.
 */
declare global {
  var __codejourneyDbClient: postgres.Sql | undefined;
}

function createClient(): postgres.Sql {
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      "DATABASE_URL is not set. Copy .env.example to .env.local and start the DB with `pnpm db:up`.",
    );
  }
  return postgres(url, {
    // Small pool; the modular monolith shares one process in dev.
    max: 10,
    // Fail fast in dev instead of hanging a request for the default 30s.
    connect_timeout: 5,
  });
}

const client = globalThis.__codejourneyDbClient ?? createClient();
if (process.env.NODE_ENV !== "production") {
  globalThis.__codejourneyDbClient = client;
}

export const db = drizzle(client, { schema });
export { schema };
export type Db = typeof db;
