import type { Metadata } from "next";

import { noIndexMetadata } from "@/lib/seo";
import { ResetRequestForm } from "@/components/auth/ResetRequestForm";

export const metadata: Metadata = noIndexMetadata("Reset your password");

export default function ResetRequestPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">Reset your password</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Enter your email and we will create a reset link. In development the link appears in the
          server console.
        </p>
      </div>

      <ResetRequestForm />
    </div>
  );
}
