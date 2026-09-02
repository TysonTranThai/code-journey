import { describe, expect, it } from "vitest";

import * as schema from "@/lib/db/schema";

// Pure schema assertions — no database required.
describe("db schema (phase 2 identity tables)", () => {
  it("defines all six identity tables", () => {
    expect(schema.users).toBeDefined();
    expect(schema.accounts).toBeDefined();
    expect(schema.sessions).toBeDefined();
    expect(schema.verificationTokens).toBeDefined();
    expect(schema.passwordResetTokens).toBeDefined();
    expect(schema.profiles).toBeDefined();
  });

  it("gives users a student/admin role enum defaulting to student", () => {
    expect(schema.userRole.enumValues).toEqual(["student", "admin"]);
    expect(schema.users.role.default).toBe("student");
  });

  it("stores a nullable passwordHash (OAuth-only users have none)", () => {
    expect(schema.users.passwordHash.notNull).toBe(false);
  });

  it("keeps password reset tokens hashed at rest, not raw", () => {
    expect(schema.passwordResetTokens.tokenHash.notNull).toBe(true);
    const columnNames = Object.keys(schema.passwordResetTokens);
    expect(columnNames).not.toContain("token");
  });

  it("does not contain later-phase tables (curriculum/progress/submissions)", () => {
    // Guardrail for the "DB stores user-generated state only" decision.
    const exported = Object.keys(schema);
    expect(exported).not.toContain("progressEvents");
    expect(exported).not.toContain("submissions");
    expect(exported).not.toContain("discussionThreads");
  });
});
