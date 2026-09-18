"use client";

import { useEffect, useRef } from "react";
import Editor, { loader, type OnMount } from "@monaco-editor/react";

/**
 * Self-host Monaco from our own origin (07-06): the jsDelivr CDN proved to be
 * a third-party availability dependency for the CORE challenge editor (slow
 * or blocked CDN → editor stuck at "Loading editor…" forever). `pnpm
 * monaco:sync` copies the installed monaco-editor into public/monaco-vs
 * (gitignored build artifact, run via predev/prestart); this loader config
 * points the AMD loader there so the browser never touches a third-party
 * origin.
 */
loader.config({ paths: { vs: "/monaco-vs" } });

/**
 * Monaco wrapper for challenge code. Loads the HTML language mode by
 * default; theme matches the platform's dark palette. Loading via the
 * @monaco-editor/react CDN loader keeps the bundle small (documented
 * discretion in 03-CONTEXT D-10); local bundling is a Phase 6 option.
 */
export function CodeEditor({
  value,
  onChange,
  onRun,
  language = "html",
  ariaLabel,
}: {
  value: string;
  onChange: (next: string) => void;
  onRun?: () => void;
  language?: string;
  ariaLabel: string;
}) {
  const onRunRef = useRef(onRun);
  useEffect(() => {
    onRunRef.current = onRun;
  }, [onRun]);

  const onMount: OnMount = (editor, monaco) => {
    editor.focus();
    editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => {
      onRunRef.current?.();
    });
    // 07-06 belt-and-suspenders: with automaticLayout enabled the ResizeObserver
    // normally handles sizing, but an explicit layout pass on mount guarantees
    // Monaco resolves real dimensions even if the container settled late
    // (e.g. lazy-mounted tab panel).
    requestAnimationFrame(() => editor.layout());
  };

  return (
    <div
      className="h-full min-h-[16rem] overflow-hidden rounded-lg border border-zinc-800 bg-[#1e1e1e]"
      data-testid="code-editor"
    >
      <Editor
        height="100%"
        defaultLanguage={language}
        language={language}
        value={value}
        onChange={(v) => onChange(v ?? "")}
        onMount={onMount}
        theme="vs-dark"
        aria-label={ariaLabel}
        options={{
          minimap: { enabled: false },
          fontSize: 14,
          lineNumbers: "on",
          scrollBeyondLastLine: false,
          wordWrap: "on",
          tabSize: 2,
          automaticLayout: true,
          renderWhitespace: "selection",
          padding: { top: 12, bottom: 12 },
        }}
        loading={
          <div className="flex h-full items-center justify-center text-sm text-zinc-400">
            Loading editor…
          </div>
        }
      />
    </div>
  );
}
