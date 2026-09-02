import type { Metadata } from "next";
import Link from "next/link";

import { githubProviderEnabled } from "@/lib/auth/config";
import { noIndexMetadata } from "@/lib/seo";
import { LoginForm } from "@/components/auth/LoginForm";

export const metadata: Metadata = noIndexMetadata("Log in");

export default function LoginPage() {
  const githubEnabled = githubProviderEnabled();
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-zinc-100">Welcome back</h1>
        <p className="mt-1 text-sm text-zinc-400">
          Log in to keep your streak and track your progress.
        </p>
      </div>

      <LoginForm githubEnabled={githubEnabled} />

      <p className="text-sm text-zinc-400">
        New here?{" "}
        <Link href="/register" className="font-medium text-indigo-400 hover:text-indigo-300">
          Create an account
        </Link>
      </p>
      <p className="text-sm text-zinc-400">
        Forgot your password?{" "}
        <Link href="/reset" className="font-medium text-indigo-400 hover:text-indigo-300">
          Reset it
        </Link>
      </p>
    </div>
  );
}
