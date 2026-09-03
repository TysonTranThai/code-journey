import "server-only";

/**
 * Email transport (07-04). A single seam so password reset (and any future
 * transactional email) works without a real mailbox today, and a real provider
 * can be dropped in later with a one-adapter change — no vendor locked in.
 *
 * Default: a console sender (logs the composed email) that needs no network or
 * credentials. A real provider is selected from EMAIL_PROVIDER + credentials in
 * production (see getEmailSender).
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

/**
 * Resolve the active sender. When EMAIL_PROVIDER and its credentials are set in
 * production, a real provider sender is returned here. Until then the console
 * sender is the only one Phase 7 ships.
 */
export function getEmailSender(): EmailSender {
  // TODO(production): build a real sender (Nodemailer/SMTP or a transactional
  // API) from EMAIL_* env vars and return it here. Single seam — one change.
  return consoleEmailSender;
}
