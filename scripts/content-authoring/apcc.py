#!/usr/bin/env python3
"""
Authoring library for AP CSA — Core & Exam Preparation (ap-csa track, course 2).

Clones scripts/content-authoring/apc.py (which clones javaa.py) so shapes are
byte-compatible with the platform loaders. Writes to
src/content/tracks/ap-csa/courses/ap-csa-core; challenges are language:"java";
solution pairs append to scripts/content-authoring/apcc-solutions.mjs (R/W) —
a SEPARATE ledger so the Foundations ledger is never touched.

Graded code compiles under `javac --release 21` inside the platform sandbox
harness (src/workers/java-runtime.ts). Same authoring discipline as apc.py:
raw triple-quoted Java strings, self-contained tests, behavioral near-misses
for wrong solutions, explicit CjTestBase messages.
"""

import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TRACK = os.path.join(ROOT, "src/content/tracks/ap-csa")
BASE = os.path.join(TRACK, "courses/ap-csa-core")
SOLUTIONS = os.path.join(ROOT, "scripts/content-authoring/apcc-solutions.mjs")


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
            " * AP CSA Core two-sided harness (verify-challenges-apc-core.mjs).\n"
            " * Appended by the apcc_*.py authoring scripts; parsed as a ledger.\n"
            " */\n"
            "const R = {};\n"
            "const W = {};\n",
        )
    with io.open(SOLUTIONS, "r", encoding="utf-8") as f:
        src = f.read()
    if "export { R, W };" not in src:
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("\nexport { R, W };\n")


def write_course(title, description, audience, outcomes, vi_title, vi_description, vi_audience, vi_outcomes, modules):
    assert len(description) <= 400, ("course desc", len(description))
    assert len(audience) <= 400, ("course audience", len(audience))
    for o in outcomes:
        assert len(o) <= 200, ("outcome", len(o))
    _w(
        os.path.join(BASE, "course.json"),
        _j(
            {
                "id": "ap-csa-core",
                "title": title,
                "description": description,
                "audience": audience,
                "outcomes": outcomes,
                "prerequisites": ["ap-csa-beginner"],
                "modules": [{"reference": m} for m in modules],
            }
        ),
    )
    assert len(vi_description) <= 400, ("course vi desc", len(vi_description))
    assert len(vi_audience) <= 400, ("course vi audience", len(vi_audience))
    _w(
        os.path.join(BASE, "course.vi.json"),
        _j({"title": vi_title, "description": vi_description, "audience": vi_audience, "outcomes": vi_outcomes}),
    )
    print("course: ap-csa-core")


def write_module(m, title, summary, vi_title, vi_summary, lessons, practices):
    assert len(summary) <= 200, (m, len(summary))
    _w(
        os.path.join(mod_dir(m), "module.json"),
        _j(
            {
                "id": m,
                "title": title,
                "summary": summary,
                "lessons": [{"reference": l} for l in lessons],
                "practices": [{"reference": p} for p in practices],
            }
        ),
    )
    assert len(vi_summary) <= 200, (m + " vi", len(vi_summary))
    _w(
        os.path.join(mod_dir(m), "module.vi.json"),
        _j({"title": vi_title, "summary": vi_summary}),
    )
    print("module:", m)


def write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx, difficulty="intermediate"):
    """Signature matches apc.write_lesson: minutes appears once, before EN mdx."""
    assert len(description) <= 200, (lid, len(description))
    _w(
        os.path.join(mod_dir(m), "lessons", lid + ".json"),
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
    assert len(vi_description) <= 200, (lid + " vi", len(vi_description))
    _w(os.path.join(mod_dir(m), "lessons", lid + ".vi.json"), _j({"title": vi_title, "description": vi_description}))
    _w(os.path.join(mod_dir(m), "lessons", lid + ".mdx"), mdx.strip() + "\n")
    _w(os.path.join(mod_dir(m), "lessons", lid + ".vi.mdx"), vi_mdx.strip() + "\n")
    print("lesson:", m + "/" + lid)


def challenge(cid, title, prompt, boilerplate, tests, level=None, difficulty="intermediate"):
    """Java challenge. tests = [(name, code, hint), ...]."""
    assert len(prompt) <= 4000, (cid, len(prompt))
    out = {
        "id": cid,
        "title": title,
        "prompt": prompt,
        "difficulty": difficulty,
        "language": "java",
        "boilerplate": boilerplate,
        "tests": [{"name": n, "code": c, "hint": h} for (n, c, h) in tests],
    }
    if level:
        assert level in {"imitation", "guided", "independent", "combination", "real-world", "debugging", "mini-build"}, cid
        out["level"] = level
    return out


def vi_challenge(vi_title, vi_prompt, vi_tests):
    return {
        "title": vi_title,
        "prompt": vi_prompt,
        "tests": [{"name": n, "hint": h} for (n, h) in vi_tests],
    }


def write_practice(m, sid, title, description, vi_title, vi_description, after_lesson, minutes, difficulty, challenges, vi_challenges, solutions=None):
    assert len(description) <= 200, (sid, len(description))
    d = os.path.join(mod_dir(m), "practices")
    _w(
        os.path.join(d, sid + ".json"),
        _j(
            {
                "id": sid,
                "title": title,
                "description": description,
                "afterLesson": after_lesson,
                "minutes": minutes,
                "difficulty": difficulty,
                "challenges": [c["id"] for c in challenges],
            }
        ),
    )
    assert len(vi_description) <= 200, (sid + " vi", len(vi_description))
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
    Also registers itself in module.json's lessons list (loader contract).
    """
    write_lesson(m, lid, title, description, minutes, mdx, vi_title, vi_description, vi_mdx)
    mp = os.path.join(mod_dir(m), "module.json")
    with io.open(mp, encoding="utf-8") as f:
        manifest = json.load(f)
    refs = [l["reference"] for l in manifest.get("lessons", [])]
    if lid not in refs:
        manifest["lessons"].append({"reference": lid})
        _w(mp, _j(manifest))
    d = os.path.join(mod_dir(m), "lessons", lid, "challenges")
    _w(os.path.join(d, ch["id"] + ".json"), _j(ch))
    _w(os.path.join(d, ch["id"] + ".vi.json"), _j(vi_ch))
    if solution is not None and wrong is not None:
        _ensure_solutions_header()
        with io.open(SOLUTIONS, "a", encoding="utf-8") as f:
            f.write("R[" + json.dumps(ch["id"]) + "] = " + json.dumps(solution) + ";\n")
            f.write("W[" + json.dumps(ch["id"]) + "] = " + json.dumps(wrong) + ";\n")
    print("checkpoint:", m + "/" + lid)
