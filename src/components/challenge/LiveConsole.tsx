"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import { useI18n } from "@/lib/i18n/provider";
import { getErrorExplanation } from "@/lib/mentor/error-explainer";
import { ErrorExplanationCard } from "./ErrorExplanationCard";

/**
 * Live output for JavaScript challenges (Course 1 revision UX): runs the
 * learner's code as they type and streams console.log output — so JS
 * challenges get the same "see it happen" feedback the HTML/CSS preview gives.
 *
 * Security model (PLAT-08 unchanged — grading stays server-side):
 *  - The code runs in a Web Worker created from a blob URL (CSP
 *    `worker-src 'self' blob:`), so it cannot touch the DOM or app state.
 *  - No network: `connect-src 'self'` blocks the worker's fetch, and the
 *    worker globals are recorder stubs, not real APIs.
 *  - A runaway script (infinite loop) cannot freeze the page: the worker is
 *    TERMINATED from the outside after a short budget — the same host-side
 *    kill model the sandbox container uses.
 *  - Stub globals mirror the grader's sandbox (button, display, storage,
 *    document, api, fetch…) so what the learner sees live matches what
 *    Submit grades. These are recorders, never real platform objects.
 */

/** Per-run budget before the worker is terminated (ms). */
const RUN_BUDGET_MS = 2500;
/** Debounce while typing (ms). */
const DEBOUNCE_MS = 600;
/** Output caps (mirrors the sandbox's truncation philosophy). */
const MAX_LINES = 60;
const MAX_CHARS = 4000;

/** Worker source: recorder stubs + console capture, one fresh worker per run. */
const WORKER_SRC = String.raw`
const __out = [];
function __fmt(args) {
  return args
    .map((a) => {
      if (typeof a === "string") return a;
      try { return JSON.stringify(a); } catch { return String(a); }
    })
    .join(" ");
}
function __send(isDone) {
  self.postMessage({
    type: isDone ? "done" : "chunk",
    text: __out.slice(0, ${MAX_LINES}).join("\n").slice(0, ${MAX_CHARS}),
  });
}

self.console = {
  log: (...a) => { __out.push(__fmt(a)); __send(false); },
  info: (...a) => { __out.push(__fmt(a)); __send(false); },
  warn: (...a) => { __out.push(__fmt(a)); __send(false); },
  error: (...a) => { __out.push(__fmt(a)); __send(false); },
};

// Recorder stubs — same contract as the grader's sandbox (workers/sandbox.ts).
function makeEl(tag) {
  const e = {
    tagName: String(tag || "div").toUpperCase(),
    textContent: "",
    className: "",
    src: "",
    alt: "",
    value: "",
    children: [],
    listeners: {},
    classList: { add: function () {}, remove: function () {}, toggle: function () {} },
    addEventListener: function (type, fn) { e.listeners[type] = fn; },
    appendChild: function (c) { e.children.push(c); },
    remove: function () {},
  };
  return e;
}
const __listEl = makeEl("ul");
const __store = new Map();
self.api = {
  loadUser: () => Promise.resolve({ name: "Ada" }),
  loadGreeting: (n) => Promise.resolve("Hello, " + n),
};
self.fetch = () => Promise.resolve({ ok: true, json: async () => ({ name: "Ada", role: "learner" }) });
self.checkReady = () => Promise.resolve(true);
self.storage = {
  setItem: (k, v) => __store.set(String(k), String(v)),
  getItem: (k) => (__store.has(String(k)) ? __store.get(String(k)) : null),
  removeItem: (k) => __store.delete(String(k)),
};
self.document = {
  createElement: (t) => makeEl(t),
  querySelector: (sel) => (String(sel).includes("task-list") || String(sel).includes("todo-list") ? __listEl : makeEl("div")),
  getElementById: () => __listEl,
};
self.button = makeEl("button");
self.display = makeEl("span");
self.heading = makeEl("h1");
self.intro = makeEl("p");
self.hero = makeEl("img");
self.form = makeEl("form");
self.usernameInput = makeEl("input");
self.emailInput = makeEl("input");
self.errorBox = makeEl("div");

self.onmessage = (e) => {
  try {
    new Function(e.data)();
  } catch (err) {
    __out.push("Error: " + (err && err.message ? err.message : String(err)));
  }
  // Let microtasks/promises flush before closing.
  setTimeout(() => { __send(true); self.close(); }, 150);
};
`;

type ConsoleStatus = "idle" | "running" | "stopped";

