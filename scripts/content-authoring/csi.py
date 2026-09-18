#!/usr/bin/env python3
"""
Authoring library for C# — Intermediate (csharp track, course 2).

Clones scripts/content-authoring/csb.py (C# Beginner) so shapes are
byte-compatible with the platform loaders. Writes to
src/content/tracks/csharp/courses/csharp-intermediate; challenges are
language:"csharp"; solution pairs append to
scripts/content-authoring/csi-solutions.mjs (R[id] = reference source,
W[id] = intentionally wrong source) for the two-sided container harness
verify-challenges-csi.mjs — a SEPARATE ledger so the Beginner agent's
csharp-beginner-solutions.mjs is never touched.

C#-specific conventions (probed 2026-09-17, see
docs/CURRICULUM-RESEARCH-CSHARP-INTERMEDIATE.md — re-probes the Beginner
phase's toolchain): raw Roslyn csc on .NET 10, C# 14, no implicit usings
(boilerplates carry the `using` lines), one Solution.cs compiled together
with each test, entry pinned via -main:CjTest, no NuGet/network. Graded
members live on `public class Solution` (or its public nested types);
output challenges grade `static void program()` via Cj.Capture.

Intermediate-specific baseline (all probed in-sandbox this phase):
System.Text.Json, HttpClient with literal HttpMessageHandler stubs
(deterministic HTTP with zero network), async/Task/WhenAll/cancellation,
IAsyncEnumerable + await foreach, Thread/Interlocked/Monitor/SemaphoreSlim,
ConcurrentDictionary/Queue, yield pipelines, full modern LINQ, records,
pattern matching, Span<char>. No NuGet ⇒ no xUnit/Moq/EF Core/DI containers
in graded code — those topics are taught prose-side and graded through
hand-built equivalents (hand-rolled test runners, in-memory stores,
composition-root wiring), mirroring the sandbox-shaped design of
Python Intermediate.
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/csharp")
BASE = os.path.join(TRACK, "courses/csharp-intermediate")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/csi-solutions.mjs")

CS_PRELUDE = (
    "using System;\n"
    "using System.Collections.Generic;\n"
    "using System.IO;\n"
    "using System.Linq;\n"
    "using System.Text;\n"
)

# TinyContainer boilerplate (Module 11+): the lesson-built DI container,
# shipped as provided infrastructure so challenges can compose services.
CJ_TINY_CONTAINER = CS_PRELUDE + (
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public sealed class TinyContainer\n"
    "{\n"
    "    private readonly System.Collections.Generic.Dictionary<System.Type, Func<object>> _factories = new();\n"
    "\n"
    "    public void Register<TService>(Func<TService> factory) =>\n"
    "        RegisterTransient(factory);\n"
    "\n"
    "    public void RegisterTransient<TService>(Func<TService> factory) =>\n"
    "        _factories[typeof(TService)] = () => factory()!;\n"
    "\n"
    "    public void RegisterSingleton<TService>(Func<TService> factory)\n"
    "    {\n"
    "        object? instance = null;\n"
    "        _factories[typeof(TService)] = () =>\n"
    "        {\n"
    "            if (instance is null) instance = factory()!;\n"
    "            return instance;\n"
    "        };\n"
    "    }\n"
    "\n"
    "    public TService Resolve<TService>()\n"
    "    {\n"
    "        if (!_factories.TryGetValue(typeof(TService), out var factory))\n"
    "            throw new System.InvalidOperationException(\"no registration for \" + typeof(TService).Name);\n"
    "        return (TService)factory();\n"
    "    }\n"
    "}\n"
)

# CjStubHandler boilerplate (Module 13+): deterministic HTTP stubs — no
# network. Scripted path -> response-list handlers, a recording handler for
# request-shape checks, a default data handler, and a fake async delay
# recorder so retry/backoff timing is fully deterministic.
CJ_STUB_HANDLER = CS_PRELUDE + (
    "using System.Net;\n"
    "using System.Net.Http;\n"
    "using System.Threading;\n"
    "using System.Threading.Tasks;\n"
    "\n"
    "// Provided infrastructure — do not modify.\n"
    "public sealed class CjStubHandler : HttpMessageHandler\n"
    "{\n"
    "    private readonly System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<HttpResponseMessage>> _script;\n"
    "    private readonly System.Collections.Generic.Dictionary<string, int> _next = new();\n"
    "    private readonly bool _record;\n"
    "    private readonly bool _data;\n"
    "\n"
    "    public static HttpRequestMessage? LastRequest { get; private set; }\n"
    "    public static System.Collections.Generic.List<int> Delays { get; } = new();\n"
    "    public static int HandlerCount { get; private set; }\n"
    "\n"
    "    public CjStubHandler(System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<HttpResponseMessage>> script, bool record = false, bool data = false)\n"
    "    {\n"
    "        _script = script; _record = record; _data = data;\n"
    "        HandlerCount++;\n"
    "    }\n"
    "\n"
    "    public static System.Collections.Generic.List<HttpResponseMessage> One(HttpResponseMessage resp) => new() { resp };\n"
    "    public static System.Collections.Generic.List<HttpResponseMessage> Sequence(params HttpResponseMessage[] items) => new(items);\n"
    "    public static System.Collections.Generic.List<HttpResponseMessage> Always(HttpResponseMessage resp) => new() { resp, resp, resp, resp, resp, resp, resp, resp };\n"
    "    public static HttpResponseMessage Json(int code, string body) =>\n"
    "        new((HttpStatusCode)code) { Content = new StringContent(body) };\n"
    "\n"
    "    // One client per test: stub handler + base address, ready to use.\n"
    "    public static HttpClient Client(System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<HttpResponseMessage>> script) =>\n"
    "        new(new CjStubHandler(script)) { BaseAddress = new System.Uri(\"https://api.test\") };\n"
    "    public static HttpClient Recording() =>\n"
    "        new(new CjStubHandler(new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<HttpResponseMessage>>(), record: true)) { BaseAddress = new System.Uri(\"https://api.test\") };\n"
    "    public static HttpClient Default() =>\n"
    "        new(new CjStubHandler(new System.Collections.Generic.Dictionary<string, System.Collections.Generic.List<HttpResponseMessage>>(), data: true)) { BaseAddress = new System.Uri(\"https://api.test\") };\n"
    "\n"
    "    // Deterministic fake delay: records the requested delay, does not sleep.\n"
    "    public static Task DelayAsync(int milliseconds, CancellationToken ct)\n"
    "    {\n"
    "        Delays.Add(milliseconds);\n"
    "        return Task.CompletedTask;\n"
    "    }\n"
    "\n"
    "    protected override Task<HttpResponseMessage> SendAsync(HttpRequestMessage req, CancellationToken ct)\n"
    "    {\n"
        "        LastRequest = CloneRequest(req);   // snapshot: HttpClient disposes the original after send\n"
    "        string path = req.RequestUri!.PathAndQuery;\n"
    "        if (_data)\n"
    "            return Task.FromResult(Json(200, \"data:\" + path.TrimStart('/')));\n"
    "        if (_script.TryGetValue(path, out var list))\n"
    "        {\n"
    "            int i = _next.TryGetValue(path, out int n) ? n : 0;\n"
    "            _next[path] = System.Math.Min(i + 1, list.Count - 1);\n"
    "            return Task.FromResult(Clone(list[i]));   // fresh instance per send — a sent response is disposed\n"
    "        }\n"
    "        return Task.FromResult(Json(404, \"\"));\n"
    "    }\n"
    "\n"
    "    private static HttpResponseMessage Clone(HttpResponseMessage source)\n"
    "    {\n"
    "        var copy = new HttpResponseMessage(source.StatusCode);\n"
    "        foreach (var h in source.Headers) copy.Headers.TryAddWithoutValidation(h.Key, h.Value);\n"
    "        if (source.Content is not null)\n"
    "            copy.Content = new StringContent(\n"
    "                source.Content.ReadAsStringAsync(CancellationToken.None).GetAwaiter().GetResult());\n"
    "        return copy;\n"
    "    }\n"
    "\n"
    "    private static HttpRequestMessage CloneRequest(HttpRequestMessage source)\n"
    "    {\n"
    "        var copy = new HttpRequestMessage(source.Method, source.RequestUri);\n"
    "        foreach (var h in source.Headers) copy.Headers.TryAddWithoutValidation(h.Key, h.Value);\n"
    "        if (source.Content is not null)\n"
    "        {\n"
    "            string body = source.Content.ReadAsStringAsync(CancellationToken.None).GetAwaiter().GetResult();\n"
    "            var media = source.Content.Headers.ContentType?.MediaType ?? \"application/octet-stream\";\n"
    "            copy.Content = new StringContent(body, System.Text.Encoding.UTF8, media);\n"
    "        }\n"
    "        return copy;\n"
    "    }\n"
    "}\n"
)






def _w(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(text)


def _j(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def mod_dir(m):
    return os.path.join(BASE, "modules", m)


def _ensure_solutions_header():
    if not os.path.exists(SOLUTIONS):
        _w(
            SOLUTIONS,
            "/**\n"
            " * Reference (R) and intentionally-wrong (W) solutions for the\n"
            " * C# Intermediate two-sided harness (verify-challenges-csi.mjs).\n"
            " * Appended by the csi_*.py authoring scripts; parsed as a ledger.\n"
            " */\n"
            "const R = {};\n"
            "const W = {};\n",
        )
    with io.open(SOLUTIONS, "r", encoding="utf-8") as f:
        src = f.read()
    if "export { R, W };" not in src:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("\nexport { R, W };\n")


def write_module(m, title, summary, vi_title, vi_summary, lessons, practices):
    _w(
        os.path.join(mod_dir(m), "module.json"),
        _j(
            {
                "id": m,
                "title": title,
                "summary": summary,
                "lessons": [{"reference": (l if l.startswith("csi-") else "csi-" + l)} for l in lessons],
                "practices": [{"reference": (p if p.startswith("csi-") else "csi-" + p)} for p in practices],
            }
        ),
    )
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="intermediate"):
    if not lid.startswith("csi-"):
        lid = "csi-" + lid  # course-level namespace
    d = os.path.join(mod_dir(m), "lessons")
    _w(
        os.path.join(d, lid + ".json"),
        _j(
            {
                "id": lid,
                "title": title,
                "description": description,
                "minutes": minutes,
                "difficulty": difficulty,
                "contentPath": "./" + lid + ".mdx",
            }
        ),
    )
    _w(os.path.join(d, lid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    _w(os.path.join(d, lid + ".mdx"), mdx.strip() + "\n")
    _w(os.path.join(d, lid + ".vi.mdx"), vi_mdx.strip() + "\n")
    print("lesson:", m + "/" + lid)


def challenge(cid, title, prompt, boilerplate, tests, level=None, difficulty="intermediate"):
    """C# challenge. tests = [(name, code, hint), ...]."""
    out = {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "language": "csharp",
        "boilerplate": boilerplate,
        "tests": [{"name": n, "code": c, "hint": h} for (n, c, h) in tests],
    }
    if level:
        if level in {"imitation", "guided", "independent", "combination", "real-world", "debugging", "mini-build"}:
            out["level"] = level
        else:
            print("WARN: dropping invalid level %r for %s" % (level, cid))
    return out


