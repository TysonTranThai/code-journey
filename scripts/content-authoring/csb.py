#!/usr/bin/env python3
"""
Authoring library for C# — Beginner (csharp track, course 1).

Clones scripts/content-authoring/cint.py so shapes are byte-compatible with
the platform loaders. Writes to src/content/tracks/csharp/courses/
csharp-beginner; challenges are language:"csharp"; solution pairs append to
scripts/content-authoring/csharp-beginner-solutions.mjs (R[id] = reference
source, W[id] = intentionally wrong source) for the two-sided container
harness verify-challenges-csharp.mjs — a SEPARATE ledger so the other
courses' ledgers are never touched.

C#-specific conventions (probed 2026-09-16, see
docs/CURRICULUM-RESEARCH-CSHARP-BEGINNER.md): raw Roslyn csc on .NET 10,
C# 14, no implicit usings (boilerplates carry the `using` lines), one
Solution.cs compiled together with each test, entry pinned via -main:CjTest,
no NuGet/network. Graded members live on `public class Solution` (or its
nested/public types in the OOP modules); output challenges grade
`static void program()` via Cj.Capture.
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/csharp")
BASE = os.path.join(TRACK, "courses/csharp-beginner")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/csharp-beginner-solutions.mjs")

# Shared challenge prefix: every graded Solution.cs starts from these usings
# (raw csc has no implicit usings — verified by probe).
CS_PRELUDE = "using System;\nusing System.Collections.Generic;\nusing System.IO;\nusing System.Linq;\nusing System.Text;\n"


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
            " * C# Beginner two-sided harness (verify-challenges-csharp.mjs).\n"
            " * Appended by the csharp_*.py authoring scripts; parsed as a ledger.\n"
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
                "lessons": [{"reference": (l if l.startswith("csb-") else "csb-" + l)} for l in lessons],
                "practices": [{"reference": (p if p.startswith("csb-") else "csb-" + p)} for p in practices],
            }
        ),
    )
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="beginner"):
    if not lid.startswith("csb-"):
        lid = "csb-" + lid  # course-level namespace
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


def challenge(cid, title, prompt, boilerplate, tests, level=None, difficulty="beginner"):
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
                "afterLesson": (after_lesson if after_lesson.startswith("csb-") else "csb-" + after_lesson),
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
