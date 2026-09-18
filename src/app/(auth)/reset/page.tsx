import type { Metadata } from "next";

import { noIndexMetadata } from "@/lib/seo";
import { getServerI18n } from "@/lib/i18n/server";
import { ResetRequestForm } from "@/components/auth/ResetRequestForm";

export async function generateMetadata(): Promise<Metadata> {
  const { d } = await getServerI18n();
  return noIndexMetadata(d.reset.title);
}

export default async function ResetRequestPage() {
  const { d } = await getServerI18n();
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">{d.reset.title}</h1>
        <p className="mt-1 text-sm text-zinc-400">{d.reset.subtitle}</p>
      </div>

      <ResetRequestForm />
    </div>
  );
}
