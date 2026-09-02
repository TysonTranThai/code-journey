"use client";

import { useCallback, useEffect, useState } from "react";

/**
 * Draft persistence for challenge code (CHAL-06): localStorage keyed by
 * challenge id, client-only, survives page refreshes. Server-side drafts
 * are a documented deferred item.
 *
 * The hook never touches storage during SSR — `hydrated` flips true after
 * mount so callers can render server/placeholder content first.
 */
export function useDraft(challengeId: string, boilerplate: string) {
  const storageKey = `cj-draft:${challengeId}`;
  const [code, setCode] = useState(boilerplate);
  const [hydrated, setHydrated] = useState(false);

  // Load once after mount. Reading storage synchronously in the effect and
  // deferring the state write via microtask keeps the initial render stable
  // (no cascading render) while restoring the draft before first keystroke.
  useEffect(() => {
    let saved: string | null = null;
    try {
      saved = window.localStorage.getItem(storageKey);
    } catch {
      // private mode / storage disabled — boilerplate is the fallback
    }
    const raf = requestAnimationFrame(() => {
      if (saved !== null) setCode(saved);
      setHydrated(true);
    });
    return () => cancelAnimationFrame(raf);
  }, [storageKey]);

  const save = useCallback(
    (next: string) => {
      setCode(next);
      if (!hydrated) return;
      try {
        window.localStorage.setItem(storageKey, next);
      } catch {
        // quota / privacy errors are non-fatal for drafts
      }
    },
    [storageKey, hydrated],
  );

  const clearDraft = useCallback(() => {
    try {
      window.localStorage.removeItem(storageKey);
    } catch {
      // ignore
    }
    setCode(boilerplate);
  }, [storageKey, boilerplate]);

  return { code, setCode: save, clearDraft, hydrated, hasDraft: code !== boilerplate };
}
