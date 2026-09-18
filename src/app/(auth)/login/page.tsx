import type { Metadata } from "next";
import Link from "next/link";

import { githubProviderEnabled } from "@/lib/auth/config";
import { noIndexMetadata } from "@/lib/seo";
import { getServerI18n } from "@/lib/i18n/server";
import { LoginForm } from "@/components/auth/LoginForm";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getServerI18n();
  return noIndexMetadata(d.login.title);
}

export default async function LoginPage() {
  const { d } = await getServerI18n();
  const githubEnabled = githubProviderEnabled();
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">{d.login.title}</h1>
        <p className="mt-1 text-sm text-zinc-400">{d.login.subtitle}</p>
      </div>

      <LoginForm githubEnabled={githubEnabled} />

      <p className="text-sm text-zinc-400">
        {d.login.newHere}{" "}
        <Link href="/register" className="font-medium text-emerald-400 hover:text-emerald-300">
          {d.login.createAccount}
        </Link>
      </p>
      <p className="text-sm text-zinc-400">
        {d.login.forgot}{" "}
        <Link href="/reset" className="font-medium text-emerald-400 hover:text-emerald-300">
          {d.login.resetIt}
        </Link>
      </p>
    </div>
  );
}
