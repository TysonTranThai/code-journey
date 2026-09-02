"use client";

import Editor, { type OnMount } from "@monaco-editor/react";

/**
 * Monaco wrapper for challenge code. Loads the HTML language mode by
 * default; theme matches the platform's dark palette. Loading via the
 * @monaco-editor/react CDN loader keeps the bundle small (documented
 * discretion in 03-CONTEXT D-10); local bundling is a Phase 6 option.
 */
export function CodeEditor({
  value,
  onChange,
  language = "html",
  ariaLabel,
}: {
  value: string;
  onChange: (next: string) => void;
  language?: string;
  ariaLabel: string;
}) {
  const onMount: OnMount = (editor) => {
    editor.focus();
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
          <div className="flex h-full items-center justify-center text-sm text-zinc-500">
            Loading editor…
          </div>
        }
      />
    </div>
  );
}
