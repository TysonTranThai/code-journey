import type { Metadata } from "next";
import Link from "next/link";

import { noIndexMetadata } from "@/lib/seo";
import { RegisterForm } from "@/components/auth/RegisterForm";

export const metadata: Metadata = noIndexMetadata("Create your account");

export default function RegisterPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">Create your account</h1>
        <p className="mt-1 text-sm text-zinc-400">Free, forever. Learn to code at your own pace.</p>
      </div>

      <RegisterForm />

      <p className="text-sm text-zinc-400">
        Already have an account?{" "}
        <Link href="/login" className="font-medium text-indigo-400 hover:text-indigo-300">
          Log in
        </Link>
      </p>
    </div>
  );
}
