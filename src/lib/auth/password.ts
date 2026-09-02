import bcrypt from "bcryptjs";

/**
 * Password hashing (decision D-03). bcryptjs (pure JS) with cost 12 —
 * no native-build fragility; cost can rise later without changing call sites.
 */

const BCRYPT_COST = 12;

export function hashPassword(plain: string): Promise<string> {
  return bcrypt.hash(plain, BCRYPT_COST);
}

export function verifyPassword(plain: string, hash: string): Promise<boolean> {
  return bcrypt.compare(plain, hash);
}

/** Synchronous variants for scripts (seed) and non-hot paths. */
export function hashPasswordSync(plain: string): string {
  return bcrypt.hashSync(plain, BCRYPT_COST);
}

export function verifyPasswordSync(plain: string, hash: string): boolean {
  return bcrypt.compareSync(plain, hash);
}
