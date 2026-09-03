import { beforeEach, describe, expect, it, vi } from "vitest";

const sent: { to: string; subject: string; text: string }[] = [];
vi.mock("@/lib/email/transporter", () => ({
  getEmailSender: () => ({
    send: async (to: string, message: { subject: string; text: string }) => {
      sent.push({ to, subject: message.subject, text: message.text });
    },
  }),
}));

import { sendPasswordResetEmail } from "@/lib/email/send-password-reset";

describe("password reset email (07-04)", () => {
  beforeEach(() => {
    sent.length = 0;
  });

  it("sends to the given address with a reset link and single-use note", async () => {
    await sendPasswordResetEmail("learner@example.com", "rawtok123");
    expect(sent).toHaveLength(1);
    const m = sent[0]!;
    expect(m.to).toBe("learner@example.com");
    expect(m.subject).toMatch(/reset/i);
    expect(m.text).toContain("/reset/rawtok123");
    expect(m.text).toContain("once");
    expect(m.text).toContain("expires");
  });
});
