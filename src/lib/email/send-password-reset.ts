import "server-only";

import { siteConfig } from "@/lib/site-config";

import { getEmailSender } from "./transporter";

/**
 * Compose and send the password reset email (AUTH-05, 07-04). The link embeds
 * the raw reset token; the token itself is stored hashed + expiring + single-use
 * (see src/lib/auth/reset-token.ts). Always goes through the EmailSender seam so
 * a real provider can be added without changing the action.
 */
export async function sendPasswordResetEmail(to: string, rawToken: string): Promise<void> {
  const url = `${siteConfig.url}/reset/${rawToken}`;
  await getEmailSender().send(to, {
    subject: "Reset your Code Journey password",
    text: [
      "You asked to reset your password.",
      "",
      `Use this link to choose a new one:`,
      url,
      "",
      "This link expires in 1 hour and can be used once.",
      "If you didn't ask for this, you can safely ignore this email.",
      "",
    ].join("\n"),
  });
}
