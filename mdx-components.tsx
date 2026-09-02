import type { MDXComponents } from "mdx/types";

/**
 * Required by @next/mdx: default component mapping for MDX content.
 * Styled for the dark reading experience on lesson pages.
 */
export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    h2: (props) => (
      <h2
        className="mt-8 scroll-mt-20 text-2xl font-semibold tracking-tight text-zinc-100"
        {...props}
      />
    ),
    h3: (props) => (
      <h3
        className="mt-6 scroll-mt-20 text-xl font-semibold tracking-tight text-zinc-100"
        {...props}
      />
    ),
    p: (props) => <p className="leading-7 text-zinc-300" {...props} />,
    ul: (props) => (
      <ul
        className="list-disc space-y-1.5 pl-6 leading-7 text-zinc-300 marker:text-zinc-600"
        {...props}
      />
    ),
    ol: (props) => (
      <ol
        className="list-decimal space-y-1.5 pl-6 leading-7 text-zinc-300 marker:text-zinc-600"
        {...props}
      />
    ),
    a: (props) => (
      <a
        className="font-medium text-indigo-400 underline underline-offset-4 hover:text-indigo-300"
        {...props}
      />
    ),
    strong: (props) => <strong className="font-semibold text-zinc-100" {...props} />,
    blockquote: (props) => (
      <blockquote
        className="border-l-2 border-indigo-500/60 pl-4 italic text-zinc-400"
        {...props}
      />
    ),
    pre: (props) => (
      <pre
        className="overflow-x-auto rounded-lg border border-zinc-800 bg-zinc-900 p-4 text-sm leading-6 text-zinc-200"
        {...props}
      />
    ),
    code: (props) => <code className="font-mono text-[0.9em]" {...props} />,
    table: (props) => (
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm text-zinc-300" {...props} />
      </div>
    ),
    th: (props) => (
      <th
        className="border-b border-zinc-700 px-3 py-2 text-left font-semibold text-zinc-200"
        {...props}
      />
    ),
    td: (props) => <td className="border-b border-zinc-800/60 px-3 py-2" {...props} />,
    hr: (props) => <hr className="border-zinc-800" {...props} />,
    ...components,
  };
}
