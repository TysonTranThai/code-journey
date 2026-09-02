"use client";

import { useActionState } from "react";

import { register, type AuthFormState } from "@/server/actions/auth";

const initialState: AuthFormState = {};

const inputClasses =
  "rounded-lg border border-zinc-700 bg-zinc-950 px-3 py-2.5 text-zinc-100 placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500";

export function RegisterForm() {
  const [state, formAction, pending] = useActionState(register, initialState);

  return (
    <form action={formAction} className="flex flex-col gap-4">
      {state.error ? (
        <p role="alert" className="rounded-lg bg-amber-950/60 px-4 py-3 text-sm text-amber-300">
          {state.error}
        </p>
      ) : null}

      <div className="flex flex-col gap-1.5">
        <label htmlFor="name" className="text-sm font-medium text-zinc-300">
          Name
        </label>
        <input
          id="name"
          name="name"
          type="text"
          autoComplete="name"
          required
          aria-describedby={state.fieldErrors?.name ? "name-error" : undefined}
          className={inputClasses}
        />
        {state.fieldErrors?.name ? (
          <p id="name-error" role="alert" className="text-xs text-red-400">
            {state.fieldErrors.name}
          </p>
        ) : null}
      </div>

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
          aria-describedby={state.fieldErrors?.email ? "email-error" : undefined}
          className={inputClasses}
        />
        {state.fieldErrors?.email ? (
          <p id="email-error" role="alert" className="text-xs text-red-400">
            {state.fieldErrors.email}
          </p>
        ) : null}
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="password" className="text-sm font-medium text-zinc-300">
          Password
        </label>
        <input
          id="password"
          name="password"
          type="password"
          autoComplete="new-password"
          required
          minLength={10}
          aria-describedby={state.fieldErrors?.password ? "password-error" : undefined}
          className={inputClasses}
        />
        {state.fieldErrors?.password ? (
          <p id="password-error" role="alert" className="text-xs text-red-400">
            {state.fieldErrors.password}
          </p>
        ) : null}
        <p className="text-xs text-zinc-500">At least 10 characters.</p>
      </div>

      <button
        type="submit"
        disabled={pending}
        className="min-h-11 rounded-lg bg-indigo-500 px-5 py-2.5 font-medium text-white transition-colors hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-400 disabled:opacity-60"
      >
        {pending ? "Creating account…" : "Create account"}
      </button>
    </form>
  );
}
