import type { Metadata } from "next";
import Link from "next/link";

import { noIndexMetadata } from "@/lib/seo";
import { betaGateEnabled } from "@/lib/beta/access";
import { getServerI18n } from "@/lib/i18n/server";
import { RegisterForm } from "@/components/auth/RegisterForm";

// The beta gate is environment-configured and must be evaluated per request —
// a prerendered page would bake the gate state in at build time (Phase 9).
export const dynamic = "force-dynamic";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getServerI18n();
  return noIndexMetadata(d.register.title);
}

export default async function RegisterPage() {
  const { d } = await getServerI18n();
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">{d.register.title}</h1>
        <p className="mt-1 text-sm text-zinc-400">{d.register.subtitle}</p>
      </div>

      <RegisterForm betaRequired={betaGateEnabled()} />

      <p className="text-sm text-zinc-400">
        {d.register.haveAccount}{" "}
        <Link href="/login" className="font-medium text-emerald-400 hover:text-emerald-300">
          {d.register.loginLink}
        </Link>
      </p>
    </div>
  );
}
