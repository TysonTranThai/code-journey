import bcrypt from "bcryptjs";
import { sql } from "drizzle-orm";
import postgres from "postgres";
import { afterAll, beforeAll, describe, expect, it } from "vitest";

import { passwordResetTokens, profiles, users } from "@/lib/db/schema";

/**
 * Integration tests — run ONLY when the database is reachable.
 * `pnpm db:up` starts Postgres; when it is down this suite skips itself so
 * `pnpm test` stays green on machines without Docker running.
 */
const probe = postgres(process.env.DATABASE_URL ?? "", {
  connect_timeout: 2,
  max: 1,
});

const dbUp = await probe`select 1`.then(() => true).catch(() => false);
await probe.end();

describe.skipIf(!dbUp)("database integration (identity layer)", () => {
  let client: postgres.Sql;
  let db: ReturnType<typeof import("drizzle-orm/postgres-js").drizzle>;

  beforeAll(async () => {
    const postgresClient = (await import("postgres")).default;
    const { drizzle } = await import("drizzle-orm/postgres-js");
    client = postgresClient(process.env.DATABASE_URL ?? "", { max: 1 });
    db = drizzle(client);
  });

  afterAll(async () => {
    await client?.end();
  });

  it("seeds fixtures idempotently (two runs → one row per email)", async () => {
    // Run the seed script twice via its exported logic by exec'ing tsx.
    const { execSync } = await import("node:child_process");
    execSync("pnpm db:seed", { stdio: "pipe" });
    execSync("pnpm db:seed", { stdio: "pipe" });

    const student = await db
      .select()
      .from(users)
      .where(sql`${users.email} = 'dev-student@codejourney.local'`);
    expect(student).toHaveLength(1);
    expect(student[0]?.role).toBe("student");
  });

  it("stores bcrypt hashes that verify against the dev password", async () => {
    const [user] = await db
      .select()
      .from(users)
      .where(sql`${users.email} = 'dev-admin@codejourney.local'`);
    expect(user?.passwordHash).toBeTruthy();
    expect(bcrypt.compareSync("dev-password-123", user?.passwordHash ?? "")).toBe(true);
    expect(bcrypt.compareSync("wrong-password", user?.passwordHash ?? "")).toBe(false);
  });

  it("cascades user deletion to profiles and password reset tokens", async () => {
    const [temp] = await db
      .insert(users)
      .values({
        email: "cascade-test@codejourney.local",
        name: "Cascade Test",
      })
      .returning();
    expect(temp).toBeDefined();

    await db.insert(profiles).values({ userId: temp!.id, displayName: "Cascade" });
    await db.insert(passwordResetTokens).values({
      tokenHash: "a".repeat(64),
      userId: temp!.id,
      expiresAt: new Date(Date.now() + 60_000),
    });

    await db.delete(users).where(sql`${users.id} = ${temp!.id}`);

    const remainingProfiles = await db
      .select()
      .from(profiles)
      .where(sql`${profiles.userId} = ${temp!.id}`);
    const remainingTokens = await db
      .select()
      .from(passwordResetTokens)
      .where(sql`${passwordResetTokens.userId} = ${temp!.id}`);
    expect(remainingProfiles).toHaveLength(0);
    expect(remainingTokens).toHaveLength(0);
  });

  it("rejects duplicate password reset token hashes (unique constraint)", async () => {
    const [temp] = await db
      .insert(users)
      .values({
        email: "unique-token-test@codejourney.local",
        name: "Unique Token Test",
      })
      .returning();
    expect(temp).toBeDefined();

    const expiresAt = new Date(Date.now() + 60_000);
    await db.insert(passwordResetTokens).values({
      tokenHash: "b".repeat(64),
      userId: temp!.id,
      expiresAt,
    });

    await expect(
      db.insert(passwordResetTokens).values({
        tokenHash: "b".repeat(64),
        userId: temp!.id,
        expiresAt,
      }),
    ).rejects.toThrow();

    await db.delete(users).where(sql`${users.id} = ${temp!.id}`);
  });
});