export function LiveConsole({
  code,
  boilerplate,
  language,
  serverOutput,
  isServerRunning,
  failedTestMessage,
}: {
  code: string;
  boilerplate: string;
  language?: string;
  serverOutput?: string;
  isServerRunning?: boolean;
  failedTestMessage?: string;
}) {
  const { d, t } = useI18n();
  const [output, setOutput] = useState("");
  const [status, setStatus] = useState<ConsoleStatus>("idle");
  const workerRef = useRef<Worker | null>(null);
  const killTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const stopWorker = useCallback(() => {
    if (killTimer.current) {
      clearTimeout(killTimer.current);
      killTimer.current = null;
    }
    if (workerRef.current) {
      workerRef.current.terminate();
      workerRef.current = null;
    }
  }, []);

  useEffect(() => stopWorker, [stopWorker]);

  const runCode = useCallback(
    (next: string) => {
      stopWorker();
      setOutput("");
      setStatus("running");

      const blob = new Blob([WORKER_SRC], { type: "text/javascript" });
      const url = URL.createObjectURL(blob);
      let worker: Worker;
      try {
        worker = new Worker(url);
      } catch {
        URL.revokeObjectURL(url);
        setStatus("stopped");
        setOutput(d.console.unavailable);
        return;
      }
      workerRef.current = worker;

      worker.onmessage = (
        e: MessageEvent<{ type?: string; text?: string } | string>,
      ) => {
        const data = e.data;
        const text = typeof data === "string" ? data : (data?.text ?? "");
        setOutput(text);
        if (typeof data === "object" && data?.type === "done") {
          if (killTimer.current) {
            clearTimeout(killTimer.current);
            killTimer.current = null;
          }
          setStatus("idle");
        }
      };
      worker.onerror = () => {
        if (killTimer.current) {
          clearTimeout(killTimer.current);
          killTimer.current = null;
        }
        setStatus("idle");
        setOutput((prev) => prev || d.console.threw);
      };

      // Host-side kill: an infinite loop must never freeze the page.
      killTimer.current = setTimeout(() => {
        stopWorker();
        setStatus("stopped");
        setOutput(
          (prev) =>
            `${prev}${prev ? "\n" : ""}${t(d.console.stoppedLong, { seconds: RUN_BUDGET_MS / 1000 })}`,
        );
      }, RUN_BUDGET_MS);

      worker.postMessage(next);
      URL.revokeObjectURL(url); // worker already constructed from the blob
    },
    [stopWorker, d, t],
  );

  const isJs = !language || language === "javascript" || language === "js";

  // Live: re-run (debounced) whenever the code changes (JavaScript only).
  useEffect(() => {
    if (!isJs) return;
    const t = setTimeout(() => runCode(code), DEBOUNCE_MS);
    return () => clearTimeout(t);
  }, [code, isJs, runCode]);

  const untouched = code === boilerplate;
  const displayOutput = isJs ? output : (serverOutput ?? "");
  const effectiveStatus: ConsoleStatus = isJs
    ? status
    : isServerRunning
      ? "running"
      : "idle";

  const stdoutExplanation = getErrorExplanation(displayOutput, d, language);
  const explanation =
    stdoutExplanation ??
    (failedTestMessage ? getErrorExplanation(failedTestMessage, d, language) : null);
  const isErrorOutput =
    displayOutput.startsWith("Error:") ||
    displayOutput.includes("error:") ||
    displayOutput.includes("Error:") ||
    displayOutput.includes("SyntaxError") ||
    displayOutput.includes("ReferenceError") ||
    displayOutput.includes("TypeError") ||
    displayOutput.includes("RangeError") ||
    displayOutput.includes("Stopped:") ||
    displayOutput.includes("Đã dừng:") ||
    displayOutput.startsWith("Lỗi:") ||
    displayOutput.includes("Exception") ||
    stdoutExplanation !== null;

  return (
    <section
      aria-label={d.console.aria}
      className="glass-card p-4 rounded-2xl flex flex-col gap-2.5 shadow-xl"
    >
      <div className="flex items-center justify-between gap-2 border-b border-white/[0.08] pb-2">
        <div className="flex items-center gap-2">
          <span className="h-2.5 w-2.5 rounded-full bg-rose-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-amber-500/80 inline-block" aria-hidden="true" />
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/80 inline-block" aria-hidden="true" />
          <h3 className="font-mono text-xs font-semibold uppercase tracking-wider text-zinc-300 ml-1">
            {isJs ? d.console.heading : d.console.headingBackend}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          {effectiveStatus === "stopped" && (
            <span className="badge-pixel badge-pixel-streak text-[10px]">{d.console.stopped}</span>
          )}
          {isJs && (
            <span className="badge-pixel badge-pixel-level text-[10px] uppercase font-mono text-emerald-400">
              ● LIVE
            </span>
          )}
          {!isJs && (
            <span className="badge-pixel badge-pixel-level text-[10px] uppercase font-mono">
              {(language ?? "SANDBOX").toUpperCase()} {effectiveStatus === "running" ? d.console.runningBadge : "OUTPUT"}
            </span>
          )}
        </div>
      </div>
      <div
        role="log"
        aria-live="polite"
        className={`max-h-48 min-h-20 overflow-auto whitespace-pre-wrap rounded-xl border border-white/[0.08] bg-[#070a18] p-3.5 font-mono text-xs leading-relaxed shadow-inner ${
          isErrorOutput ? "text-rose-300" : "text-emerald-400"
        }`}
      >
        {displayOutput.length > 0
          ? displayOutput
          : effectiveStatus === "running"
            ? (isJs ? "…" : d.console.runningBackend)
            : isJs
              ? (untouched ? d.console.emptyStart : d.console.noOutput)
              : serverOutput !== undefined
                ? d.console.noOutputBackend
                : d.console.emptyBackend}
      </div>
      {explanation && <ErrorExplanationCard explanation={explanation} />}
      <p className="font-mono text-[11px] text-zinc-400">
        ● {isJs ? d.console.caption : d.console.captionBackend}
      </p>
    </section>
  );
}
