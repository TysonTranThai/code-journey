"use client";

import { useActionState } from "react";

import { consumePasswordReset, type AuthFormState } from "@/server/actions/auth";

const initialState: AuthFormState = {};

export function ResetConsumeForm({ token }: { token: string }) {
  const [state, formAction, pending] = useActionState(consumePasswordReset, initialState);

  return (
    <form action={formAction} className="flex flex-col gap-4">
      <input type="hidden" name="token" value={token} />

      {state.error ? (
        <p role="alert" className="rounded-lg bg-red-950/60 px-4 py-3 text-sm text-red-300">
          {state.error}
        </p>
      ) : null}
      {state.success ? (
        <p
          role="status"
          className="rounded-lg bg-emerald-950/60 px-4 py-3 text-sm text-emerald-300"
        >
          {state.success}
        </p>
      ) : null}
      {state.fieldErrors?.password ? (
        <p role="alert" className="text-xs text-red-400">
          {state.fieldErrors.password}
        </p>
      ) : null}

      <div className="flex flex-col gap-1.5">
        <label htmlFor="password" className="text-sm font-medium text-zinc-300">
          New password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          minLength={10}
          className="rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-zinc-100 placeholder:text-zinc-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
        />
      </div>

      <button
        type="submit"
        disabled={pending}
        className="min-h-11 rounded-lg bg-indigo-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 disabled:opacity-60"
      >
        {pending ? "Updating…" : "Set new password"}
      </button>
    </form>
  );
}
