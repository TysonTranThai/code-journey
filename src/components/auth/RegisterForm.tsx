"use client";

import { useActionState } from "react";

import { register, type AuthFormState } from "@/server/actions/auth";
import { useI18n } from "@/lib/i18n/provider";

const initialState: AuthFormState = {};

const inputClasses =
  "rounded-lg border border-white/[0.1] bg-[#070b14] px-4 py-2.5 text-sm font-mono text-zinc-100 placeholder:text-zinc-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-400 transition-all";

export function RegisterForm({ betaRequired }: { betaRequired: boolean }) {
  const [state, formAction, pending] = useActionState(register, initialState);
  const { d } = useI18n();

  return (
    <form action={formAction} className="flex flex-col gap-4">
      {state.error ? (
        <p role="alert" className="rounded-lg border border-rose-500/30 bg-rose-950/40 px-4 py-3 text-sm font-mono text-rose-300">
          {state.error}
        </p>
      ) : null}

      <div className="flex flex-col gap-1.5">
        <label htmlFor="name" className="text-sm font-medium text-zinc-300">
          {d.register.name}
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
          {d.register.email}
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
          {d.register.password}
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
        <p className="text-xs text-zinc-400 font-mono">{d.register.passwordHint}</p>
      </div>

      {betaRequired ? (
        <div className="flex flex-col gap-1.5">
          <label htmlFor="betaCode" className="text-sm font-medium text-zinc-300">
            {d.register.betaCode}
          </label>
          <input
            id="betaCode"
            name="betaCode"
            type="text"
            required
            autoComplete="off"
            aria-describedby="beta-code-note"
            className={inputClasses}
          />
          <p id="beta-code-note" className="text-xs text-zinc-400 font-mono">
            {d.register.betaNote}
          </p>
        </div>
      ) : null}

      <button
        type="submit"
        disabled={pending}
        className="btn-conductor-primary group min-h-11 w-full py-3 text-sm font-bold shadow-[0_0_20px_rgba(34,197,94,0.4)] disabled:opacity-60"
      >
        <span>{pending ? d.register.submitting : d.register.submit}</span>
        <span className="ml-1.5 text-xs font-mono transition-transform duration-150 group-hover:translate-x-0.5" aria-hidden="true">→</span>
      </button>
    </form>
  );
}
