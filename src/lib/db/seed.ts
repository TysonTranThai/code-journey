import bcrypt from "bcryptjs";
import { readFileSync } from "node:fs";
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

import { profiles, users } from "./schema";

/**
 * Identity fixtures for local development (decision D-10). Curriculum content
 * is NOT seeded — it lives as version-controlled files under src/content/.
 * Idempotent: safe to run repeatedly (upserts by email).
 *
 * Run: pnpm db:seed
 */

function databaseUrl(): string {
  if (process.env.DATABASE_URL) return process.env.DATABASE_URL;
  try {
    const envFile = readFileSync(".env.local", "utf8");
    const match = envFile.match(/^DATABASE_URL=["']?([^"'\n]+)["']?\s*$/m);
    if (match?.[1]) return match[1];
  } catch {
    // fall through
  }
  console.error(
    "DATABASE_URL is not set. Start the database with `pnpm db:up`, then copy .env.example to .env.local.",
  );
  process.exit(1);
}

const DEV_PASSWORD = "dev-password-123";

const fixtures = [
  {
    email: "dev-student@codejourney.local",
    name: "Dev Student",
    role: "student" as const,
    displayName: "Dev Student",
  },
  {
    email: "dev-admin@codejourney.local",
    name: "Dev Admin",
    role: "admin" as const,
    displayName: "Dev Admin",
  },
];

async function seed(): Promise<void> {
  const client = postgres(databaseUrl(), { max: 1 });
  const db = drizzle(client);
  const passwordHash = bcrypt.hashSync(DEV_PASSWORD, 12);

  for (const fixture of fixtures) {
    const [user] = await db
      .insert(users)
      .values({
        email: fixture.email,
        name: fixture.name,
        role: fixture.role,
        passwordHash,
      })
      .onConflictDoUpdate({
        target: users.email,
        set: { name: fixture.name, role: fixture.role, passwordHash },
      })
      .returning();

    if (!user) throw new Error(`Failed to upsert fixture ${fixture.email}`);

    await db
      .insert(profiles)
      .values({ userId: user.id, displayName: fixture.displayName })
      .onConflictDoUpdate({
        target: profiles.userId,
        set: { displayName: fixture.displayName },
      });

    console.log(`seeded: ${fixture.email} (${fixture.role})`);
  }

  console.log(`\nDev password for both fixtures: ${DEV_PASSWORD}`);
  console.log("These are LOCAL DEVELOPMENT fixtures only — not real accounts.");
  await client.end();
}

seed().catch((error) => {
  console.error("Seed failed:", error);
  process.exit(1);
});
