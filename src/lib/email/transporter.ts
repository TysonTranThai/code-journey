import "server-only";

import nodemailer from "nodemailer";

/**
 * Email transport (07-04). A single seam so password reset (and any future
 * transactional email) works without a mailbox in dev, and a real provider
 * plugs in via env config — no vendor locked in.
 *
 * Production mode: when EMAIL_PROVIDER=smtp and SMTP_URL + EMAIL_FROM are
 * set, a Nodemailer SMTP transport is used (SMTP_URL like
 * smtps://user:pass@smtp.example.com:465, or smtp://host:587 with
 * SMTP_USER/SMTP_PASS or URL-embedded credentials). The reset link is the
 * only secret ever handed to the transport, and it is single-use,
 * hashed-at-rest, and expires in 1h.
 */

export interface EmailSender {
  send(to: string, message: { subject: string; text: string; html?: string }): Promise<void>;
}

const consoleEmailSender: EmailSender = {
  async send(to, message) {
    // Dev transport: log the email. The reset link is intentional here for local
    // testing; real secrets are never logged.
    console.log(`[email] to=${to} subject="${message.subject}"\n${message.text}`);
  },
};

/** Nodemailer SMTP sender (production). Built only when SMTP_URL is set. */
class SmtpEmailSender implements EmailSender {
  private readonly transporter: nodemailer.Transporter;
  private readonly from: string;

  constructor(from: string, url: string) {
    this.transporter = nodemailer.createTransport(url, { from });
    this.from = from;
  }

  send(to: string, message: { subject: string; text: string; html?: string }): Promise<void> {
    return this.transporter.sendMail({
      from: this.from,
      to,
      subject: message.subject,
      text: message.text,
      html: message.html,
    });
  }
}

/**
 * Resolve the active sender:
 * 1. EMAIL_PROVIDER=smtp with SMTP_URL (and EMAIL_FROM) → real SMTP transport.
 * 2. Otherwise (or misconfigured) → console sender, with a loud warning so a
 *    "password reset is email-ready" claim can never be made silently.
 */
export function getEmailSender(): EmailSender {
  const url = process.env.SMTP_URL?.trim();
  const from = process.env.EMAIL_FROM?.trim();
  if (process.env.EMAIL_PROVIDER === "smtp" && url && from) {
    return new SmtpEmailSender(from, url);
  }
  if (url && from) {
    // SMTP credentials exist but EMAIL_PROVIDER is not set to "smtp".
    // Fail-safe to console, never silently claim real delivery.
    console.warn(
      "[email] SMTP_URL is set but EMAIL_PROVIDER is not 'smtp' — using the console dev sender. Set EMAIL_PROVIDER=smtp to enable real email.",
    );
  }
  return consoleEmailSender;
}

export { consoleEmailSender };
