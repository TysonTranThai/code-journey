"use client";

import { useActionState } from "react";
import { signIn } from "next-auth/react";

import { loginAction, type AuthFormState } from "@/server/actions/auth";

const initialState: AuthFormState = {};

export function LoginForm({ githubEnabled }: { githubEnabled: boolean }) {
  const [state, formAction, pending] = useActionState(loginAction, initialState);

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
            Email
          </label>
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            className="rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-zinc-100 placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
          />
        </div>

        <div className="flex flex-col gap-1.5">
          <label htmlFor="password" className="text-sm font-medium text-zinc-300">
            Password
          </label>
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            className="rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-zinc-100 placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
          />
        </div>

        <button
          type="submit"
          disabled={pending}
          className="min-h-11 rounded-lg bg-indigo-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 disabled:opacity-60"
        >
          {pending ? "Logging in…" : "Log in"}
        </button>
      </form>

      {githubEnabled ? (
        <>
          <div className="flex items-center gap-3 text-xs uppercase tracking-wider text-zinc-400">
            <span className="h-px flex-1 bg-zinc-800" />
            or
            <span className="h-px flex-1 bg-zinc-800" />
          </div>
          <button
            type="button"
            onClick={() => void signIn("github", { redirectTo: "/learn" })}
            className="min-h-11 rounded-lg border border-zinc-700 bg-zinc-900 px-5 py-2.5 font-medium text-zinc-100 transition-colors hover:border-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400"
          >
            Continue with GitHub
          </button>
        </>
      ) : null}
    </div>
  );
}
