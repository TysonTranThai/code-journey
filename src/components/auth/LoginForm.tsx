"use client";

import { useActionState } from "react";
import { signIn } from "next-auth/react";

import { loginAction, type AuthFormState } from "@/server/actions/auth";
import { useI18n } from "@/lib/i18n/provider";

const initialState: AuthFormState = {};

export function LoginForm({ githubEnabled }: { githubEnabled: boolean }) {
  const [state, formAction, pending] = useActionState(loginAction, initialState);
  const { d } = useI18n();

  return (
    <div className="flex flex-col gap-4">
      {state.error ? (
        <p role="alert" className="rounded-lg bg-red-950/60 px-4 py-3 text-sm text-red-300">
          {state.error}
        </p>
      ) : null}

      <form action={formAction} className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <label htmlFor="email" className="text-sm font-medium text-zinc-300">
            {d.login.email}
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="rounded-lg border border-white/[0.1] bg-[#070b14] px-4 py-2.5 text-sm font-mono text-zinc-100 placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 transition-all"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="password" className="text-sm font-medium text-zinc-300">
            {d.login.password}
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            className="rounded-lg border border-white/[0.1] bg-[#070b14] px-4 py-2.5 text-sm font-mono text-zinc-100 placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 transition-all"
          />
        </div>

        <button
          type="submit"
          disabled={pending}
          className="btn-conductor-primary min-h-11 w-full py-3 text-sm font-bold shadow-[0_0_20px_rgba(34,197,94,0.4)] disabled:opacity-60"
        >
          {pending ? d.login.submitting : d.login.submit}
        </button>
      </form>

      {githubEnabled ? (
        <>
          <div className="flex items-center gap-3 text-xs uppercase tracking-wider text-zinc-500">
            <span className="h-px flex-1 bg-white/[0.08]" />
            {d.login.or}
            <span className="h-px flex-1 bg-white/[0.08]" />
          </div>
          <button
            type="button"
            onClick={() => void signIn("github", { redirectTo: "/learn" })}
            className="btn-conductor-secondary min-h-11 w-full py-2.5 text-sm font-medium"
          >
            {d.login.github}
          </button>
        </>
      ) : null}
    </div>
  );
}