def vi_challenge(vi_title, vi_prompt, vi_tests):
    return {
        "title": vi_title,
        "prompt": vi_prompt,
        "tests": [{"name": n, "hint": h} for (n, h) in vi_tests],
    }


def write_practice(m, sid, title, description, vi_title, vi_description, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions=None):
    d = os.path.join(mod_dir(m), "practices")
    _w(
        os.path.join(d, sid + ".json"),
        _j(
            {
                "id": sid,
                "title": title,
                "description": description,
                "afterLesson": (after_lesson if after_lesson.startswith("csi-") else "csi-" + after_lesson),
                "minutes": minutes,
                "difficulty": difficulty,
                "challenges": [c["id"] for c in challenges],
            }
        ),
    )
    _w(os.path.join(d, sid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    for c in challenges:
        _w(os.path.join(d, sid, "challenges", c["id"] + ".json"), _j(c))
    for cid, vc in vi_challenges.items():
        _w(os.path.join(d, sid, "challenges", cid + ".vi.json"), _j(vc))
    if solutions:
        _ensure_solutions_header()
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            for cid, ref, wrong in solutions:
                f.write("R[" + json.dumps(cid) + "] = " + json.dumps(ref) + ";\n")
                f.write("W[" + json.dumps(cid) + "] = " + json.dumps(wrong) + ";\n")
    print("practice set:", m + "/" + sid)


def write_checkpoint(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, ch, vi_ch, solution=None, wrong=None):
    """Checkpoint lesson with a lesson-attached challenge (+ solution pair).

    NOTE: the checkpoint lesson id must be listed in write_module's lessons
    (the Beginner pipeline includes it there); the lesson-attached challenge
    id must DIFFER from the lesson id (a lesson JSON and a challenge JSON are
    different documents — one id may name only one of each kind).
    """
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    d = os.path.join(mod_dir(m), "lessons", lid, "challenges")
    _w(os.path.join(d, ch["id"] + ".json"), _j(ch))
    _w(os.path.join(d, ch["id"] + ".vi.json"), _j(vi_ch))
    if solution is not None and wrong is not None:
        _ensure_solutions_header()
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("R[" + json.dumps(ch["id"]) + "] = " + json.dumps(solution) + ";\n")
            f.write("W[" + json.dumps(ch["id"]) + "] = " + json.dumps(wrong) + ";\n")


def write_course(course_id, title, description, audience, outcomes, prerequisites, modules, vi_title, vi_description):
    _w(
        os.path.join(BASE, "course.json"),
        _j(
            {
                "id": course_id,
                "title": title,
                "description": description,
                "audience": audience,
                "outcomes": outcomes,
                "prerequisites": prerequisites,
                "modules": [{"reference": m} for m in modules],
            }
        ),
    )
    _w(os.path.join(BASE, "course.vi.json"), _j({"title": vi_title, "description": vi_description}))
    print("course manifest:", course_id, "modules:", len(modules))
