"use client";

import { useActionState } from "react";

import { requestPasswordReset, type AuthFormState } from "@/server/actions/auth";

const initialState: AuthFormState = {};

export function ResetRequestForm() {
  const [state, formAction, pending] = useActionState(requestPasswordReset, initialState);

  return (
    <form action={formAction} className="flex flex-col gap-4">
      {state.success ? (
        <p
          role="status"
          className="rounded-lg bg-emerald-950/60 px-4 py-3 text-sm text-emerald-300"
        >
          {state.success}
        </p>
      ) : null}
      {state.fieldErrors?.email ? (
        <p role="alert" className="text-xs text-red-400">
          {state.fieldErrors.email}
        </p>
      ) : null}

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

      <button
        type="submit"
        disabled={pending}
        className="min-h-11 rounded-lg bg-indigo-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 disabled:opacity-60"
      >
        {pending ? "Creating link…" : "Create reset link"}
      </button>
    </form>
  );
}
