import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

/**
 * Health check (Phase 6 observability): reports overall status + DB
 * reachability. Never throws — a down DB is a status, not a 500.
 */
export async function GET() {
  let db: "up" | "down" = "down";
  try {
    const { db: database } = await import("@/lib/db");
    await database.execute("select 1");
    db = "up";
  } catch {
    db = "down";
  }

  return NextResponse.json({
    status: "ok",
    db,
    service: "code-journey",
    version: "0.1.0",
    timestamp: new Date().toISOString(),
  });
}
