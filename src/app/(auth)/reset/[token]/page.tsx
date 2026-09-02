import type { Metadata } from "next";

import { noIndexMetadata } from "@/lib/seo";
import { ResetConsumeForm } from "@/components/auth/ResetConsumeForm";

export const metadata: Metadata = noIndexMetadata("Choose a new password");

export default async function ResetTokenPage({ params }: { params: Promise<{ token: string }> }) {
  const { token } = await params;
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">Choose a new password</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Pick something long and unique — at least 10 characters.
        </p>
      </div>

      <ResetConsumeForm token={token} />
    </div>
  );
}
