import { describe, expect, it } from "vitest";

import {
  hashPassword,
  hashPasswordSync,
  verifyPassword,
  verifyPasswordSync,
} from "@/lib/auth/password";

describe("password hashing (bcrypt, cost 12)", () => {
  it("hashes and verifies round-trip", async () => {
    const hash = await hashPassword("correct horse battery staple");
    expect(hash).toMatch(/^\$2[aby]\$12\$/);
    expect(await verifyPassword("correct horse battery staple", hash)).toBe(true);
    expect(await verifyPassword("wrong password", hash)).toBe(false);
  });

  it("sync variants behave identically", () => {
    const hash = hashPasswordSync("dev-password-123");
    expect(verifyPasswordSync("dev-password-123", hash)).toBe(true);
    expect(verifyPasswordSync("nope", hash)).toBe(false);
  });

  it("produces unique hashes for identical passwords (salted)", async () => {
    const [a, b] = await Promise.all([
      hashPassword("same-password"),
      hashPassword("same-password"),
    ]);
    expect(a).not.toBe(b);
  });
});
