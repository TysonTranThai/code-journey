"use server";

import { eq } from "drizzle-orm";
import { AuthError } from "next-auth";
import { z } from "zod";

import {
  hashResetToken,
  generateResetToken,
  isResetTokenValid,
  resetTokenExpiry,
} from "@/lib/auth/reset-token";
import { hashPassword } from "@/lib/auth/password";
import { signIn } from "@/lib/auth/config";
import { sendPasswordResetEmail } from "@/lib/email/send-password-reset";
import { db } from "@/lib/db";
import { passwordResetTokens, profiles, sessions, users } from "@/lib/db/schema";
import { clientIp, consume, HOUR_MS, MINUTE_MS, retryMessage } from "@/lib/rate-limit/limiter";

/**
 * Auth server actions (AUTH-01, AUTH-05). All input is zod-validated at this
 * trust boundary (docs/SECURITY.md). Registration and reset responses are
 * enumeration-safe (decision D-06).
 */

export interface AuthFormState {
  error?: string;
  success?: string;
  fieldErrors?: Partial<Record<"name" | "email" | "password", string>>;
}

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const registerSchema = z.object({
  name: z.string().trim().min(1, "Enter your name").max(80),
  email: z.string().trim().toLowerCase().regex(EMAIL_PATTERN, "Enter a valid email address"),
  password: z.string().min(10, "Use at least 10 characters").max(200, "Password is too long"),
});

const emailSchema = z.object({
  email: z.string().trim().toLowerCase().regex(EMAIL_PATTERN, "Enter a valid email address"),
});

const resetConsumeSchema = z.object({
  token: z.string().min(10),
  password: z.string().min(10, "Use at least 10 characters").max(200, "Password is too long"),
});

function fieldErrorsFrom(error: z.ZodError): AuthFormState["fieldErrors"] {
  const fieldErrors: AuthFormState["fieldErrors"] = {};
  for (const issue of error.issues) {
    const key = issue.path[0];
    if ((key === "name" || key === "email" || key === "password") && !fieldErrors[key]) {
      fieldErrors[key] = issue.message;
    }
  }
  return fieldErrors;
}

/** Sign in with email + password (called by the login form). */
export async function loginAction(
  _prevState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  // Rate limit (07-03): per-IP, plus a short per-minute burst to blunt credential stuffing.
  const ip = await clientIp();
  const lim = await consume("login", ip, 10, HOUR_MS);
  if (!lim.allowed) return { error: retryMessage(lim.resetMs).message };
  const burst = await consume("login-burst", ip, 5, MINUTE_MS);
  if (!burst.allowed) return { error: retryMessage(burst.resetMs).message };

  const email = formData.get("email");
  const password = formData.get("password");
  if (typeof email !== "string" || typeof password !== "string" || !email || !password) {
    return { error: "Enter your email and password." };
  }
  try {
    await signIn("credentials", { email, password, redirectTo: "/learn" });
    return {};
  } catch (error) {
    if (error instanceof AuthError) {
      // Generic message: never reveal whether the email exists.
      return { error: "Invalid email or password." };
    }
    // NEXT_REDIRECT and unknown errors must propagate.
    throw error;
  }
}

/** Create an account, then sign the user in (AUTH-01). */
export async function register(
  _prevState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  // Rate limit (07-03): per-IP; bcrypt cost-12 hashing is CPU-expensive, so limit it.
  // 20/h still blunts bulk abuse while tolerating NAT'd classrooms / shared IPs
  // (school labs legitimately create many accounts from one address).
  const ip = await clientIp();
  const lim = await consume("register", ip, 20, HOUR_MS);
  if (!lim.allowed) return { error: retryMessage(lim.resetMs).message };

  const parsed = registerSchema.safeParse({
    name: formData.get("name"),
    email: formData.get("email"),
    password: formData.get("password"),
  });
  if (!parsed.success) {
    return { fieldErrors: fieldErrorsFrom(parsed.error) };
  }
  const { name, email, password } = parsed.data;

  const [existing] = await db
    .select({ id: users.id })
    .from(users)
    .where(eq(users.email, email))
    .limit(1);
  if (existing) {
    // Generic by design — do not confirm whether the email is taken (D-06).
    return {
      error:
        "If this email can be registered, follow the instructions shown. If it belongs to an existing account, use password reset instead.",
    };
  }

  const passwordHash = await hashPassword(password);
  const [user] = await db.insert(users).values({ name, email, passwordHash }).returning();
  if (!user) {
    return { error: "Could not create the account. Please try again." };
  }
  await db.insert(profiles).values({ userId: user.id, displayName: name }).onConflictDoNothing();

  try {
    await signIn("credentials", { email, password, redirectTo: "/learn" });
    return {};
  } catch (error) {
    if (error instanceof AuthError) {
      return { error: "Account created — please log in." };
    }
    throw error;
  }
}

/** Request a password reset link (AUTH-05). Enumeration-safe by design. */
export async function requestPasswordReset(
  _prevState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  // Rate limit (07-03): per-IP; also prevents reset-token DB flooding.
  const ip = await clientIp();
  const lim = await consume("reset", ip, 5, HOUR_MS);
  if (!lim.allowed) return { error: retryMessage(lim.resetMs).message };

  const parsed = emailSchema.safeParse({ email: formData.get("email") });
  if (!parsed.success) {
    return { fieldErrors: fieldErrorsFrom(parsed.error) };
  }
  const { email } = parsed.data;

  const [user] = await db
    .select({ id: users.id })
    .from(users)
    .where(eq(users.email, email))
    .limit(1);

  if (user) {
    const rawToken = generateResetToken();
    await db.insert(passwordResetTokens).values({
      tokenHash: hashResetToken(rawToken),
      userId: user.id,
      expiresAt: resetTokenExpiry(),
    });
    // 07-04: send via the EmailSender seam (console sender today; a real
    // provider is a single adapter change). The token stays hashed, expiring,
    // and single-use; we only ever hand out the raw link through the transport.
    await sendPasswordResetEmail(email, rawToken);
  }

  // Identical response whether or not the account exists (D-06).
  return {
    success:
      "If an account exists for that email, a reset link has been created. In development, check the server console for the link.",
  };
}

/** Consume a reset token and set a new password (AUTH-05). */
export async function consumePasswordReset(
  _prevState: AuthFormState,
  formData: FormData,
): Promise<AuthFormState> {
  const parsed = resetConsumeSchema.safeParse({
    token: formData.get("token"),
    password: formData.get("password"),
  });
  if (!parsed.success) {
    return { fieldErrors: fieldErrorsFrom(parsed.error) };
  }
  const { token, password } = parsed.data;

  const tokenHash = hashResetToken(token);
  const [row] = await db
    .select()
    .from(passwordResetTokens)
    .where(eq(passwordResetTokens.tokenHash, tokenHash))
    .limit(1);

  if (!row || !isResetTokenValid(row)) {
    return {
      error: "This reset link is invalid or has expired. Request a new one.",
    };
  }

  const passwordHash = await hashPassword(password);
  await db
    .update(users)
    .set({ passwordHash, updatedAt: new Date() })
    .where(eq(users.id, row.userId));
  await db
    .update(passwordResetTokens)
    .set({ usedAt: new Date() })
    .where(eq(passwordResetTokens.id, row.id));
  // Best-effort: drop any database sessions for this user. JWT sessions
  // (the active strategy) cannot be server-revoked and expire on their own.
  await db.delete(sessions).where(eq(sessions.userId, row.userId));

  return { success: "Password updated. You can now log in with your new password." };
}
